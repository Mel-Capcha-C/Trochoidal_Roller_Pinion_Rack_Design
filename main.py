import numpy as np
import matplotlib.pyplot as plt

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

# ---- Plot ----
plt.figure()

plt.plot(x_pitch_circle, y_pitch_circle, label="Pitch Circle")
plt.xlabel("x(mm)")
plt.ylabel("y(mm)")
plt.title("Parametric Plot of Trochoid Tooth Profile")
plt.axis("equal")
plt.grid()

theta = 2 * np.pi / z
for ii in range(0, z):
    x_roller = -r * np.sin(theta * ii) + m * c_f / 2 * np.cos(beta)
    y_roller = R - r * np.cos(theta * ii) + m * c_f / 2 * np.sin(beta)
    plt.plot(x_roller, y_roller, label=f"Roller {ii}")

# ---- Parameter range (phi) ----
phi = np.linspace(0, 50.56712 * np.pi / 180, 1000)

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

plt.plot(x_D, y_D)
plt.savefig("plot.png", dpi=300)  # ✅ Save instead of show
