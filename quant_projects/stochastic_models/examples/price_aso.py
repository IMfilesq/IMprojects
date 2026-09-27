import pandas as pd
from option.area_spread.area_spread import AreaSpreadOption

def price_aso() -> None:
    KO = pd.read_csv("data/KO_stock.csv")
    PEP = pd.read_csv("data/PEP_stock.csv")

    ASO = AreaSpreadOption(KO["Open"][::-1], PEP["Open"][::-1], 30, 0.1)
    ap = ASO.american_price(1, 100000, 100)
    ep = ASO.european_price(1, 100000, 100)

    print("One year ASO option price. Evaluated using 100 time steps and 100K simulated paths.")
    print(f"American: {ap}")
    print(f"European: {ep}")

if __name__ == "__main__":
    price_aso()