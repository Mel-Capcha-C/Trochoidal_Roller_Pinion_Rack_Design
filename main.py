import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
import win32com.client

matplotlib.use("QtAgg")
print(matplotlib.get_backend())

# ---- Parameters (adjust these) ----
m = 11.0
z = 10
c_y = 5.0 / m
c_f = 16.0 / m
c_h = 16.0 / m

R = m * z / 2 + m * c_y
r = m * z / 2

beta = np.linspace(0, 2 * np.pi, 1000)


# ---- Figure ----
fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.grid()

# (pitch_circle,) = ax.plot([], [], lw=2)
(pitch_circle,) = ax.plot([], [])
rollers = [ax.plot([], [])[0] for _ in range(z)]
(line_action,) = ax.plot([], [])
(tooth_profile,) = ax.plot([], [])


def F(phi):
    x_A = -(m * z / 2) * np.sin(phi)
    y_A = (m * z / 2) + m * c_y - (m * z / 2) * np.cos(phi)

    Nvec_norm = np.sqrt(x_A**2 + y_A**2)

    # ---- Final expressions ----
    factor = (Nvec_norm - (m * c_f) / 2) / Nvec_norm
    y_D = y_A * factor

    return y_D - m * c_h - m * c_y


def secant(phi0, phi1, tol=1e-8, max_iter=50):
    for _ in range(max_iter):
        f0 = F(phi0)
        f1 = F(phi1)

        if abs(f1 - f0) < 1e-12:
            break

        phi2 = phi1 - f1 * (phi1 - phi0) / (f1 - f0)

        if abs(phi2 - phi1) < tol:
            return phi2

        phi0, phi1 = phi1, phi2

    return phi1


# # ---- Init function ----
# def init():
#     # line.set_data([], [])
#     roller.set_data([], [])
#     # return line, roller
#     return rollerclea


phi_h = secant(0, 1)
print(phi_h)

# ========== Animation parameters ============

angular_velocity = 0.01
number_frames = (int)(phi_h // angular_velocity)
print(number_frames)

# Do you want a stationary simulation, i.e. the pinion rotates, but does not move
stationary_flag = False

if stationary_flag:
    # Stationary frame
    ax.set_xlim([-70, 70])
    ax.set_ylim([-10, 130])
else:
    # Moving frame
    # ax.set_xlim([-10, 400])
    ax.set_xlim([-10, 150])
    ax.set_ylim([-10, 125])


# ---- Update function ----
def update(frame):
    angle = frame * angular_velocity  # rotation speed

    x_pitch_circle, y_pitch_circle = pitch_circle_sim(angle, stationary_flag)
    pitch_circle.set_data(x_pitch_circle, y_pitch_circle)

    la_angles = np.arange(0.0, number_frames, 1) * angular_velocity

    for ii in range(z):
        x_roller, y_roller = rollers_sim(angle, ii, z, stationary_flag)
        rollers[ii].set_data(x_roller, y_roller)

    x_D, y_D = line_action_sim(la_angles[:frame], stationary_flag)
    line_action.set_data(x_D, y_D)

    # x_tooth_profile, y_tooth_profile = tooth_profile_sim(la_angles[:frame])
    # tooth_profile.set_data(x_tooth_profile, y_tooth_profile)

    return pitch_circle, rollers, line_action, tooth_profile


def pitch_circle_sim(phi=0, stationary_flag=True):
    x_pitch_circle = R * (phi * (not stationary_flag) + np.cos(beta))
    y_pitch_circle = R * (1 + np.sin(beta))
    return x_pitch_circle, y_pitch_circle


def rollers_sim(phi=0, i=0, N=4, stationary_flag=True):
    angle = phi + (2 * np.pi / N) * i
    x = R * phi * (not stationary_flag) - r * np.sin(angle) + m * c_f / 2 * np.cos(beta)
    y = R - r * np.cos(angle) + m * c_f / 2 * np.sin(beta)
    return x, y


def line_action_sim(phi, stationary_flag=True):
    # # ---- Parameter range (phi) ----
    # phi = np.linspace(0, 50.56712 * np.pi / 180, 1000)

    # ---- Intermediate variables ----
    x_A = -(m * z / 2) * np.sin(phi)
    y_A = (m * z / 2) + m * c_y - (m * z / 2) * np.cos(phi)

    Nvec_norm = np.sqrt(x_A**2 + y_A**2)

    # ---- Avoid division by zero ----
    # R_safe = np.where(R == 0, 1e-8, R)

    # ---- Final expressions ----
    factor = (Nvec_norm - (m * c_f) / 2) / Nvec_norm

    x_D = R * phi * (not stationary_flag) + x_A * factor
    y_D = y_A * factor
    return x_D, y_D


def tooth_profile_sim(phi):
    x_roller = R * phi - r * np.sin(phi)
    y_roller = R - r * np.cos(phi)
    x_O = R * phi
    y_O = 0
    Nvec_norm = np.sqrt((x_O - x_roller) ** 2 + (y_O - y_roller) ** 2)
    unit_Nvec = 1 / Nvec_norm * (x_O - x_roller, y_O - y_roller)
    x_tooth_profile = x_roller + unit_Nvec[0] * m * c_f / 2
    y_tooth_profile = y_roller + unit_Nvec[1] * m * c_f / 2
    return x_tooth_profile, y_tooth_profile


# # ====================== Animation ==========================
# ani = FuncAnimation(fig, update, frames=number_frames, interval=30)
# # Save animation (important in Visual Studio)
# # ani.save("meshing.gif", writer="pillow", fps=30)

# plt.show()
# # plt.savefig("plot.png", dpi=300)  # Save instead of show

# ======================== Inventor ===========================
# Launch Inventor
# inv = win32com.client.Dispatch("Inventor.Application")
# inv.Visible = True

# # Open your file
# doc = inv.Documents.Open(
#     r"C:\Users\Mel_C\Data\Documents\Projects\Impulso\Mechanical Design\LeonardBot_Impulso_003\Trochoidal\Cremallera.ipt"
# )

# params = doc.ComponentDefinition.Parameters

# # Modify parameters
# params.Item("d").Value = 4.0  # cm

# # Rebuild
# doc.Update()

# print("Updated successfully")
