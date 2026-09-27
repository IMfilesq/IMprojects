import numpy as np
from option.area_spread.process_params import ProcessParams
from sde_simulator.option_params import OptionParams
import scipy.stats as st

class Controll:
    def __init__(self, par: ProcessParams):
        self.par = par

    @staticmethod
    def payoff(S1, S2):
        return abs(S1 - S2)

    def expected_spread_payoff(self, t, T):
        sigma = np.sqrt(self.par.sigma_1**2 + self.par.sigma_2**2 - 2*self.par.rho*self.par.sigma_1*self.par.sigma_2)
        d1 = sigma**2/2*(T - t)/(sigma*np.sqrt(T - t))
        d2 = d1 - sigma*np.sqrt(T - t)
        return np.exp(self.par.r*(T - t))*2*(st.norm.cdf(d1) - st.norm.cdf(d2))