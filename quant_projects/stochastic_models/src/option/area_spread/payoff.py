from option.area_spread.process_params import ProcessParams
from sde_simulator.option_params import OptionParams
import numpy as np
import scipy.stats as st

class Payoff:
    """
    Extracts payoffs of the option from simulation results.

    Args:
        par:
            Holds parameters of the process.
    """

    def __init__(self,
                 par : ProcessParams):
        self.par = par



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

        return endpoints[:, 2]

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
        return paths[:, :, 2]
