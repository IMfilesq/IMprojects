"""
This file contains an implementation of binomial asset pricing model for a very general class of derrivatives.
"""


import numpy as np
import sys
from functools import lru_cache

class bin_model:
    def __init__(self, r, N, S_0, u, d):
            """
            :param r: one interval interest rate
            :param N: number of intervals, execution time
            :param S_0: initial stock price
            :param u: the value by which the stok move up, so that S*u corresponds to the stock price after it moved up
            :param d: the value by which the stok moves down, so that S*d corresponds to the stock price after it moved down

            this class also stores:
            - possible stock price paths, which are stored in self.stock_prices, a lower diagonal matrix
              self.stock_prices[i,j] is the stock price at time i, after j up moves
            - self.p, self.q - a risk neutral probabilities of up and down move

            """
            self.r = r
            self.N = N
            self.S_0 = S_0
            self.u = u
            self.d = d

            stock_prices = np.zeros((self.N + 1, self.N + 1))
            for time in range(self.N + 1):
                for up_move in range(time + 1):
                    stock_prices[time, up_move] = S_0*u**up_move*d**(time - up_move)
  
            self.stock_prices = stock_prices

            self.p = (1 + r - d)/(u - d)
            self.q = 1 - self.p

class option:
    """
    a general option class for future inheritange, it will use values stored in bin_model object
    """
    def __init__(self, bin_model):
        self.N = bin_model.N
        self.S = bin_model.stock_prices
        self.p = bin_model.p
        self.q = bin_model.q
        self.r = bin_model.r
    
class vanilla(option):
    """
    this is a general blueprint for non path dependent options, it requires only payoff function as an init argument
    """
    def __init__(self, bin_model, payoff_fun):
        super().__init__(bin_model)
        self.f = payoff_fun
    
    def replicate(self, value_formula, waste_formula):
        """
        This function returns all the posiible information regarding option prices, hedging, values and earlu exercise premiums
        :param value_formula: value_formula is a function that encodes the next option value in backward induction
        :param waste_formula: value_formula is a function that encodes the eary exercise premium backward induction
        """
        #these will store option payoffs, positions require for hedging, option values and early exercise premiums
        payoffs = np.zeros((self.N + 1, self.N + 1))
        deltas = np.zeros((self.N, self.N))
        values = np.zeros((self.N + 1, self.N + 1))
        waste = np.zeros((self.N, self.N))

        #we initialize option values as payoffs at time N
        for i in range(self.N+1):
            values[self.N, i] = self.f(self.S[self.N, i])

        payoffs[self.N, :] = values[self.N, :]

        # here is the core backward induction algorithm
        for i in reversed(range(self.N)):
            for j in range(i + 1):
                weighted = (1 / (1 + self.r))*(self.p*values[i + 1, j + 1] + self.q*values[i + 1, j])
                payoffs[i,j] = self.f(self.S[i,j])
                values[i,j] = value_formula(weighted, payoffs[i,j])
                deltas[i,j] = (values[i + 1, j + 1] - values[i + 1, j])/(self.S[i + 1, j + 1] - self.S[i + 1, j])
                waste[i,j] = waste_formula(weighted, payoffs[i,j])

        return (payoffs, deltas, values, waste)
    
    def price(self, value_formula):
        """this returns option value at time zero, price() is much faster and memory efficient than replicate """
        curr = np.zeros(self.N + 1)
        for i in range(self.N + 1):
            curr[i] = self.f(self.S[self.N, i])
        
        for i in reversed(range(self.N)):
            new = np.zeros(i + 1)
            for j in range(i + 1):
                weighted = (1 / (1 + self.r))*(self.p*curr[j + 1] + self.q*curr[j])
                new[j] = value_formula(weighted, self.f(self.S[i,j]))
            curr = new
        return curr[0]
    
     
class european_vanilla(vanilla):
    """" 
    uses the methods form vanilla class, but specifies value and waste formulas specific for european options
    """
    def __init__(self, bin_model, payoff_fun):
        super().__init__(bin_model, payoff_fun)
        self.value_formula = lambda x, y : x
        self.waste_formula = lambda x, y : 0

    def replicate(self):
        return(super().replicate(self.value_formula, self.waste_formula))
    
    def price(self):
        return(super().price(self.value_formula))
    

class american_vanilla(vanilla):
    """" 
    uses the methods form vanilla class, but specifies value and waste formulas specific for american options
    """
    def __init__(self, bin_model, payoff_fun):
        super().__init__(bin_model, payoff_fun)
        self.value_formula = lambda x, y : max(x, y)
        self.waste_formula = lambda x, y : self.value_formula(x,y) - x

    def replicate(self):
        return(super().replicate(self.value_formula, self.waste_formula))
    
    def price(self):
        return(super().price(self.value_formula))
    

class exotic(option):
    """
    this is the general engine for exotic options
    """

    def __init__(self, bin_model, payoff_fun, state_zero, state_formula, s_price):
        """
        :param bin_model: - binomial model object
        :param payoff_fun: function that speifies option payoff
        :param state_zero: the state tuple of stock at time zero (requires storing enough values to make derivative payoff a markov process)
        :param state_formula: a function that specifies future states, returns both as a tuple
        :param s_price: function that extracts stock price from state tuple
        """
        super().__init__(bin_model)
        self.f = payoff_fun
        self.state_zero = state_zero
        self.state_formula = state_formula
        self.s_price = s_price


    def tree(self, state_formula, state_zero):
        """
        this function creates the tree that stores possible states as a list of dicts,
        which map state to values connected to pricing and replicating such as "value", "payoff" and in future "delta" and "waste"
        it returns the whole data structure
        """
        tree = [{} for _ in range(self.N + 1)]
        tree[0][self.state_zero] = {"payoff":self.f(state_zero)}
        for i in range(1, self.N + 1):
            for state, _ in tree[i - 1].items():
                for next_scenario in state_formula(state):
                    tree[i][next_scenario] = {"payoff":self.f(next_scenario)}
                    if i == self.N:
                        tree[i][next_scenario]["value"] = tree[i][next_scenario]["payoff"]
        return tree

    def replicate(self, value_formula, waste_formula):
        """
        it performs backward induction adding all the missing values to tree
        it returns whole data structure
        """
        tree = self.tree(self.state_formula, self.state_zero)
        for i in reversed(range(self.N)):
            for state, _ in tree[i].items():
                next_u, next_d = self.state_formula(state)
                val_u = tree[i + 1][next_u]["value"]
                val_d = tree[i + 1][next_d]["value"]

                weighted = (1 / (1 + self.r))*(self.p*val_u + self.q*val_d)
                curr_node = tree[i][state]
                curr_payoff = curr_node["payoff"]
                curr_node["value"] = value_formula(weighted, curr_payoff)

                curr_node["delta"] = (val_u - val_d)/(self.s_price(next_u)- self.s_price(next_d))
                curr_node["waste"] = waste_formula(weighted, curr_payoff)
        return tree

    def price(self, value_formula):
        """
        This method is recursive equivalent of replicate(),
        it does not store values and returns option price at time zero
        """
        sys.setrecursionlimit(max(1000, self.N + 100)) 
        disc = 1 / (1 + self.r)

        @lru_cache(None)
        def get_value(time, state):
            if time == self.N:
                return self.f(state)
            next_u, next_d = self.state_formula(state)
            weighted = disc * (self.p * get_value(time + 1, next_u) + self.q * get_value(time + 1, next_d))
            curr_payoff = self.f(state)
            return value_formula(weighted, curr_payoff)

        return get_value(0, self.state_zero)
    


        

class european_exotic(exotic):
    """
    inherits from exotic, specifies value and early exercise premiums for european option backpropagation
    """

    def __init__(self, bin_model, payoff_fun, state_zero, state_formula, s_price):
        super().__init__(bin_model, payoff_fun, state_zero, state_formula, s_price)
        self.value_formula = lambda weighted, curr_payoff : weighted
        self.waste_formula = lambda weighted, curr_payoff : 0


    def replicate(self):
        return super().replicate(self.value_formula, self.waste_formula)
       
    def price(self):
        return super().price(self.value_formula)


class american_exotic(exotic):
    """
    inherits from exotic, specifies value and early exercise premiums for american option backpropagation 
    """

    def __init__(self, bin_model, payoff_fun, state_zero, state_formula, s_price):
        super().__init__(bin_model, payoff_fun, state_zero, state_formula, s_price)
        self.value_formula = lambda weighted, curr_payoff : max(weighted, curr_payoff)
        self.waste_formula = lambda weighted, curr_payoff : self.value_formula(weighted, curr_payoff) - weighted

    def replicate(self):
        return super().replicate(self.value_formula, self.waste_formula)
       
    def price(self):
        return super().price(self.value_formula)


#a example of how to use the code above for pricing asian option
b = bin_model(0.02, 10, 2, 2, 0.5)
asian = american_exotic(b,
                        lambda x : x[1]/x[2], (2, 2, 1),
                        lambda x : ((x[0]*b.u, x[1] + x[0]*b.u, x[2] + 1),(x[0]*b.d, x[1] + x[0]*b.d, x[2] + 1)),
                        lambda x: x[0])
asian.price()
asian.replicate()

