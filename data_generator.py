#!/bin/python3.10

import random
import time

# Generate fake candlestick data
def generate_candlestick_data(region):
    open_price = random.uniform(1.0, 2.0)  # Random opening price
    close_price = open_price * random.uniform(0.95, 1.05)  # Close near open
    high_price = max(open_price, close_price) * random.uniform(1.01, 1.05)  # Slightly higher
    low_price = min(open_price, close_price) * random.uniform(0.95, 0.99)  # Slightly lower
    volume = random.randint(500, 2000)  # Random volume
    timestamp = int(time.time_ns())  # Current time in nanoseconds
    return f"ton_price_data,region={region} open={open_price:.2f},high={high_price:.2f},low={low_price:.2f},close={close_price:.2f},volume={volume} {timestamp}"

regions = ["NA", "EU", "ASIA"]
data_points = []

# Generate 100 fake candlestick records
for _ in range(100):
    region = random.choice(regions)
    data_points.append(generate_candlestick_data(region))

# Write to file or print
with open("ton_candlestick_data.txt", "w") as f:
    f.write("\n".join(data_points))

print("Fake data generated in ton_candlestick_data.txt")

