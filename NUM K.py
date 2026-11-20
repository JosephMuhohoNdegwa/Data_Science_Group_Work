from scipy.optimize import root

# Program to find intersections of a circle and a parabola
# Circle: x^2 + y^2 = 4
# Parabola: y = x^2 - 1


def equations(z):
    x, y = z
    return [
        x**2 + y**2 - 4,
        y - x**2 + 1,
    ]


def main():
    # Display program title
    print("NONLINEAR EQUATIONS SOLVER")
    print("==========================")

    # Get initial guesses from the user
    x_guess = float(input("Enter initial guess for x: "))
    y_guess = float(input("Enter initial guess for y: "))
    initial_guess = [x_guess, y_guess]

    # Solve the nonlinear equations
    solution = root(equations, initial_guess)

    # Display the results
    print("\nSOLUTION RESULTS")
    print("==========================")
    print("Initial guess:", initial_guess)

    if solution.success:
        x, y = solution.x
        print("\nIntersection Point")
        print("--------------------------")
        print("X-coordinate:", round(x, 6))
        print("Y-coordinate:", round(y, 6))

        print("\nNumerical Accuracy")
        print("--------------------------")
        print("Residuals:")
        print("Equation 1:", round(solution.fun[0], 10))
        print("Equation 2:", round(solution.fun[1], 10))

        print("\nConvergence Status:", "Successful")
        print("Solver message:", solution.message)
    else:
        print("\nThe solver failed to find a solution.")
        print("Convergence Status: Unsuccessful")
        print("Solver message:", solution.message)


if __name__ == "__main__":
    main()
