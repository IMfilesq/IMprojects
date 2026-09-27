from option.area_spread.visualizer import Visualizer
import pandas as pd
from option.area_spread.calibrator import Calibrator
from option.area_spread.process import Process
from sde_simulator.sde_engine import SDESimulator

KO = pd.read_csv("tests/KO_stock.csv")
PEP = pd.read_csv("tests/PEP_stock.csv")

df = pd.DataFrame(KO, PEP)


proc_par = Calibrator.calibrate(KO["Open"].iloc[::-1], PEP["Open"].iloc[::-1], 30, 0.1)
proc = Process(proc_par)
simulator = SDESimulator(proc.init_state, proc.noise, proc.state_update)
Visualizer.visualize(KO["Open"].iloc[::-1],
                     PEP["Open"].iloc[::-1],
                     pd.DatetimeIndex(KO["Date"].iloc[::-1]),
                     simulator,
                     0.5,
                     0.5)

