import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, interp1d

# Program for estimating temperature using interpolation


def main():

    # Display program heading
    print("TEMPERATURE INTERPOLATION SYSTEM")
    print("================================")

    # Request the number of measurements
    n = int(input("Enter number of temperature measurements (minimum 3): "))

    if n < 3:
        print("Error: At least 3 measurements are required.")
        return

    hours = []
    temperatures = []

    # Collect temperature measurements from the user
    for i in range(n):

        print(f"\nMEASUREMENT {i + 1}")
        print("--------------------------")

        hour = float(input("Enter hour (e.g. 8 for 8 AM): "))
        temperature = float(input("Enter temperature in Celsius: "))

        hours.append(hour)
        temperatures.append(temperature)

    # Convert measurements into NumPy arrays
    hours = np.array(hours, dtype=float)
    temperatures = np.array(temperatures, dtype=float)

    # Arrange measurements in ascending order of time
    order = np.argsort(hours)

    hours = hours[order]
    temperatures = temperatures[order]

    # Ensure that every measurement has a unique hour
    if len(np.unique(hours)) != n:
        print("\nError: Duplicate hours are not allowed.")
        return

    # Construct interpolation models
    linear_model = interp1d(hours, temperatures, kind="linear")
    cubic_model = CubicSpline(hours, temperatures)

    # Request the time for temperature estimation
    target_time = float(
        input("\nEnter hour to estimate (e.g. 10.5 for 10:30 AM): ")
    )

    # Check whether the requested time is within the data range
    if target_time < hours[0] or target_time > hours[-1]:
        print("Error: Enter a time within the measured hours.")
        return

    # Calculate estimated temperatures
    linear_result = float(linear_model(target_time))
    cubic_result = float(cubic_model(target_time))

    # Display interpolation results
    print("\nINTERPOLATION RESULTS")
    print("==============================")

    print(f"Target time: {target_time:.2f} hours")
    print(f"Linear interpolation: {linear_result:.2f} °C")
    print(f"Cubic spline interpolation: {cubic_result:.2f} °C")

    # Generate values for plotting the interpolation curves
    times = np.linspace(hours[0], hours[-1], 100)

    linear_estimates = linear_model(times)
    cubic_estimates = cubic_model(times)

    # Plot the original temperature measurements
    plt.scatter(
        hours,
        temperatures,
        color="red",
        label="Measured temperatures"
    )

    # Plot linear interpolation
    plt.plot(
        times,
        linear_estimates,
        label="Linear interpolation"
    )

    # Plot cubic spline interpolation
    plt.plot(
        times,
        cubic_estimates,
        label="Cubic spline interpolation"
    )

    # Highlight the estimated temperature
    plt.scatter(
        [target_time],
        [cubic_result],
        color="green",
        label="Estimated temperature"
    )

    # Add graph labels and formatting
    plt.xlabel("Hour of day")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Interpolation Graph")

    plt.legend()
    plt.grid(True)

    # Display the graph
    plt.show()


if __name__ == "__main__":
    main()
