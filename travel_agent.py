
import random
import math
import matplotlib.pyplot as plt

# A more complex distance matrix for 10 cities
distance_matrix = [
    [0, 29, 20, 21, 17, 28, 35, 40, 10, 50],
    [29, 0, 15, 17, 30, 25, 33, 50, 20, 40],
    [20, 15, 0, 28, 10, 15, 35, 25, 15, 30],
    [21, 17, 28, 0, 35, 20, 22, 30, 18, 25],
    [17, 30, 10, 35, 0, 15, 40, 25, 22, 18],
    [28, 25, 15, 20, 15, 0, 22, 30, 25, 35],
    [35, 33, 35, 22, 40, 22, 0, 18, 35, 28],
    [40, 50, 25, 30, 25, 30, 18, 0, 28, 20],
    [10, 20, 15, 18, 22, 25, 35, 28, 0, 15],
    [50, 40, 30, 25, 18, 35, 28, 20, 15, 0]
]


# Function to calculate the total distance of the tour
def total_distance(tour, distance_matrix):
    distance = 0
    for i in range(len(tour)):
        distance += distance_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return distance


# Function to generate a neighboring solution by swapping two cities
def swap_two_cities(tour):
    new_tour = tour[:]
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour


# Cooling schedule: function to reduce temperature
def schedule(t):
    return 1000 * (0.995 ** t)


# Simulated Annealing algorithm
def simulated_annealing(distance_matrix, max_iterations):
    num_cities = len(distance_matrix)

    # Initial random tour
    current_tour = list(range(num_cities))
    random.shuffle(current_tour)
    current_distance = total_distance(current_tour, distance_matrix)

    best_tour = current_tour
    best_distance = current_distance

    current = current_tour
    best_distances = []

    for t in range(max_iterations):
        T = schedule(t)
        if T == 0:
            break

        next_tour = swap_two_cities(current)
        delta_E = total_distance(next_tour, distance_matrix) - total_distance(current, distance_matrix)

        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            current = next_tour
            current_distance = total_distance(current, distance_matrix)

        if current_distance < best_distance:
            best_tour = current
            best_distance = current_distance

        best_distances.append(best_distance)

        # Print the current best distance at each iteration
        if t % 100 == 0:
            print(f"Iteration {t + 1}: Best Distance = {best_distance}")

    return best_tour, best_distance, best_distances


# Parameters for the Simulated Annealing
initial_temp = 1000
max_iterations = 5000

# Run the Simulated Annealing algorithm
best_tour, best_distance, best_distances = simulated_annealing(distance_matrix, max_iterations)

# Print the best tour and distance
print("Best Tour:", best_tour)
print("Best Distance:", best_distance)

# Plot the best distance over iterations
plt.plot(best_distances)
plt.title("Simulated Annealing: Best Distance Over Iterations")
plt.xlabel("Iteration")
plt.ylabel("Best Distance")
plt.show()
