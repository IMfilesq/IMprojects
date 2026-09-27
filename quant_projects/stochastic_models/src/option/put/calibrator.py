from option.put.process_params import ProcessParams
import pandas as pd
import numpy as np

class Calibrator:
    """
    Utility class for estimating parameters of the process used for pricing.
    """
    @staticmethod
    def calibrate(stock : pd.Series,
                  window : int,
                  r : float) -> ProcessParams:
        """
        Estimates parameters from historical asset prices.

        Args:
            stock:
                Historical daily price series for the asset.
                Should be in chrononological order, with the most recent price at the end of the series.
            window:
                Number of most recent observations used for calibration.
            r:
                Annualized risk-free interest rate expressed as a decimal.

        Returns:
            ProcessParams object

        """ 

        log_ret = np.log(stock/ stock.shift(1))[-window:]
        sigma = log_ret.std()*np.sqrt(252)
        return ProcessParams(stock.iloc[-1], r, sigma) 
    


    
