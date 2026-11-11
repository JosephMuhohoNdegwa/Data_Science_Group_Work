from scipy.optimize import root

# Program to find intersections of a circle and a parabola
# Circle: x^2 + y^2 = 4
# Parabola: y = x^2 - 1


def equations(z):
    x, y = z
    return [
        x**2 + y**2 - 4,
        y - (x**2 - 1),
    ]


def main():
    # Input initial guesses from the user
    print("NONLINEAR EQUATIONS SOLVER")
    print("--------------------------")

    x_guess = float(input("Enter initial guess for x: "))
    y_guess = float(input("Enter initial guess for y: "))
    guess = [x_guess, y_guess]

    # Solve the equations
    solution = root(equations, guess)

    # Display the results
    print("\nRESULTS")
    print("--------------------------")
    print("Initial guess:", guess)

    if solution.success:
        x, y = solution.x
        print("Intersection point:")
        print("x =", round(x, 6))
        print("y =", round(y, 6))
        print("\nResiduals:", equations(solution.x))
        print("Converged:", solution.success)
    else:
        print("The solver did not converge.")
        print("Message:", solution.message)


if __name__ == "__main__":
    main()
