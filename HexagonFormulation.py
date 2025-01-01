import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
T = 1000  # Total number of time steps
robot_numbers = 6  # Number of robots
dt = 0.1  # Time step size

# Define Laplacian matrix for cyclic graph of 6 robots
L = np.array([[1, 0, 0, 0, 0, -1],
              [-1, 1, 0, 0, 0, 0],
              [0, -1, 1, 0, 0, 0],
              [0, 0, -1, 1, 0, 0],
              [0, 0, 0, -1, 1, 0],
              [0, 0, 0, 0, -1, 1]])

# # Define Laplacian matrix for cyclic graph of 6 robots
# L = np.array([[1, -1, 0, 0, 0, 0],
#               [0, 1, -1, 0, 0, 0],
#               [0, 0, 1, -1, 0, 0],
#               [0, 0, 0, 1, -1, 0],
#               [0, 0, 0, 0, 1, -1],
#               [-1, 0, 0, 0, 0, 1]])

# Define desired formation (triangle) in complex plane
d_matrix = L @ np.array([0, 10-10j / np.sqrt(3), 10-30j / np.sqrt(3), -40j / np.sqrt(3), -10-30j / np.sqrt(3), -10-10j /np.sqrt(3)])

z = np.zeros((robot_numbers, T), dtype=complex)
z[:, 0] = np.array(
    [20 + 40j, 80 + 40j, 40 + 20j, 40 + 80j, 60 + 20j, 60 + 80j])  # Initial position of robots at t=0 sec.
# [20 + 40j, 80 + 40j, 40 + 20j, 40 + 80j, 60 + 20j, 60 + 80j]


# Control law simulation
# def update_positions(positions, c, L):
#     d = L @ c  # Control vector from desired formation
#     u = -L @ positions + d  # Control law
#     return positions + time_step * u


# Simulate over time
for t in range(1, T):
    # positions = update_positions(positions, d_matrix, L)
    # positions_history[t] = positions

    z[:,t] = z[:, t-1] + dt * (-L @ z[:, t-1] + d_matrix)

# Setup the animation
#subplots() without arguments returns a Figure and a single Axes.
fig, ax = plt.subplots()
ax.set_xlim(0,100)
ax.set_ylim(0,100)
ax.set_aspect('equal') # same scaling from data to plot units for x and y
fig.suptitle("Hexagon Formulation")

lines = [ax.plot([], [], 'o-', label=f'Point {i+1}')[0] for i in range (robot_numbers)]
trajectories = [ax.plot([], [], '-', lw=0.5)[0] for _ in range(robot_numbers)]

# print(ax.plot([], [], 'o-', label=f'Point {i+1}'))

# Update Function
def update(frame):
    for i, line in enumerate(lines): #Enumerate : Returns an iterator with index and element pairs from the original iterable
        line.set_data([z[i, frame].real], [z[i, frame].imag])
        trajectories[i].set_data( z[i, :frame].real, z[i, :frame].imag)
    return lines + trajectories

ani = FuncAnimation(fig, update, frames=T, interval=50, blit=True)
plt.legend()
plt.grid()
plt.show()
