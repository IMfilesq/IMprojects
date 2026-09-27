import pandas as pd
from option.put.put import PutOption


def price_put():
    KO = pd.read_csv("data/KO_stock.csv")
    P = PutOption(KO["Open"][::-1], 30, 0.1, 100)
    ap = P.american_price(1, 100000, 100)
    ep = P.european_price(1, 100000, 100)

    print("One year put option price. Evaluated using 100 time steps and 100K simulated paths.")
    print(f"American: {ap}")
    print(f"European: {ep}")

if __name__ == "__main__":
    price_put()


