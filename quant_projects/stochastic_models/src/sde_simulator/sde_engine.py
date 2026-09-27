import numpy as np
from typing import Callable
from .option_params import OptionParams

class SDESimulator:
    """
    Simulates trajectories of user defined stochastic process.

    Args:
        init_state:
            Value the process starts with
        noise:
            Function that returns noise (dW increment) of a process.
        state_update:
            Function thet returns next state of the process based on previous one.
    
    """
    def __init__(self,
                 init_state : np.ndarray,
                 noise : Callable,
                 state_update : Callable):
        
        self.noise = noise
        self.state_update = state_update
        self.init_state = init_state
        
    def paths(self,
             opt_par : OptionParams
             ) -> np.array:
        
        """
        Simulates the solution of SDE via Euler formula and optionaly keeps tracks of state variables.

        Args:
            opt_par:
                Specifies accuracy, time horizon and number of paths.

        Returns
        -------
        np.array object of size (opt_par.n_intervals + 1, opt_par.n_sim, opt_par.n_states)
        """
        T = opt_par.T
        t_0 = opt_par.t_0
        n_intervals = opt_par.n_intervals
        n_sim = opt_par.n_sim
        
        dt = (T - t_0) / n_intervals #dt is the length of interval in Euler alghoritm
        state = np.tile(self.init_state, (n_sim, 1)) #state is of the shape (n_states, n_sim)
        path_arr = np.empty(shape = (n_intervals + 1, n_sim, state.shape[1])) #will store paths, is of the shape (n_intervals + 1, n_sim, n_states)
        path_arr[0, :, :] = state #assigns initial states to the starting times
        for i in range(n_intervals): 
            t = t_0 + i * dt #keeps track of the current time of the process
            dW = self.noise(dt, n_sim) #generates noise to be used in the evaluation of the next state
            path_arr[i + 1, :, :] = self.state_update(path_arr[i, :, :].copy(), dt, dW) #evaluates the next state
        return path_arr
    
    def endpoints(self,
                 opt_par : OptionParams
                 ) -> np.ndarray:
        """ 
        Simulates the endpoints of SDE solution (at time opt_par.T) via Euler formula and optionaly keeps tracks of state variables.

        Args:
            opt_par:
                Specifies accuracy, time horizon and number of paths.

        Returns:
            np.array object of size (opt_par.n_sim, opt_par.n_states)
        """
        T = opt_par.T
        t_0 = opt_par.t_0
        n_intervals = opt_par.n_intervals
        n_sim = opt_par.n_sim

        dt = (T - t_0) / n_intervals #dt is the length of interval in Euler alghoritm
        state = np.tile(self.init_state, (n_sim, 1)) #state is of the shape (n_states, n_sim)
        for i in range(n_intervals): 
            t = t_0 + i * dt #keeps track of the current time of the process
            dW = self.noise(dt, n_sim) #generates noise to be used in the evaluation of the next state
            state = self.state_update(state, dt, dW) #evaluates the next state 
        return state
    
        

