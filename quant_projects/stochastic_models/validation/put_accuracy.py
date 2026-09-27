from option.put_benchmark.put import Put as QuantLibPut
import pandas as pd
from option.put.process_params import ProcessParams
from option.put.process import Process
from option.put.payoff import Payoff
from option.put.discount import Discount
from pricer.american_pricer import AmericanPricer
from pricer.european_pricer import EuropeanPricer
from sde_simulator.option_params import OptionParams
from sde_simulator.sde_engine import SDESimulator

def validate_put() -> None:
    sigma = 0.5
    S0 = 100
    K = [50,75,100,125,150]
    T = 1
    r = 0.1

    euro_df = pd.DataFrame(index = K, columns = ["QuantLib", "MyPut"])
    amer_df = pd.DataFrame(index = K, columns = ["QuantLib", "MyPut"])

    for k in K:
        proc_par = ProcessParams(S0, r, sigma)
        proc = Process(proc_par)
        simulator = SDESimulator(proc.init_state,
                                proc.noise,
                                proc.state_update)

        pay = Payoff(proc_par, k)
        amer_pay = pay.pathwise
        euro_pay = pay.terminal
        dis = Discount(proc_par)
        amer_dis = dis.pathwise
        euro_dis = dis.terminal

        ap = AmericanPricer(simulator,
                            amer_pay,
                            amer_dis).price

        ep = EuropeanPricer(simulator,
                            euro_pay,
                            euro_dis).price
        opt_par = OptionParams(0, T, 100000, 100)
        euro_df.loc[k, "QuantLib"] = QuantLibPut.european_price(S0, k, T, r, sigma)
        euro_df.loc[k, "MyPut"] = ep(opt_par)
        amer_df.loc[k, "QuantLib"] = QuantLibPut.american_price(S0, k, T, r, sigma)
        amer_df.loc[k, "MyPut"] = ap(opt_par)

    print("Parameters used : (S0 = {}, r = {}, sigma = {}, T = {})".format(S0, r, sigma, T))
    print("Comparison of European put option prices:")
    print(euro_df)
    print("simulation parameters : (n_sim = {}, n_intervals = {})".format(opt_par.n_sim, opt_par.n_intervals))
    print("Grid 1000x1000)")
    print("Comparison of American put option prices:")
    print(amer_df)

if __name__ == "__main__":
    validate_put()
