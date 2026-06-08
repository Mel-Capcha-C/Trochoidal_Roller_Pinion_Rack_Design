import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation

print(matplotlib.get_backend())

# ---- Parameters (adjust these) ----
m = 11.0
z = 10
c_y = 5.0 / m
c_f = 16.0 / m

R = m * z / 2 + m * c_y
r = m * z / 2

beta = np.linspace(0, 2 * np.pi, 1000)
x_pitch_circle = R * np.cos(beta)
y_pitch_circle = R * (1 + np.sin(beta))

# ---- Figure ----
fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.grid()
# ax.set_xlim([-70, 70])
# ax.set_ylim([-10, 130])
ax.set_xlim([-55, 5])
ax.set_ylim([-10, 50])

# (pitch_circle,) = ax.plot([], [], lw=2)
(pitch_circle,) = ax.plot([], [])
rollers = [ax.plot([], [])[0] for _ in range(z)]
(line_action,) = ax.plot([], [])

# # ---- Init function ----
# def init():
#     # line.set_data([], [])
#     roller.set_data([], [])
#     # return line, roller
#     return rollerclea

number_frames = 300
angular_velocity = 0.003


# ---- Update function ----
def update(frame):
    pitch_circle.set_data(x_pitch_circle, y_pitch_circle)
    angle = frame * angular_velocity  # rotation speed
    la_angles = np.arange(0.0, number_frames, 1) * angular_velocity

    for ii in range(z):
        x_roller, y_roller = rollers_sim(angle, ii, z)
        rollers[ii].set_data(x_roller, y_roller)

    x_D, y_D = line_action_sim(la_angles[:frame])
    line_action.set_data(x_D, y_D)
    # # Example: moving contact point along curve
    # idx = frame % len(beta)
    # roller.set_data(x_roller[idx], y_roller[idx])
    return pitch_circle, rollers


def rollers_sim(t, i, N):
    angle = t + (2 * np.pi / N) * i
    x = -r * np.sin(angle) + m * c_f / 2 * np.cos(beta)
    y = R - r * np.cos(angle) + m * c_f / 2 * np.sin(beta)
    return x, y


def line_action_sim(phi):
    # # ---- Parameter range (phi) ----
    # phi = np.linspace(0, 50.56712 * np.pi / 180, 1000)

    # ---- Intermediate variables ----
    x_A = -(m * z / 2) * np.sin(phi)
    y_A = (m * z / 2) + m * c_y - (m * z / 2) * np.cos(phi)

    R = np.sqrt(x_A**2 + y_A**2)

    # ---- Avoid division by zero ----
    R_safe = np.where(R == 0, 1e-8, R)

    # ---- Final expressions ----
    factor = (R_safe - (m * c_f) / 2) / R_safe

    x_D = x_A * factor
    y_D = y_A * factor
    return x_D, y_D


# ---- Animation ----
ani = FuncAnimation(fig, update, frames=number_frames, interval=30)
# Save animation (important in Visual Studio)
# ani.save("meshing.gif", writer="pillow", fps=30)


# plt.plot(x_pitch_circle, y_pitch_circle, label="Pitch Circle")
# plt.xlabel("x(mm)")
# plt.ylabel("y(mm)")
# plt.title("Parametric Plot of Trochoidal Tooth Profile")
# plt.axis("equal")
# plt.grid()

# plt.plot(x_D, y_D)
plt.show()

# plt.savefig("plot.png", dpi=300)  # ✅ Save instead of show
