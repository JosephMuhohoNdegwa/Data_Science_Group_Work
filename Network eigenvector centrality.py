"""Rank network nodes by eigenvector-based importance."""

import numpy as np


# Adjacency matrix for the modified network.
# Node order: A, B, C, D.
adjacency = np.array(
    [
        [0.0, 1.0, 1.0, 1.0],
        [1.0, 0.0, 1.0, 1.0],
        [1.0, 1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0, 0.0],
    ]
)

# Calculate eigenvalues and eigenvectors.
eigenvalues, eigenvectors = np.linalg.eig(adjacency)

# Find the dominant eigenvalue and its corresponding eigenvector.
index = np.argmax(np.real(eigenvalues))
dominant_value = np.real(eigenvalues[index])
dominant_vector = np.abs(np.real(eigenvectors[:, index]))

# Normalize the vector so node scores sum to one.
centrality = dominant_vector / dominant_vector.sum()
nodes = ["A", "B", "C", "D"]

print("Dominant eigenvalue:", dominant_value)
print("Eigenvector-based importance:")

for node, score in zip(nodes, centrality):
    print(f"{node}: {score:.4f}")

# Verify A v = lambda v using the corresponding eigenvector.
vector = np.real(eigenvectors[:, index])
print(
    "Verification error:",
    np.linalg.norm(adjacency @ vector - dominant_value * vector),
)
