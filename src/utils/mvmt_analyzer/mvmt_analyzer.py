import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read data from CSV file
df = pd.read_csv(
    r"C:\Users\Jeter\dev\heartwoods_miner\src\utils\mvmt_analyzer\example.csv"
)

# Extract x and y data from the DataFrame
x_data = df["distance"].values
y_data = df["time"].values


# Define the function to fit
def func(x, a, b):
    return a * x + b


# Perform the curve fitting
params, covariance = curve_fit(func, x_data, y_data)

# Get the fitted parameters
a, b = params


# Define the fitted function
def fitted_function(x):
    return a * x + b


# def mvmt_fx(y):
#     return (y - b)/a


# Generate the fitted curve
fitted_curve = fitted_function(x_data)

# Plot the original data and the fitted curve
plt.scatter(x_data, y_data, label="Original Data")
plt.plot(x_data, fitted_curve, label="Fitted Curve", color="red")
plt.legend()
plt.xlabel("distance")
plt.ylabel("time")
plt.title("Curve Fitting Example")
plt.show()

# Display the fitted parameters
# print("Fitted Parameters:")
print(f"a: {a}, b: {b}")
distance = 36
print(f"when distance is {distance}, hold time should be {fitted_function(distance)}")
