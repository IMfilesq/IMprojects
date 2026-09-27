from dataclasses import dataclass

@dataclass(frozen=True)
class ProcessParams:
    """
    Keeps model parameters that specify evolution of the process we simulate.

    Attributes:
        sigma_1: Volatility of the first asset
        sigma_2: Volatility of the second asset
        rho : Correlation between the two assets
        r : Interest rate
    """
    sigma_1 : float
    sigma_2 : float
    rho : float
    r : float