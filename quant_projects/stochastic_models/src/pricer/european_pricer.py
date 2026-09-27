from typing import Callable
from sde_simulator.sde_engine import SDESimulator
from sde_simulator.option_params import OptionParams

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
                 discount : Callable):
        
        self.simulator = simulator
        self.payoff = payoff
        self.discount = discount

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
        price = (time_value * intrinsic_value).mean() #evaluates the expectation of discounted payoffs
        return float(price)
    