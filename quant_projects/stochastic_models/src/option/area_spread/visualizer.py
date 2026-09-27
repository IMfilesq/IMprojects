import matplotlib.pyplot as plt
import pandas as pd
from sde_simulator.sde_engine import SDESimulator
from sde_simulator.option_params import OptionParams

class Visualizer:
      """
      Helper class containing visualize() method. 
      """
      @staticmethod
      def visualize(stock_1 : pd.Series,
                    stock_2 : pd.Series,
                    date_idx : pd.DatetimeIndex,
                    simulator : SDESimulator,
                    t_back : float,
                    T : float,
                    save : bool = True):
            """
            Generates a chart presenting historical option prices and their simulated future trajectories.
            Displays option value at terminal time and present the area accumulated between the assets.

            Args:
                  stock_1:
                        Daily historical prices of the first asset.
                  stock_2:
                        Daily historical prices of the second asset.
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
            area = fut_path[-1, 0, 2]

            #preparing simulated path to plot

            fut_idx = pd.date_range(start=date_idx[-1],
                                periods = n_intervals + 1,
                                freq="D")
            
            future_df = pd.DataFrame(data = {"price_1":fut_path[:, 0, 0],
                                             "price_2":fut_path[:, 0, 1]},
                                     index = fut_idx)

            fig, ax = plt.subplots()

            #preparing historical data to plot 
            periods_back = round(t_back * 365) 
            past_data = pd.DataFrame({"price_1":stock_1.values,
                                      "price_2":stock_2.values},
                                      index = date_idx)

      
            past_data = past_data.iloc[-periods_back:]
            past_idx = date_idx[-periods_back:]

            ax.plot(past_idx, past_data["price_1"]/past_data["price_1"].iloc[-1], label="CocaCola")
            ax.plot(past_idx, past_data["price_2"]/past_data["price_2"].iloc[-1], label="Pepsi")
            ax.plot(future_df.index, future_df["price_1"], label="sim CocaCola")
            ax.plot(future_df.index, future_df["price_2"], label="sim Pepsi")

            ax.fill_between(future_df.index, future_df["price_1"], future_df["price_2"], alpha=0.4)
            ax.axvline(date_idx[-1], linestyle="--", color="black")
            ax.grid(True)
            ax.set_xlabel("date")
            ax.set_ylabel("normalized value")
            ax.set_title(f"Area = {round(area, 5)} USD")
            ax.legend()

            if save == True:
                  plt.savefig('outputs/area_option_fig')

            plt.close(fig)
            return fig 
      

