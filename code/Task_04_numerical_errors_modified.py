import numpy as np


# Floating-point comparison
calculated = 0.1 + 0.2
expected = 0.3

print("Calculated value:", calculated)
print("Exact comparison:", calculated == expected)
print("Approximate comparison:", np.isclose(calculated, expected))

# Absolute and relative error
true_value = np.sqrt(5)
approx_value = 2.236

absolute_error = abs(true_value - approx_value)
relative_error = absolute_error / abs(true_value)

print("\nAbsolute error:", round(absolute_error, 8))
print("Relative error:", round(relative_error * 100, 6), "%")

# Comparing unstable and stable calculations
for x in [1e-3, 1e-6, 1e-9]:
    direct = (np.sqrt(1 + x) - 1) / x
    stable = 1 / (np.sqrt(1 + x) + 1)

    print(f"\nx = {x}")
    print("Direct result:", direct)
    print("Stable result:", stable)
