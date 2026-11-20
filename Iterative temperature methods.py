import numpy as np
import matplotlib.pyplot as plt


def jacobi(A, b, x0, tol=1e-8, max_iter=500):
    diagonal = np.diag(A)
    remainder = A - np.diagflat(diagonal)
    x = x0.copy()
    errors = []

    for _ in range(max_iter):
        x_new = (b - remainder @ x) / diagonal
        error = np.linalg.norm(x_new - x, ord=np.inf)
        errors.append(error)

        if error < tol:
            return x_new, errors, True

        x = x_new

    return x, errors, False


def gauss_seidel(A, b, x0, tol=1e-8, max_iter=500):
    x = x0.copy()
    errors = []

    for _ in range(max_iter):
        old = x.copy()

        for i in range(len(b)):
            x[i] = (
                b[i]
                - A[i, :i] @ x[:i]
                - A[i, i + 1 :] @ old[i + 1 :]
            ) / A[i, i]

        error = np.linalg.norm(x - old, ord=np.inf)
        errors.append(error)

        if error < tol:
            return x, errors, True

    return x, errors, False


def main():
    print("ITERATIVE METHODS FOR LINEAR SYSTEMS")
    print("1. Original 5-point temperature model")
    print("2. Modified 3-point temperature model")
    print("3. General 3-variable linear system")

    choice = input("Choose a model (1, 2 or 3): ")

    models = {
        "1": (
            np.array(
                [
                    [2.0, -1.0, 0.0, 0.0, 0.0],
                    [-1.0, 2.0, -1.0, 0.0, 0.0],
                    [0.0, -1.0, 2.0, -1.0, 0.0],
                    [0.0, 0.0, -1.0, 2.0, -1.0],
                    [0.0, 0.0, 0.0, -1.0, 2.0],
                ]
            ),
            np.array([100.0, 0.0, 0.0, 0.0, 20.0]),
            "Original temperature model",
        ),
        "2": (
            np.array(
                [
                    [4.0, -1.0, 0.0],
                    [-1.0, 4.0, -1.0],
                    [0.0, -1.0, 4.0],
                ]
            ),
            np.array([100.0, 50.0, 20.0]),
            "Modified 3-point model",
        ),
        "3": (
            np.array(
                [
                    [10.0, -2.0, 1.0],
                    [-1.0, 8.0, -2.0],
                    [2.0, -1.0, 7.0],
                ]
            ),
            np.array([30.0, 20.0, 10.0]),
            "General linear system",
        ),
    }

    if choice not in models:
        print("Invalid selection.")
        return

    A, b, model_name = models[choice]
    n = len(b)

    guess_input = input(
        f"Enter {n} initial guesses separated by commas "
        "(press Enter for zeros): "
    )
    if guess_input.strip():
        try:
            x0 = np.array([float(value) for value in guess_input.split(",")])
        except ValueError:
            print("Error: enter numeric guesses separated by commas.")
            return

        if len(x0) != n:
            print("Error: the number of guesses must match the unknowns.")
            return
    else:
        x0 = np.zeros(n)

    try:
        tol = float(input("Enter tolerance (e.g. 0.000001): "))
        max_iter = int(input("Enter maximum iterations (e.g. 500): "))
    except ValueError:
        print("Error: tolerance and maximum iterations must be numeric.")
        return

    if tol <= 0 or max_iter <= 0:
        print("Tolerance and iterations must be positive.")
        return

    if np.any(np.diag(A) == 0):
        print("Error: diagonal elements cannot be zero.")
        return

    x_j, err_j, converged_j = jacobi(A, b, x0, tol, max_iter)
    x_gs, err_gs, converged_gs = gauss_seidel(A, b, x0, tol, max_iter)
    x_exact = np.linalg.solve(A, b)

    print(f"\nMODEL: {model_name}")
    print("\nJacobi solution:")
    print(x_j)
    print("Jacobi iterations:", len(err_j))
    print("Jacobi converged:", converged_j)

    print("\nGauss-Seidel solution:")
    print(x_gs)
    print("Gauss-Seidel iterations:", len(err_gs))
    print("Gauss-Seidel converged:", converged_gs)

    print("\nDirect solution:")
    print(x_exact)

    plt.figure(figsize=(8, 5))
    plt.semilogy(err_j, label="Jacobi")
    plt.semilogy(err_gs, label="Gauss-Seidel")
    plt.xlabel("Iteration")
    plt.ylabel("Maximum change")
    plt.title("Iterative Methods Convergence Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
