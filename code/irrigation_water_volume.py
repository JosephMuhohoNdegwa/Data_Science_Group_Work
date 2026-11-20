import numpy as np
from scipy.integrate import simpson


# Irrigation flow-rate readings every 10 minutes
time_minutes = np.array([0, 10, 20, 30, 40, 50, 60], dtype=float)
flow_litres_per_min = np.array([4, 5, 7, 8, 7, 6, 4], dtype=float)

# Integrate flow rate over time to estimate water volume
volume_trapezoid = np.trapezoid(flow_litres_per_min, time_minutes)
volume_simpson = simpson(flow_litres_per_min, x=time_minutes)

print(f"Water volume using trapezoidal rule: {volume_trapezoid:.3f} litres")
print(f"Water volume using Simpson's rule:   {volume_simpson:.3f} litres")
print(
    "Difference between estimates: "
    f"{abs(volume_simpson - volume_trapezoid):.3f} litres"
)
