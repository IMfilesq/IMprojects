import pandas as pd
from option.area_spread.var_red_area_spread import AreaSpreadOption

KO = pd.read_csv("tests/KO_stock.csv")
PEP = pd.read_csv("tests/PEP_stock.csv")

ASO = AreaSpreadOption(KO["Open"][::-1], PEP["Open"][::-1], 30, 0.1)
ap = ASO.american_price(1, 100000, 100)
ep = ASO.european_price(1, 100000, 100)

print("One year ASO option price. Evaluated using 100 time steps and 100K simulated paths.")
print(f"American: {ap}")
print(f"European: {ep}")


