"""Summarize hourly household electricity consumption."""

import numpy as np


# 24 hourly electricity consumption readings in kWh
electricity_kwh = np.array(
    [
        0.5, 0.4, 0.3, 0.3, 0.4, 0.6,
        0.8, 1.2, 1.5, 1.0, 0.9, 0.7,
        0.8, 0.9, 1.1, 1.3, 1.6, 2.0,
        2.5, 2.2, 1.8, 1.4, 1.0, 0.7,
    ]
)

# Calculate electricity consumption statistics
mean_usage = np.mean(electricity_kwh)
min_usage = np.min(electricity_kwh)
max_usage = np.max(electricity_kwh)

# Convert kWh to Wh
electricity_wh = electricity_kwh * 1000

# Display results
print(f"Average hourly consumption: {mean_usage:.2f} kWh")
print(f"Minimum hourly consumption: {min_usage:.2f} kWh")
print(f"Maximum hourly consumption: {max_usage:.2f} kWh")
print("First six readings in Wh:", electricity_wh[:6])
