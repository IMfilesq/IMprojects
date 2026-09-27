from option.put.process_params import ProcessParams
import numpy as np

class Process:
    """
    Defines the process process we use for pricing put options. It is expressed as Euler's formula for SDE.

    Args:
        parameters:
            Specifies parameters of the process
    
    Attributes:
        params:
            Parameters of the process   

        init_state: 
            Value the process starts with 

    """

    def __init__(self,
                 parameters : ProcessParams):
        self.params = parameters
        self.init_state = self.params.S0

    def state_update(self,
                    old_state : np.ndarray,
                    dt : float,
                    dW : np.ndarray,
                    ) -> np.ndarray:
        
        """
        Used for evaluating the next state of the process.

        Args:
            old_state:
                Prievious state of the process.

            dt:
                Time that passes between process steps.

            dW:
                Noise driving the process.

        Returns:
            Next state of the process

        """ 
        #GBM evolution for the asset
        new_state = old_state + self.params.r * old_state * dt + self.params.sigma * old_state * dW
        return new_state

    def noise(self,
              dt : float,
              n_sim : int,
              ) -> np.ndarray:
        
        """
        Used for evaluating the one step increment of the noise driving the process.

        Args:
            dt:
                Length of the time interval.

            n_sim:
                Number of paths we simulate.

        Returns:
            dW increment of the process.

        """ 
        #Independent increments
        dW = np.random.normal(0, np.sqrt(dt), n_sim)
        return dW[:, np.newaxis]

