import numpy as np
import matplotlib.pyplot as plt
# Defining Given Constants with a little bit of math 
a = 100 # Distance from airport
w = 44  # wind speed 
v_0 = 88 # initial velocity 
x_0 = a  # initial x_value 
y_0 = 0  # initial y_value 
h = 0.0001 # Step size used for difference approximation
k = w/v_0 # constant factor in ODE

def f(x, y):  
    """Differential Equation from ODE"""
    return (y/x) - (k * np.sqrt(1 + ((y/x) ** 2)))   

def euler_forward(f, x_0, y_0, h, target):  
    # Start Making Arrays to hold x_values and y_values of sequence
    x_values = [x_0] 
    y_values = [y_0]  

    # Condition is > target as we are decreasing x
    while x_values[-1] > target:  
        y_n = y_values[-1]  
        x_n = x_values[-1]  

        # Safegaurd to prevent approximation from overshooting
        if x_n - h < target: 
            h = x_n - target 
        
        # Euler Forward Sequences, - instead of + as h needs to be - 
        y_next = y_n - (h * f(x_n, y_n))
        x_next = x_n - h 

        # We append the values as we reference the last index in the equation for x_n, y_n
        y_values.append(y_next) 
        x_values.append(x_next)   
        
    # Reversed the arrays for ease of printing 
    return np.array(x_values[::-1]), np.array(y_values[::-1])

x_vals, y_vals = euler_forward(f, x_0, y_0, h, 0) 

# print(x_vals[0]) 
# print(y_vals[0])  
# print(len(x_vals)) 
# print(len(y_vals))

plt.figure(figsize=(8,6))  
plt.plot(x_vals[1::], y_vals[1::], color="green", label="Trajectory") 
plt.scatter(x_vals[1::int(len(x_vals)/100)], y_vals[1::int(len(x_vals)/100)], color="blue") 
plt.xlabel("Distance to Airport (x)") 
plt.ylabel("Altitude (y)") 
plt.title("Trajectory of the Plane") 
plt.legend() 
plt.grid(True) 
plt.show()

# Print Coordinates
print("Coordinates (x, y) of 100 evenly spaced points: ")  
step = len(x_vals) // 100
for i in range(0, len(x_vals), step): 
    print(f"({x_vals[i]:.2f}, {y_vals[i]:.2f})")
