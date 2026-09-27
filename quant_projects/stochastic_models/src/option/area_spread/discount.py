import numpy as np
from option.area_spread.process_params import ProcessParams
from sde_simulator.option_params import OptionParams

class Discount:
    """
    Specifies discounting functions used in pricing of the option.

    Args:
        par:
            Holds parameters of the process.
    
    """
    def __init__(self,
                 par : ProcessParams):
        self.proc_par = par

    def terminal(self,
                 endpoints : np.ndarray,
                 opt_par : OptionParams
                 ) -> np.ndarray:
        """
        Suitable for pricing european variant of the option.

        Args:
            endpoints:
                Final state of the process simulated using SDEsimulator.endpoints.
            opt_par :
                Specifies parameters of the option.
        
        Returns:
            np.ndarray of discount factors for corresponding endpoints.
        """
        
        T = opt_par.T
        t_0 = opt_par.t_0
        n_intervals = opt_par.n_intervals
        n_sim = opt_par.n_sim
        r = self.proc_par.r
        
        discount = np.full(n_sim, np.exp(-r*(T - t_0)))
        return discount
    

    def pathwise(self,
                 paths : np.ndarray,
                 opt_par : OptionParams
                 ) -> np.ndarray:
        
        """
        Suitable for pricing american variant of the option.

        Args:
            paths:
                Paths of the process simulated using SDEsimulator.path.
            opt_par :
                Specifies parameters of the option.
        
        Returns:
            np.ndarray of discount factors for corresponding states.
        """
        
        T = opt_par.T
        t_0 = opt_par.t_0
        n_intervals = opt_par.n_intervals
        n_sim = opt_par.n_sim
        r = self.proc_par.r
                 
        times = np.linspace(t_0, T, n_intervals + 1)
        dis_vec = np.exp(-r * times).reshape(1,-1)
        dis_arr = np.repeat(dis_vec, n_sim, axis = 0).T
        return dis_arr
        
