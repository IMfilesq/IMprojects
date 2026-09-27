import pandas as pd
from option.put.calibrator import Calibrator
from option.put.process import Process
from option.put.payoff import Payoff
from option.put.discount import Discount
from pricer.american_pricer import AmericanPricer
from pricer.european_pricer import EuropeanPricer
from sde_simulator.option_params import OptionParams
from sde_simulator.sde_engine import SDESimulator


class PutOption:
    """
    Evaluates the price of a put option.

    Args:
        stock:
            Historical daily prices of the asset. Should account for splits and cannot contain Nulls.
            Should be in chronological order, with the most recent price at the end of the series.
        Window:
            Number of most recent data to infer parameters from.
        r:
            Interest rate.
        K:
            Strike price of the option.

    """
    def __init__(self,
                 stock: pd.Series,
                 window: int,
                 r: float,
                 K: float):
        self.stock = stock
        proc_par = Calibrator.calibrate(stock, window, r)
        proc = Process(proc_par)
        self.simulator = SDESimulator(proc.init_state,
                                 proc.noise,
                                 proc.state_update)
        pay = Payoff(proc_par, K)
        amer_pay = pay.pathwise
        euro_pay = pay.terminal
        dis = Discount(proc_par)
        amer_dis = dis.pathwise
        euro_dis = dis.terminal

        self.ap = AmericanPricer(self.simulator,
                                    amer_pay,
                                    amer_dis).price
        
        self.ep = EuropeanPricer(self.simulator,
                                    euro_pay,
                                    euro_dis).price
        
    def american_price(self,
                        T : float,
                        n_sim : int,
                        n_intervals : int):
        """
        Evaluates the american price of an area spread option via Longstaff-Schwartz alghoritm.
        
        Args:
            T:
                Terminal time.
            n_sim
                Number of simulations.
            n_intervals:
                Number of time-steps.

        """
        opt_par = OptionParams(0, T, n_sim, n_intervals)
        price = self.ap(opt_par)
        return price
    
    def european_price(self,
                        T : float,
                        n_sim : int,
                        n_intervals : int):
        
        """
        Evaluates the american price of an area spread option via monte carlo simultion.
        
        Args:
            T:
                Terminal time.
            n_sim
                Number of simulations.
            n_intervals:
                Number of time-steps.

        """
        
        opt_par = OptionParams(0, T, n_sim, n_intervals)
        price = self.ep(opt_par)
        return price
    