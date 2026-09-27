from option.put.visualizer import Visualizer
import pandas as pd
from option.put.calibrator import Calibrator
from option.put.process import Process
from sde_simulator.sde_engine import SDESimulator


KO = pd.read_csv("tests/KO_stock.csv")

proc_par = Calibrator.calibrate(KO["Open"].iloc[::-1], 30, 0.1)
proc = Process(proc_par)
simulator = SDESimulator(proc.init_state, proc.noise, proc.state_update)
Visualizer.visualize(KO["Open"].iloc[::-1],
                     pd.DatetimeIndex(KO["Date"].iloc[::-1]),
                     simulator,
                     80,
                     0.5,
                     0.5)

