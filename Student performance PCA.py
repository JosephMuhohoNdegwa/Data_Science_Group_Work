"""Analyze variation in student marks using covariance-matrix PCA."""

import numpy as np


# Columns represent Mathematics, Programming, Physics, and Statistics.
marks = np.array(
    [
        [80, 85, 75, 82],
        [70, 75, 65, 72],
        [90, 95, 85, 92],
        [60, 65, 55, 62],
        [85, 88, 80, 86],
        [75, 78, 70, 76],
        [95, 98, 90, 96],
        [65, 68, 60, 66],
    ],
    dtype=float,
)

subjects = ["Mathematics", "Programming", "Physics", "Statistics"]

# Calculate means, center the data, and compute the subject covariance matrix.
mean_marks = np.mean(marks, axis=0)
centered_data = marks - mean_marks
covariance_matrix = np.cov(centered_data, rowvar=False)

# Sort the covariance eigenpairs from greatest to least eigenvalue.
eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[indices]
eigenvectors = eigenvectors[:, indices]

dominant_eigenvalue = eigenvalues[0]
dominant_eigenvector = eigenvectors[:, 0]
explained_variance = dominant_eigenvalue / np.sum(eigenvalues) * 100

print("STUDENT PERFORMANCE ANALYSIS")

print("\nMean Marks:")
for subject, mean in zip(subjects, mean_marks):
    print(f"{subject}: {mean:.2f}")

print("\nCovariance Matrix:")
print(np.round(covariance_matrix, 2))

print("\nEigenvalues:")
print(np.round(eigenvalues, 4))

print("\nDominant Eigenvalue:")
print(round(dominant_eigenvalue, 4))

print("\nDominant Eigenvector:")
for subject, value in zip(subjects, dominant_eigenvector):
    print(f"{subject}: {value:.4f}")

print("\nPercentage of Variation Explained:")
print(f"{explained_variance:.2f}%")

# Verify that the leading eigenpair satisfies the covariance eigenvalue equation.
verification = np.linalg.norm(
    covariance_matrix @ dominant_eigenvector
    - dominant_eigenvalue * dominant_eigenvector
)

print("\nVerification Error:")
print(f"{verification:.10f}")
