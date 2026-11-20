import numpy as np


# Number of Type A and Type B servers
A = np.array(
    [
        [4.0, 2.0],
        [8.0, 12.0],
    ]
)
b = np.array([24.0, 72.0])

# Solve the equations
solution = np.linalg.solve(A, b)

# Display the answers
print("Type A servers:", solution[0])
print("Type B servers:", solution[1])

# Verify the solution
print("Verification:", A @ solution)
