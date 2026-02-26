#Greeks implementation

BlackScholesGreeks=function(S, X, time, r, sigma){
  d1 = (log(S/X) + (r + sigma^2/2)*time)/(sigma*sqrt(time))
  d2 = d1 - sigma*sqrt(time)
  CE = S*pnorm(d1) - X*exp(-r*time)*pnorm(d2)
  PE = X*exp(-r*time)*pnorm(-d2) - S*pnorm(-d1)
  DeltaCall = pnorm(d1)
  DeltaPut = pnorm(-d1)
  Gamma = pnorm(d1)/(S*sigma*sqrt(time))
  Vega = S*pnorm(d1)*sqrt(time)
  return(c(CE, PE, DeltaCall, DeltaPut, Gamma, Vega))
}

BlackScholesGreeks(S=80, X=100, time=2, r=0.1, sigma=0.05)

#analytical pricing in binomial model

CRRPrice<-function(TypeFlag, S, X, u, d, r, n){
  k = 0:n
  m = m = min(k[S*(1+u)^k*(1+d)^(n-k) >= X])
  p_star = (r-d)/(u-d)
  q = p_star*(1+u)/(1+r)
  if(TypeFlag == "ce"){
      val = S*(1 - pbinom(m - 1,n,q)) - X*(1+r)^(-n)*(1 - pbinom(m-1,n,p_star))
  }
  else{
    val = -S*pbinom(m-1,n,q) + X*(1+r)^(-n)*pbinom(m-1,n,p_star)
  }
  return(val)
}

CRRPrice(TypeFlag = "pe", S=80, X=80, u=0.1, d=-0.05, r=0.05, n=2) 

#tree based binomial option pricing

BinomialTreeOption<-function(TypeFlag, S, X, d, r, u, n){
  tree = matrix(nrow = n+1, ncol = n+1)
  for(time in 1:(n+1)){
    for(up_moves in 1:(time))
      tree[up_moves, time] = S*(1+u)^(up_moves-1)*(1+d)^(time - up_moves)
  }
  p_star = (r-d)/(u-d)
  q_star = 1- p_star
  if(TypeFlag == "ce"){
    payoff = function(s) pmax(s - X, 0)
    tree[,n+1] = payoff(tree[,n+1])
    for(time in n:1){
      for(up_move in time:1){
        tree[up_move, time] = 1/(1+r)*(p_star*tree[up_move+1, time + 1] + q_star*tree[up_move, time + 1])
      }
    }
  }
  if(TypeFlag == "pe"){
    payoff = function(s) pmax(X-s, 0)
    tree[,n+1] = payoff(tree[,n+1])
    for(time in n:1){
      for(up_move in time:1){
        tree[up_move, time] = 1/(1+r)*(p_star*tree[up_move+1, time + 1] + q_star*tree[up_move, time + 1])
      }
    }
  }
  if(TypeFlag == "ca"){
    payoff = function(s) pmax(s - X, 0)
    tree[,n+1] = payoff(tree[,n+1])
    for(time in n:1){
      for(up_move in time:1){
        current = payoff(tree[up_move, time])
        weighted = 1/(1+r)*(p_star*tree[up_move+1, time + 1] + q_star*tree[up_move, time + 1])
        tree[up_move, time] = max(current, weighted)
      }
    }
  }
  if(TypeFlag == "pa"){
    payoff = function(s) pmax(X - s, 0)
    tree[,n+1] = payoff(tree[,n+1])
    for(time in n:1){
      for(up_move in time:1){
        current = payoff(tree[up_move, time])
        weighted = 1/(1+r)*(p_star*tree[up_move+1, time + 1] + q_star*tree[up_move, time + 1])
        tree[up_move, time] = max(current, weighted)
      }
    }
  }
  return(tree)
}

BinomialTreeOption(TypeFlag = "pe", S=80, X=80, u=0.1, d=-0.05, r=0.05, n=2)[1]


#tree visualization 

library(ggplot2)


BinomialTreePlot <- function(Tree){
  Tree = signif(Tree, 2)
  n = nrow(Tree)
  vals = c()
  x = c()
  y = c()
  start = 0
  for(i in 1:n){
    for(j in 1:i){
      vals = c(vals, Tree[j,i])
      x = c(x, i)
      y = c(y, start - 2*(j-1))
    }
    start = start + 1
  }
  
  df <- data.frame(x = x, y = y, label = vals)
  
  edges <- data.frame(x = numeric(0), y = numeric(0), xend = numeric(0), yend = numeric(0))
  start2 <- 0
  for(i in 1:(n-1)){
    for(j in 1:i){
      x0 <- i
      y0 <- start2 - 2*(j-1)
      x1 <- i + 1
      y1_up <- start2 + 1 - 2*(j-1)
      y1_down <- start2 + 1 - 2*j
      edges <- rbind(edges, data.frame(x = x0, y = y0, xend = x1, yend = y1_up))
      edges <- rbind(edges, data.frame(x = x0, y = y0, xend = x1, yend = y1_down))
    }
    start2 <- start2 + 1
  }
  
  p <- ggplot(df, aes(x = x, y = y)) +
    geom_point(color = "blue", size = 3) +
    geom_text(aes(label = label), vjust = -0.5, color = "black") +
    geom_segment(data = edges, aes(x = x, y = y, xend = xend, yend = yend), color = "black") +
    xlab("interval") +
    ylab("") +
    theme(
      axis.title.y = element_blank(),
      axis.text.y = element_blank(),
      axis.ticks.y = element_blank()
    ) +
    ggtitle("Option prices in binomial model")
  
  return(p)
}

t = BinomialTreeOption(TypeFlag = "pe", S=80, X=80, u=0.1, d=-0.05, r=0.05, n=2)
BinomialTreePlot(t)

#Simulating brownian paths

BrownianMotion = function(N, n, t, mu, sigma, S){
  m = matrix(0, nrow = N, ncol = n + 1)
  m[,1] = S
  for(i in 1:N){
    for(k in 1:n){
      m[i, k+1] = m[i, k] + mu * t/n +sigma * sqrt(t/n) * rnorm(1)
    }
  }
  return(m)
}
BrownianMotion(2, 10, 10, 1, 2, 0)

#monte carlo options pricing from brownian paths 

MC.euro=function(TypeFlag=c("call","put"),t,r,sigma,S,X,N=500,n=100){
  TypeFlag = match.arg(TypeFlag)
  prices = numeric(N)
  for(path in 1:N){
    times = (1:n) * (t/n)
    increments = rnorm(n, 0, sqrt(t/n))
    brownian_path = cumsum(increments)
    geom_path = S*exp((r-1/2*sigma^2)*times + sigma*brownian_path)
    if(TypeFlag == "call"){
      prices[path] = max(geom_path[n] - X, 0)
    }
    else{
      prices[path] = max(X - geom_path[n], 0)
    }
  }
  option_val = exp(-r*t)*mean(prices)
  return(option_val)
}

MC.euro("call", 2, 0.1, 0.05, 80, 100, 100000)

BlackScholesGreeks(S=80, X=100, time=2, r=0.1, sigma=0.05)[1]
