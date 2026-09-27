import matplotlib.pyplot as plt
import numpy
import pandas as pd
from sde_simulator.sde_engine import SDESimulator
from sde_simulator.option_params import OptionParams
from option.put.payoff import Payoff
import numpy as np

class Visualizer:
      """
      Helper class containing visualize() method. 
      """
      @staticmethod
      def visualize(stock : pd.Series,
                    date_idx : pd.DatetimeIndex,
                    simulator : SDESimulator,
                    K : float,
                    t_back : float,
                    T : float,
                    save : bool = True):
            """
            Generates a chart presenting historical option prices and their simulated future trajectories.
            Displays option value at terminal time and present the area accumulated between the assets.

            Args:
                  stock:
                        Daily historical prices of the asset.
                  date_idx:
                        Dates in which the asset prices were recorded.
                  simulator:
                        Simulates the future asseet trajectory.
                  t_back:
                        How much of past data to display (in yeasrs).
                  T:
                        Terminal time of the opton.
                  Save:
                        Boolean flag if the chart should be saved to a file.

            """
            #initialization of the simulator
            n_intervals = round(T * 365)
            opt_par = OptionParams(0, T, 1, n_intervals)

            #evalauation of the trajectory
            fut_path = simulator.paths(opt_par)

            #the terminal time payoff
            payoff_value = np.maximum(K - fut_path[-1], 0)

            #preparing simulated path to plot

            fut_idx = pd.date_range(start=date_idx[-1],
                                periods = n_intervals + 1,
                                freq="D")
            
            future_df = pd.DataFrame(data = {"price":fut_path[:, 0, 0]},
                                     index = fut_idx)

            fig, ax = plt.subplots()

            #preparing historical data to plot 
            periods_back = round(t_back * 365) 
            past_data = pd.DataFrame({"price":stock.values},
                                      index = date_idx)

      
            past_data = past_data.iloc[-periods_back:]
            past_idx = date_idx[-periods_back:]

            ax.plot(past_idx, past_data["price"], label="CocaCola")
            ax.plot(future_df.index, future_df["price"], label="sim CocaCola")

            ax.axvline(date_idx[-1], linestyle="--", color="black")
            ax.axhline(K, linestyle="--", color="red", label="Strike price")

            final_date = future_df.index[-1]
            final_price = future_df["price"].iloc[-1]
          
            if final_price < K:
              ax.vlines(x=final_date, ymin=final_price, ymax=K, 
                        color='darkgreen', linestyle=':', linewidth=2, 
                        label="Intrinsic Value Gap")

            ax.grid(True)
            ax.set_xlabel("date")
            ax.set_ylabel("Stock price")
            ax.set_title(f"Payoff = {round(payoff_value.item(), 5)} USD")
            ax.legend()

            if save == True:
                  plt.savefig('outputs/put_fig')

            plt.close(fig)
            return fig 
      

