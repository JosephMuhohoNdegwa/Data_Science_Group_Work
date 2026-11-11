import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, interp1d

# Temperature Interpolation Program


def main():
    print("TEMPERATURE INTERPOLATION")
    print("-------------------------")

    # Input the number of measurements
    n = int(input("Enter the number of temperature measurements (minimum 3): "))
    if n < 3:
        print("Please enter at least 3 measurements.")
        return

    hours = []
    temperatures = []

    # Input hours and temperatures
    for i in range(n):
        print(f"\nMeasurement {i + 1}")
        hours.append(float(input("Enter hour (e.g. 8 for 8 AM): ")))
        temperatures.append(float(input("Enter temperature in Celsius: ")))

    # Convert lists into NumPy arrays
    hours = np.array(hours, dtype=float)
    temperatures = np.array(temperatures, dtype=float)

    # Sort measurements by hour
    order = np.argsort(hours)
    hours = hours[order]
    temperatures = temperatures[order]

    # Check for duplicate hours
    if len(np.unique(hours)) != n:
        print("Error: Each measurement must have a unique hour.")
        return

    # Create interpolation functions
    linear = interp1d(hours, temperatures, kind="linear")
    cubic = CubicSpline(hours, temperatures)

    # Input the target time
    target_time = float(
        input("\nEnter the hour to estimate (e.g. 10.5 for 10:30 AM): ")
    )
    if target_time < hours[0] or target_time > hours[-1]:
        print("Error: The target time must be within the measured hours.")
        return

    # Calculate estimates
    linear_result = float(linear(target_time))
    cubic_result = float(cubic(target_time))

    # Display results
    print("\nINTERPOLATION RESULTS")
    print("---------------------")
    print(f"Linear estimate: {linear_result:.2f} C")
    print(f"Cubic estimate:  {cubic_result:.2f} C")

    # Generate points for the graph
    times = np.linspace(hours[0], hours[-1], 100)
    linear_estimates = linear(times)
    cubic_estimates = cubic(times)

    # Plot measurements and interpolation curves
    plt.scatter(hours, temperatures, color="red", label="Measured temperatures")
    plt.plot(times, linear_estimates, label="Linear interpolation")
    plt.plot(times, cubic_estimates, label="Cubic spline interpolation")
    plt.scatter(
        [target_time],
        [cubic_result],
        label="Estimated temperature",
    )
    plt.xlabel("Hour of day")
    plt.ylabel("Temperature (C)")
    plt.title("Temperature Interpolation")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
