import numpy as np
import matplotlib.pyplot as plt

# Fish population growth using Euler's Method

P_initial = 100  # Initial fish population
growth_rate = 0.2  # Growth rate per year
h = 1.0  # Step size: 1 year
end_time = 10  # Simulate for 10 years

# Create time values
time = np.arange(0, end_time + h, h)

# Create an array to store population values
population = np.zeros(len(time))
population[0] = P_initial

# Euler's Method
for i in range(len(time) - 1):
    rate_of_change = growth_rate * population[i]
    population[i + 1] = population[i] + h * rate_of_change

# Display results
print("Fish Population Growth")
print("----------------------")

for i in range(len(time)):
    print(f"Year {time[i]:.0f}: {population[i]:.2f} fish")

# Plot the population growth
plt.plot(time, population, marker="o")
plt.xlabel("Time (years)")
plt.ylabel("Fish population")
plt.title("Fish Population Growth Using Euler's Method")
plt.grid(True)
plt.show()
