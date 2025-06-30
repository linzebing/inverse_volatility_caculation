import numpy as np
import math

# Mock data from the test
prices = [
    100.0,  # 2020-02-15
    98.5,   # 2020-02-14
    99.2,   # 2020-02-13
    97.8,   # 2020-02-12
    98.1,   # 2020-02-11
    99.5,   # 2020-02-10
    100.2,  # 2020-02-09
    99.8,   # 2020-02-08
    100.5,  # 2020-02-07
    101.2,  # 2020-02-06
    100.8,  # 2020-02-05
    101.5,  # 2020-02-04
    102.0,  # 2020-02-03
    101.8,  # 2020-02-02
    102.2,  # 2020-02-01
    101.9,  # 2020-01-31
    102.5,  # 2020-01-30
    103.0,  # 2020-01-29
    102.8,  # 2020-01-28
    103.2,  # 2020-01-27
    103.5   # 2020-01-26
]

# Calculate log returns
log_returns = []
for i in range(20):  # window_size = 20
    log_returns.append(math.log(prices[i] / prices[i+1]))

# Calculate volatility
volatility = np.std(log_returns, ddof=1) * np.sqrt(252)  # annualized volatility

# Calculate performance (prices[0] / prices[window_size] - 1.0)
performance = prices[0] / prices[20] - 1.0

print(f"Calculated volatility: {volatility:.6f}")
print(f"Performance: {performance:.6f}") 