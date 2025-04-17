import numpy as np
import matplotlib.pyplot as plt

def clover_curve(theta): 
    """
    Provides Integrand for Computing Overall Clover Area
    """
    return np.sin(2 * theta) 

def compute_overall_area():
    """
    Computes the approximate total area of the clover shape using polar integral.
    """
    def integrand(theta):
        return clover_curve(theta)**2

    theta_min = 0
    theta_max = np.pi
    num_intervals = 100
    delta_theta = (theta_max - theta_min) / num_intervals

    area_sum = 0
    for i in range(num_intervals):
        theta_i = theta_min + i * delta_theta
        theta_ip1 = theta_min + (i + 1) * delta_theta
        area_sum += (integrand(theta_i) + integrand(theta_ip1)) * delta_theta / 2

    # Multiply by 1/2 for polar integral
    return area_sum / 2

def inside_clover(x, y): 
    """ 
    Equation to check if points lie inside clover 
    """ 
    return (x**2 + y**2)**3 <= 4 * x ** 2 * y ** 2   

def inside_rectangle(points, width, height):  
    """
    Function to return points inside the rectangle  
    Inputs: 
    - points: clover points (numpy array)
    - width: width of rectangle 
    - height: height of rectangle
    """ 
    half_width = width/2 
    half_height = height/2

    x = points[:, 0] 
    y = points[:, 1] 
    
    inside_rect = (np.abs(x) <= half_width) & (np.abs(y) <= half_height) 
    return inside_rect 

def generate_clover_points(num_points): 
    """ 
    Function to generate points inside of clover 
    Uses inside_clover as a mask and generates points inside of bounding box -1, 1 
    """ 
    x_points = np.linspace(-1, 1, num_points + 1) 
    y_points = np.linspace(-1, 1, num_points + 1)    

    step = x_points[1] - x_points[0]
    
    # Mesh Grid is returning x poins repeated over and over, and same with y points 
    xx, yy = np.meshgrid(x_points, y_points)   

    # xx.ravel() and yy.ravel() give the flattend version of these
    grid = np.column_stack((xx.ravel(), yy.ravel()))  

    # The grid is now a collection of points in the form (x, y)

    # We care about clover points however so let's mask this  
    # To do this masking we need a truth array or table for each point 
    x = grid[:, 0]  
    y = grid[:, 1] 
    mask = inside_clover(x, y)
    return grid[mask], step  

def transformation(points, xc, yc, alpha):  
    """ 
    Function to transform clover points as if the rectangle was rotated 
    and transformed as we are meant to simulate the center and angle of 
    the rectangle changing 
    """
    # we need to translate each point and now we need to rotate it 
    translated = points - np.array([xc, yc]) 
    sin = np.sin(alpha) 
    cos = np.cos(alpha)   

    # Rotation Matrix Definition
    rotation_matrix = np.array([[cos, -sin],[sin, cos]]) 

    rotated = np.dot(translated, rotation_matrix)  

    return rotated 

# Now that we've transformed we gotta try different inputs and check what's in the rectangle now 
def simulated_annealing_search(points, step, width, height, T_init, T_final, iterations, sigma_xy, sigma_angle):   
    """ 
    Simulated Annealing Code To Try Different Rotations to Maximize 
    Area Cut by Rectangle Cutter 

    Inputs: 
    - points: clover points 
    - step: step for the clover points/grid 
    - width/height: of rectangle
    - T_init: Initial Temperature chosen 
    - T_final: Final Temperature to cool down to 
    - Iterations: Number of Iterations to be done 
    - sigma_xy: normal distribution scale for x, y adjusting
    - sigma_angle: normal distribution scale for alpha adjusting 

    Outputs: 
    - Best
    """
    # Intial State/Guess
    xc, yc, alpha = np.random.uniform(low = 0, high = 0.1), np.random.uniform(low=0, high = 0.1), np.random.uniform(low = 0, high = 0.01) 
    transformed_points = transformation(points, xc, yc, alpha) 
    mask = inside_rectangle(transformed_points, width, height) 
    current_score = np.sum(mask) 

    best_score = current_score 
    best_params = (xc, yc, alpha) 

    # Set up Decay Factor 
    T = T_init 
    decay = (T_final/T_init) ** (1.0/iterations)  

    # Now we iterate
    for _ in range (iterations):      
        # Set up Proposed New Guess
        delta_point_x = np.random.normal(scale=sigma_xy) 
        delta_point_y = np.random.normal(scale=sigma_xy) 
        delta_angle = np.random.normal(scale=sigma_angle)
        xc_new = xc + delta_point_x 
        yc_new = yc + delta_point_y
        alpha_new = (alpha + delta_angle) % np.pi # mod pi to prevent looping 
        
        # New State From New Guess
        transformed_points = transformation(points, xc_new, yc_new, alpha_new) 
        mask_new = inside_rectangle(transformed_points, width, height) 
        new_score = np.sum(mask_new)     

        # Acception or Rejection Field
        delta = new_score - current_score 
        if delta > 0 or np.random.rand() < np.exp(delta/T):  
            xc, yc, alpha = xc_new, yc_new, alpha_new 
            current_score = new_score 
            if new_score > best_score:  
                best_score = new_score
                best_params = (xc, yc, alpha)      

        # Decay
        T *= decay        

    # Area cut by rectangle
    total_area = best_score * (step ** 2)
    return best_params, best_score, total_area
 

clover_points, step = generate_clover_points(400) 
best_params, best_score, total_area = simulated_annealing_search(clover_points, step, 1, 1/np.sqrt(2), 0.1, 0.0001, 20000, 0.02, 0.01) 

print(f"Approximate Best Value For Center X: {best_params[0]:.4f}")
print(f"Approximate Best Value For Center Y: {best_params[1]:.4f}")
print(f"Approximate Best Value For Angle: {best_params[2]:.4f} radians ({np.degrees(best_params[2]):.2f}°)")
print(f"Number Of Sampled Points in Cutter: {best_score}")
print(f"Approximate Area Covered by Cutter: {total_area:.6f}")
print(f"Approximate Actual Area of Clover: {compute_overall_area():.6f}")


def draw_rotated_rectangle(ax, xc, yc, alpha, width=1.0, height=1/np.sqrt(2)): 
    """
    Function to help plot rotated angle that was found! 
    """
    hw, hh = width / 2, height / 2
    corners = np.array([
        [-hw, -hh], [hw, -hh], [hw, hh], [-hw, hh], [-hw, -hh]
    ])
    c, s = np.cos(alpha), np.sin(alpha)
    R = np.array([[c, -s], [s, c]])
    rotated = (corners @ R.T) + np.array([xc, yc])
    ax.plot(rotated[:, 0], rotated[:, 1], 'b-', lw=2)


# Generate clover curve to be plotted
theta = np.linspace(0, 2 * np.pi, 1000)
r = clover_curve(theta)
x = r * np.cos(theta)
y = r * np.sin(theta)

# Plot Code Below 
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x, y, 'r-', lw=1.5, label="Clover Curve")
draw_rotated_rectangle(ax, best_params[0], best_params[1], best_params[2])
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Clover Curve with Optimized Cutter Placement")
ax.legend()
plt.show()