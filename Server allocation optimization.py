import numpy as np
from scipy.optimize import minimize


# x and y are the capacity units allocated to Type A and Type B servers.
# Cost per unit: A = 12, B = 18
# Capacity per unit: A = 100, B = 170
# Required total capacity: at least 1500
cost_a = 12
cost_b = 18
capacity_a = 100
capacity_b = 170
required_capacity = 1500


def cost(z):
    x, y = z
    return cost_a * x + cost_b * y


def capacity_constraint(z):
    x, y = z
    return capacity_a * x + capacity_b * y - required_capacity


constraints = {"type": "ineq", "fun": capacity_constraint}
bounds = [(0, None), (0, None)]
solution = minimize(
    cost,
    x0=[5, 3],
    method="SLSQP",
    bounds=bounds,
    constraints=constraints,
)

print("Optimization success:", solution.success)
if solution.success:
    x, y = solution.x
    total_capacity = capacity_a * x + capacity_b * y
    print(f"Type A allocation: {x:.3f}")
    print(f"Type B allocation: {y:.3f}")
    print(f"Total capacity: {total_capacity:.2f}")
    print(f"Minimum planning cost: {solution.fun:.2f}")
else:
    print("Solver message:", solution.message)

# Search feasible whole-server allocations for the least-cost combination.
best_integer = None
max_a = int(np.ceil(required_capacity / capacity_a))
max_b = int(np.ceil(required_capacity / capacity_b))

for a in range(max_a + 1):
    for b in range(max_b + 1):
        capacity = capacity_a * a + capacity_b * b
        if capacity >= required_capacity:
            total_cost = cost_a * a + cost_b * b
            if best_integer is None or total_cost < best_integer[0]:
                best_integer = (total_cost, a, b, capacity)

print("Best integer solution (cost, Type A, Type B, capacity):", best_integer)
