import numpy as np
from numpy.random import uniform, normal, exponential
import matplotlib.pyplot as plt
from math import sqrt, log, cos, pi

def dist_normal(u1, u2, mean, sd):
    x = sqrt(-2 * log(u1)) * cos(2 * pi * u2)
    return x * sd + mean

# new_values = [dist_normal(uniform(0, 1),uniform(0, 1),4,0.5) for i in range(100000)]
values = exponential(5, 1000)

plt.figure(figsize=(8,6))
# plt.hist(new_values, bins=100, alpha=0.5, label="Ours")

plt.xlabel("Values", size=14)
plt.ylabel("Count", size=14)
plt.title("Normal Comparison")
plt.plot(values, alpha=0.5, label="Numpy")
plt.savefig("graphs/normal_dist.png")
