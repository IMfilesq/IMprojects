from dataclasses import dataclass

@dataclass(frozen=True)
class OptionParams:
    """
    Keeps option parameters.

    Attributes:
        t_0 : Starting time.
        T: Terminal time.
        n_sim : Number of paths to simulate.
        n_intervals : Number of time steps in Euler's algorithm.
    """
    t_0 : float
    T : float
    n_sim : int
    n_intervals : int