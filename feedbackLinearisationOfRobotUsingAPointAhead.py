import math as m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

T = 1000
x = np.zeros(T)
y  = np.zeros(T)
theta = np.zeros(T)
e = 0.2

x[0] = x_curr = 1
y[0] = y_curr = 1
theta[0] = theta_curr = 0



for i in range(1, 1000):
      v = -x_curr*m.cos(theta_curr)-y_curr*m.sin(theta_curr) - e
      w = (1/e)*(x_curr*m.sin(theta_curr) - y_curr*m.cos(theta_curr))
      x_curr = x_curr + v*m.cos(theta_curr)*0.1
      y_curr = y_curr + v * m.sin(theta_curr) * 0.1
      theta_curr = theta_curr + w * 0.1
      x[i]=x_curr
      y[i] = y_curr
      theta[i] = theta_curr

# print(x)
# print(y)
# print(theta)



# Axes Limit
fig, axis = plt.subplots()
axis.set_xlim([-1.25, 1.5])
axis.set_ylim(-0.5, 1.25)
fig.suptitle("Simulation of Linearisation of unicycle at a point just Ahead.")

# Define triangle vertices
triangle = np.array([[0.0, 0.0, 0.2, 0.0],
                     [-0.1, 0.1, 0, -0.1]])


#Animated Plot
animated_plot, = axis.plot([], [], 'b-', lw=2)
trajectory_line, = axis.plot([], [], 'r-', lw=1)  # Centroid trajectory line

# Store centroid trajectory
centroid_x = []
centroid_y = []
def update_data(frame):
    # Current rotation angle
    angle = theta[frame]
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])

    # Rotate and translate triangle
    rotated_triangle = rotation_matrix @ triangle
    translated_triangle = rotated_triangle + np.array([[x[frame]], [y[frame]]])

    # Calculate and store the centroid
    cx = np.mean(translated_triangle[0, :3])
    cy = np.mean(translated_triangle[1, :3])
    centroid_x.append(cx)
    centroid_y.append(cy)

    # Update triangle patch
    animated_plot.set_data(translated_triangle[0, :], translated_triangle[1, :])
    trajectory_line.set_data(centroid_x, centroid_y)

    return animated_plot,trajectory_line

animation = FuncAnimation(
    fig = fig,
    func = update_data,
    frames = T,
    interval = 100,
)

plt.grid()
plt.show()

