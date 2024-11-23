#!/bin/python3.10
import random
from datetime import datetime, timedelta

# Function to generate candlestick data
def generate_candlestick_data(timestamp):
    open_price = random.uniform(1.0, 2.0)  # Random opening price
    close_price = open_price * random.uniform(0.95, 1.05)  # Close near open
    high_price = max(open_price, close_price) * random.uniform(1.01, 1.05)  # Slightly higher
    low_price = min(open_price, close_price) * random.uniform(0.95, 0.99)  # Slightly lower
    volume = random.randint(500, 2000)  # Random volume
    return f"ton_price_data open={open_price:.2f},high={high_price:.2f},low={low_price:.2f},close={close_price:.2f},volume={volume} {timestamp}"

# Generate data points
start_time = datetime.now()
data_points = []
for i in range(100):  # Generate 100 points
    # Calculate timestamp in nanoseconds
    timestamp = int((start_time + timedelta(minutes=i * 5)).timestamp() * 1e9)
    data_points.append(generate_candlestick_data(timestamp))

# Write to file or print
with open("ton_candlestick_data.txt", "w") as f:
    f.write("\n".join(data_points))

print("Fake data generated in ton_candlestick_data.txt")
