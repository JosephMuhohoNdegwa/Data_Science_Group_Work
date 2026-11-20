import numpy as np


# Four corners of a square; each row is an [x, y] coordinate.
points = np.array(
    [
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0],
    ]
)

angle = np.deg2rad(45)

rotation = np.array(
    [
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)],
    ]
)

scale = np.array(
    [
        [2.0, 0.0],
        [0.0, 1.5],
    ]
)

# Apply scaling, then rotation.
transformation = rotation @ scale

# Row-vector coordinates multiply the transformation transpose.
transformed_points = points @ transformation.T

print("Original square coordinates:\n", points)
print("\nRotation matrix:\n", rotation)
print("\nScaling matrix:\n", scale)
print("\nCombined transformation:\n", transformation)
print("\nTransformed square coordinates:\n", transformed_points)
print("\nDeterminant:", np.linalg.det(transformation))
