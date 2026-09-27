import numpy as np
from option.area_spread.process_params import ProcessParams

class Process:
    """
    Defines the 3-dimensional process we use for pricing. It is expressed as Euler's formula for SDE.
    First two dimensions represent asset prices as GBM.
    Third dimention acummulates the area of absulute value of difference between asset prices. It is an intrinsic value of the option.

    Args:
        parameters:
            Specifies parameters of the process
    
    Attributes:
        init_state: np.array([1.0, 1.0, 0.0])
            Value the process starts with
    
    """

    def __init__(self,
                 parameters : ProcessParams):
        self.params = parameters
        self.init_state = np.array([1.0, 1.0, 0.0])

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
        new_state = np.empty_like(old_state, dtype= float)
        #GBM evolution for the first asset
        new_state[:, 0] = old_state[:, 0] + self.params.r * old_state[:, 0] * dt + self.params.sigma_1 * old_state[:, 0] * dW[:, 0]
        #GBM evolution fot the second asset
        new_state[:, 1] = old_state[:, 1] + self.params.r * old_state[:, 1] * dt + self.params.sigma_2 * old_state[:, 1] * dW[:, 1]
        #evolution of the intrinsic value
        new_state[:, 2] = old_state[:, 2] + abs(new_state[:, 0] - new_state[:, 1]) * dt
        return new_state

    def noise(self,
              dt : float,
              n_sim : int,
              ) -> np.ndarray:
        
        """
        Used for evaluating the one step increment of the noise driving the process.
        Uses Cholesky decomposition to obtain desired correlation between the browanian motions.

        Args:
            dt:
                Length of the time interval.

            n_sim:
                Number of paths we simulate.

        Returns:
            dW increment of the process.

        """ 
        #Independent increments
        dW1 = np.random.normal(0, np.sqrt(dt), n_sim)
        dW2 = np.random.normal(0, np.sqrt(dt), n_sim)

        #Cholesky decomposition
        dW3 = self.params.rho * dW1 + np.sqrt(1 - self.params.rho ** 2) * dW2
        return np.array((dW1, dW3)).T
    