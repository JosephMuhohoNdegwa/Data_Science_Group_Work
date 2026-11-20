import timeit

import numpy as np


# Generate one million simulated network-delay readings.
rng = np.random.default_rng(42)
latency_ms = rng.uniform(5, 250, 1_000_000)


# Method 1: use a loop.
def loop_version():
    squared = []

    for value in latency_ms:
        seconds = value / 1000.0
        squared.append(seconds**2)

    return squared


# Method 2: use NumPy vectorization.
def vectorized_version():
    seconds = latency_ms / 1000.0
    return seconds**2


# Measure execution times.
loop_time = timeit.timeit(loop_version, number=1)
vector_time = timeit.timeit(vectorized_version, number=3) / 3

# Calculate and display the results.
result = vectorized_version()
print("First five squared latency values:", result[:5])
print(f"Loop time: {loop_time:.4f} s")
print(f"Vectorized time: {vector_time:.4f} s")
print(f"Approximate speed-up: {loop_time / vector_time:.1f}x")
