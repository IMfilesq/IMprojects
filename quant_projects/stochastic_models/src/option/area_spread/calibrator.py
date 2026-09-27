import pandas as pd
import numpy as np
from option.area_spread.process_params import ProcessParams

class Calibrator:
    """
    Utility class for estimating parameters of the process used for pricing.
    """
    @staticmethod
    def calibrate(stock_1 : pd.Series,
                  stock_2 : pd.Series,
                  window : int,
                  r : float) -> ProcessParams:
        """
        Estimates parameters from historical asset prices.

        Args:
            stock_1:
                Historical daily price series for the first asset.

            stock_2:
                Historical daily price series for the second asset.

            window:
                Number of most recent observations used for calibration.
            r:
                Annualized risk-free interest rate expressed as a decimal.

        Returns:
            ProcessParams object

        """ 

        log_ret_1 = np.log(stock_1 / stock_1.shift(1))[-window:]
        log_ret_2 = np.log(stock_2 / stock_2.shift(1))[-window:]
        sigma_1 = log_ret_1.std()*np.sqrt(252)
        sigma_2 = log_ret_2.std()*np.sqrt(252)
        rho = log_ret_1[-window:].corr(log_ret_2[-window:])

        return ProcessParams(sigma_1, sigma_2, rho, r) 
