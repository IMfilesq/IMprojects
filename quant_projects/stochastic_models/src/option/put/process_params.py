from dataclasses import dataclass

@dataclass
class ProcessParams:
    """Class for storing parameters of the process."""
    S0: float
    r: float
    sigma: float