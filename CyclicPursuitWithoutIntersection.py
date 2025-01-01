import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

robot_numbers = 6
T = 100 # Number of frames
dt = 0.1 # Time Step (sec)
time_steps = np.arange(0,T*dt,dt) # From 0(including) to T*dt(excluding) = Total Time with step = 0.1
# print(time_steps)
# print(len(time_steps))


# Z matrix
#          0 sec  0.1 sec  0.2 sec .. . 99.9 sec
# robot1    z1(0)  z1(0.1)
# robot2
# robot3
# .
# .
# robot6                                  z6(99.9)
z = np.zeros((robot_numbers, T), dtype=complex)
z[:,0] = np.array([10+55j, 40+85j, 75+60j, 80+35j, 55+20j, 25+20j])# Initial position of robots at t=0 sec.

# U matrix for 6 points
U = np.zeros((robot_numbers, robot_numbers), dtype=int)

for i in range(robot_numbers):
    U[i, (i+1)%robot_numbers] = 1

#     | 0 1 0 0 0 0 |
#     | 0 0 1 0 0 0 |
#     | 0 0 0 1 0 0 |
# U = | 0 0 0 0 1 0 |
#     | 0 0 0 0 0 1 |
#     | 1 0 0 0 0 0 |

I = np.eye(robot_numbers)
# print(I)

M = U - I

# Updating the z matrix
# dz/dt = M @ z
# (z(t) - z(t-1)/dt) = M @ z(t-1)
for t in range(1, T):
    z[:,t] = z[:,t-1] + dt * (M @ z[:,t-1]) # Update postions of robots in t column or 0.t sec

# Setup the animation
#subplots() without arguments returns a Figure and a single Axes.
fig, ax = plt.subplots()
ax.set_xlim(0,100)
ax.set_ylim(0,100)
ax.set_aspect('equal') # same scaling from data to plot units for x and y
fig.suptitle("6-Point Cyclic Pursuit Simulation")

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
