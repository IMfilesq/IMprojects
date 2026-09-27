import pandas as pd
from option.area_spread.calibrator import Calibrator
from option.area_spread.process import Process
from option.area_spread.payoff import Payoff
from option.area_spread.discount import Discount
from pricer.american_pricer import AmericanPricer
from pricer.european_pricer import EuropeanPricer
from sde_simulator.option_params import OptionParams
from sde_simulator.sde_engine import SDESimulator


class AreaSpreadOption:
    """
    Evaluates the price of an area spread option.
    
    Args:
        stock_1:
            Historical daily prices of the first asset. Should account for splits and cannot contain Nulls.
        stock_2:
            Historical daily prices of the second asset. Should account for splits and cannot contain Nulls.
        Window:
            Number of most recent data to infer parameters from.
        r:
            Interest rate.

    """
    def __init__(self,
                 stock_1: pd.Series,
                 stock_2: pd.Series,
                 window: int,
                 r: float):
        self.stock_1 = stock_1
        self.stock_2 = stock_2
        proc_par = Calibrator.calibrate(stock_1, stock_2, window, r)
        proc = Process(proc_par)
        self.simulator = SDESimulator(proc.init_state,
                                 proc.noise,
                                 proc.state_update)
        pay = Payoff(proc_par)
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
    