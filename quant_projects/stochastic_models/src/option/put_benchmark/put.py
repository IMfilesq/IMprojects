import numpy as np
import QuantLib as ql


class Put:
    """
    Helper class to evaluate the price of a put option using QuantLib.
    """

    @staticmethod
    def american_price(S0: float,
                       K: float,
                       T: float,
                       r: float,
                       sigma: float) -> float:
        """ 
        Evaluates the price of an American put option using QuantLib's finite difference engine.

        Args:
            S0:
                Current price of the underlying asset.
            K:
                Strike price of the option.
            T:
                Time to maturity in years.
            r:
                Annualized risk-free interest rate expressed as a decimal.
            sigma:
                Annualized volatility of the asset's returns expressed as a decimal.
        Returns:
            Price of the American put option.
        """

        # 1. Date setup
        today = ql.Date().todaysDate()
        ql.Settings.instance().evaluationDate = today
        
        # Convert T (years) to days for QuantLib Date arithmetic
        maturity = today + int(T * 365)
        day_count = ql.Actual365Fixed()
        calendar = ql.NullCalendar()

        # 2. Market Data handles
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(S0))
        rate_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, r, day_count))
        div_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, day_count)) 
        vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, sigma, day_count))
        
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, div_ts, rate_ts, vol_ts)

        # 3. Option Definition
        payoff = ql.PlainVanillaPayoff(ql.Option.Put, K)
        exercise = ql.AmericanExercise(today, maturity)
        option = ql.VanillaOption(payoff, exercise)

        # 4. Engine Setup (Note: arguments must be positional-only)
        engine = ql.FdBlackScholesVanillaEngine(bsm_process, 1000, 1000)
        option.setPricingEngine(engine)

        return option.NPV()
    
    @staticmethod
    def european_price(S0: float,
                       K: float,
                       T: float,
                       r: float,
                       sigma: float) -> float:
        """
        Evaluates the price of a European put option using QuantLib's analytical Black-Scholes-Merton engine.
        Args:
            S0: 
                Current price of the underlying asset.
            K:
                Strike price of the option.
            T:
                Time to maturity in years.
            r:
                Annualized risk-free interest rate expressed as a decimal.
            sigma:
                Annualized volatility of the asset's returns expressed as a decimal.
        Returns:
            Price of the European put option.

        """
        # 1. Date setup
        today = ql.Date().todaysDate()
        ql.Settings.instance().evaluationDate = today
        
        # Convert T (years) to days for QuantLib Date arithmetic
        maturity = today + int(T * 365)
        day_count = ql.Actual365Fixed()
        calendar = ql.NullCalendar()

        # 2. Market Data handles
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(S0))
        rate_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, r, day_count))
        div_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, day_count)) # 0% dividend yield
        vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, sigma, day_count))
        
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, div_ts, rate_ts, vol_ts)

        # 3. Option Definition
        payoff = ql.PlainVanillaPayoff(ql.Option.Put, K)
        exercise = ql.EuropeanExercise(maturity)
        option = ql.VanillaOption(payoff, exercise)

        # 4. Engine Setup (Exact Analytical Black-Scholes-Merton)
        engine = ql.AnalyticEuropeanEngine(bsm_process)
        option.setPricingEngine(engine)

        return option.NPV()
