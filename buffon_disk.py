import numpy as np 
import matplotlib.pyplot as plt 

def simulate_disc_tosses(diameter, num_tosses):    
    """
    Function to simulate tossing a disc and the lines it crosses  

    Inputs: 
    - diameter: diameter of the disc being tossed  
    - num_tosses: Number of tosses being simulated 

    Outputs: 
    - probabilities: Full array of probabilities for it crossing x number of lines
      meaning 1 line, 2 lines, 3 lines or 4 lines
    """
    # Hashmap to store successful tosses per number of lines being crossed
    successful_tosses = {} 
    for j in range (1, 5): # represents lines being crossed (1 - 4) 
        # print(f"Simulating Crossing {j} lines")   
        # Simulates the bottom/start of the circles num_tosses times
        bottom = np.random.uniform(0, 1, num_tosses) 
        if diameter >= j: # Given in problem
            successful_tosses[j] = num_tosses
        elif diameter < j and j - diameter > 1: 
            successful_tosses[j] = 0 
        else:   
            # We check if any of our bottoms lets us cross a line after crossing  
            # other lines due to the height needed
            height_needed = j - diameter 
            success = np.sum(bottom >= height_needed) 
            successful_tosses[j] = float(success) 
    # Array to store probabilities 
    probabilities = [] 
    for value in successful_tosses.values():   
        # Probability is the number of successes/total
        probabilities.append(value/num_tosses)  
    # print(f"Probabilities for {diameter}: {probabilities}")
    return probabilities # Full array of probabilities for it crossing x-line, meaning 1, 2, 3, 4   

def monte_carlo_disc_toss(diameters, num_tosses):  
    """
    Function to call on list of diameters that we want to simulate tosses for 

    Inputs: 
    - diameters: List of diameters for discs being  
    - num_tosses: Number of tosses being simulated 

    Outputs: 
    - crossing_probabilities: A dictionary of lists of the  
    probabilities of each diameter crossing 1-4 lines 
    """
    # So now this function will actually run this simulation and store the crossing probabilities for each thing  
    crossing_probabilities = {} 
    for diameter in diameters:  
        # print(f"Simulating Diameter: {diameter}") 
        probabilities = simulate_disc_tosses(diameter, num_tosses)  
        crossing_probabilities[diameter] = probabilities  
    return crossing_probabilities  

diameters = [1/10, 2/10, 3/10, 4/10, 5/10, 6/10, 7/10, 8/10, 9/10, 10/10, 15/10, 20/10, 30/10] 
num_tosses = 4444444 

results = monte_carlo_disc_toss(diameters, num_tosses)  
print(results)

# Extract the x values (diameters) 
x = list(results.keys())
y1 = [results[d][0] for d in x]  # Prob of crossing ≥1 line per key
y2 = [results[d][1] for d in x]  # Prob of crossing ≥2 lines per key
y3 = [results[d][2] for d in x]  # Prob of crossing ≥3 lines per key
y4 = [results[d][3] for d in x]  # Prob of crossing ≥4 lines per key 

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x, y1, label="≥1 line", marker='o')
plt.plot(x, y2, label="≥2 lines", marker='o')
plt.plot(x, y3, label="≥3 lines", marker='o')
plt.plot(x, y4, label="≥4 lines", marker='o')

plt.title("Approximate Probability of Crossing Lines vs. Disc Diameter")
plt.xlabel("Disc Diameter (d)")
plt.ylabel("Probability")
plt.grid(True)
plt.legend()
plt.ylim(0, 1.05)
plt.xticks(x, rotation=45)
plt.tight_layout()
plt.show()


print("Printing Table of Probabilities From Simulation: ")
# Get all diameters
diameters = results.keys()

# Header
headers = ["Diameter (d)", "P(≥1 line)", "P(≥2 lines)", "P(≥3 lines)", "P(≥4 lines)"]
col_widths = [15, 15, 15, 15, 15]  # Fixed widths for alignment

# Function to pad each cell
def format_row(values, widths): 
    """ 
    Prints the string we want in this case our values with the correct padding
    """
    return "| " + " | ".join(str(v).ljust(w) for v, w in zip(values, widths)) + " |"

# Print top border
print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")

# Print header row
print(format_row(headers, col_widths))

# Print header separator
print("+" + "+".join("=" * (w + 2) for w in col_widths) + "+")

# Print rows
for d in diameters:
    row = [f"{d:.2f}"] + [f"{p:.12f}" for p in results[d]]
    print(format_row(row, col_widths))

# Print bottom border
print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
