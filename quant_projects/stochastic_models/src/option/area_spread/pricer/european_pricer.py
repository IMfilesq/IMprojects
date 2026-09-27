from typing import Callable
from sde_simulator.sde_engine import SDESimulator
from sde_simulator.option_params import OptionParams
from option.area_spread.controll_spread import Controll
import numpy as np

class EuropeanPricer:
    """
    Used for pricing options in european style.

    Args:
        simmulator:
            Engine used for monte carlo simulation of the termial states.
        payoff: 
            Function extracting payoff from the terminal states.
        discount:
            Function evaluating the discount factor for terminal states.
    
    """
    
    def __init__(self,
                 simulator : SDESimulator,
                 payoff : Callable,
                 discount : Callable,
                 controll : Controll):
        
        self.simulator = simulator
        self.payoff = payoff
        self.discount = discount
        self.controll = controll

    def price(self,
                opt_par : OptionParams
                ) -> float:
            
            """
            Evaluates the price of an european derivative secuirity. Is based on simulate_endpoints() thus does not require whole paths to run.

            Args:
                opt_par :
                    Specifies parameters of the option.
                    
            Returns:
                European price of an option
            """
            
            endpoints = self.simulator.endpoints(opt_par)
            
            time_value = self.discount(endpoints, opt_par) #evaluates discount factor
            intrinsic_value = self.payoff(endpoints, opt_par)
            
            # 1. Get raw control variate arrays
            controll_intrinsic = self.controll.payoff(endpoints[:, 0], endpoints[:, 1])
            X_expected = self.controll.expected_spread_payoff(opt_par.t_0, opt_par.T)
            
            # 2. Compute covariance matrix and optimal coefficient
            # cov_matrix[0, 1] is Cov(Y, X)
            # cov_matrix[1, 1] is Var(X)
            cov_matrix = np.cov(intrinsic_value, controll_intrinsic)
            c_optimal = -cov_matrix[0, 1] / cov_matrix[1, 1] 
            
            # 3. Apply the variance reduction adjustment to the intrinsic value
            # Note the '+' sign because c_optimal already contains the negative sign
            controlled = intrinsic_value + c_optimal * (controll_intrinsic - X_expected)
            
            # 4. Discount to present value and take the expectation (mean)
            price = (time_value * controlled).mean()
            
            return float(price)
    