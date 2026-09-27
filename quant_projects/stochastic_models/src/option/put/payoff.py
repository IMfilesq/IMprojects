from option.put.process_params import ProcessParams
from sde_simulator.option_params import OptionParams
import numpy as np

class Payoff:
    """
    Extracts payoffs of the option from simulation results.

    Args:
        par:
            Holds parameters of the process.
        K:
            Strike price of the option.
    """

    def __init__(self,
                 par : ProcessParams,
                 K : float):
        self.par = par
        self.K = K

    def terminal(self,
                 endpoints : np.ndarray,
                 opt_par : OptionParams
                 ) -> np.ndarray:
        """
        Extracts payoff of the option from endpoints of the simulation.

        Args:
            endpoints:
                Final state of the process simulated using SDEsimulator.endpoints.
            opt_par :
                Specifies parameters of the option.
        
        Returns:
            np.ndarray of discount factors for corresponding payoffs.
        """
        
        return np.maximum(self.K - endpoints, 0).squeeze()
    

    def pathwise(self,
                 paths : np.ndarray,
                 opt_par : OptionParams
                 ) -> np.ndarray:
        
        """
        Extracts payoff of the option from the simulated paths.

        Args:
            paths:
                Simulated paths of the process.
            opt_par :
                Specifies parameters of the option.
        
        Returns:
            np.ndarray of discount factors for corresponding payoffs.
        """
                 
        return np.maximum(self.K - paths.squeeze(), 0)
        