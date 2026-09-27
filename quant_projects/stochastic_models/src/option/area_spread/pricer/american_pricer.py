from typing import Callable
from sde_simulator.sde_engine import SDESimulator
from sde_simulator.option_params import OptionParams
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from option.area_spread.controll_spread import Controll
import numpy as np

class AmericanPricer:
    """
    Used for pricing options in american style.

    Args:
        simmulator:
            Engine used for monte carlo simulation of the paths.
        payoff: 
            Function extracting payoff from the paths.
        discount:
            Function evaluating the discount factor for each state.
    
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
        Evaluates the price of an american derivative secuirity.
        Since used here Longstaff - Schwartz alghoritm requires storing whole paths, the function is based on simulate_paths().
        
        Args:
            opt_par :
                Specifies parameters of the option.
                
        Returns:
            European price of an option
        """

        path_arr = self.simulator.paths(opt_par)
        intrinsic = self.payoff(path_arr, opt_par)
        disc = self.discount(path_arr, opt_par)
        
        # t=0 discounted exercise values

        exercise_t0 = intrinsic * disc
        
        # Start at maturity with t=0-discounted payoff
        cash_flow = exercise_t0[-1, :].copy()

        # tracks the time of exercise for each path, initialized to maturity
        stopping_indices = np.full(opt_par.n_sim, opt_par.n_intervals)
        
        # Backward induction
        for i in range(opt_par.n_intervals - 1, 0, -1):
            x = path_arr[i, :, :]
            # Filter: Only regress on paths that are In-The-Money (ITM)
            # Assuming payoff > 0 implies ITM
            itm_mask = intrinsic[i, :] > 0
            
            if np.sum(itm_mask) > 0:
                poly = PolynomialFeatures(degree=2)
                X_poly = poly.fit_transform(x[itm_mask])
                model = LinearRegression()
                model.fit(X_poly, cash_flow[itm_mask])
                
                # Predict continuation for all paths
                continuation_t0 = model.predict(poly.transform(x))
            else:
                continuation_t0 = np.zeros(opt_par.n_sim)
            
            # Exercise if immediate payoff > continuation value
            exercise_now_t0 = exercise_t0[i, :]
            exercise_mask = (exercise_now_t0 > continuation_t0) & itm_mask
            
            # Update cash flows: exercise now OR continue with existing future cash flow
            cash_flow = np.where(exercise_mask, exercise_now_t0, cash_flow)

            stopping_indices = np.where(exercise_mask, i, stopping_indices)

        # 2. Get your terminal European control variate values (at index -1)
        # path_arr shape is assumed to be (n_intervals + 1, n_sim, n_features)
        S1_T = path_arr[-1, :, 0]
        S2_T = path_arr[-1, :, 1]
        
        # Calculate raw terminal spread
        X_terminal = self.controll.payoff(S1_T, S2_T)
        X_expected_terminal = self.controll.expected_spread_payoff(opt_par.t_0, opt_par.T)

        # 3. DISCOUNT the control variate to t=0 to match cash_flow
        # Assuming r is available via opt_par or self.controll.par
        discount_factor_T = np.exp(-self.controll.par.r * (opt_par.T - opt_par.t_0))
        
        X = X_terminal * discount_factor_T
        X_expected = X_expected_terminal * discount_factor_T

        # 4. Compute optimal alpha via covariance on identically-discounted terms
        cov_matrix = np.cov(cash_flow, X)
        c_optimal = -cov_matrix[0, 1] / cov_matrix[1, 1]

        # 5. Final variance-reduced American Option Price
        american_option_price = np.mean(cash_flow + c_optimal * (X - X_expected))
            
        return float(american_option_price)
    