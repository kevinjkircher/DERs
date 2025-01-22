"""
Introduction:
This script adapts a simple climate model from https://www.e-education.psu.edu/meteo469/node/198
and uses it to illustrate linearization and discrete-time simulation of a
nonlinear dynamical system.

Author: Kevin J. Kircher, Purdue University, 2025

Required Python Functions:
- k2c: Unit conversion (Kelvin to Celsius).
- for Stairstep plots ( use Matplotlib's `plt.step()` directly).
- nonlinear_climate_sim: Nonlinear climate simulation (students fill this in).
- linearized_climate_sim: Linearized climate simulation (students fill this in).

Notes:
Ensure you install the required libraries before running the script:
    pip install numpy .... etc
"""
# ==============================================================================
# Required imports
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from nonlinearClimateSim import nonlinear_climate_sim
from linearizedClimateSim import linearized_climate_sim
from k2c import k2c

# ==============================================================================
# graphics settings
# ==============================================================================

plt.rc('font', size=20)  # Default font size for all text
plt.rc('axes', titlesize=20, labelsize=20)  # Font size for axes titles and labels
plt.rc('xtick', labelsize=20)  # Font size for x-axis tick labels
plt.rc('ytick', labelsize=20)  # Font size for y-axis tick labels
plt.rc('legend', fontsize=15)  # Font size for legend
plt.rc('figure', titlesize=20)  # Font size for figure titles

# ==============================================================================
# Input Data
# ==============================================================================

alpha = 0.3  # Albedo of Earth's atmosphere
S = 1366  # Solar constant, W/m^2
eps = 0.767  # Emissivity of Earth's atmosphere
sigma = 5.67e-8  # Stefan-Boltzmann constant, W/m^2/K^4
rho = 997  # Density of water, kg/m^3
c = 4.186e3  # Specific heat of water, J/kg/K
R = 6.378e6  # Radius of Earth, m
l = 70  # Depth of well-mixed water layer on Earth's surface, m

C = 0.7 * 4 * np.pi * R**2 * rho * c * l  # Thermal capacitance of Earth's surface, J/K
beta = 4 * sigma * np.pi * R**2 / C  # Intermediate coefficient, K^3/s

# Linear emissivity vs. CO2 concentration fit, eps = eps0 + m*conc
T1 = 286.7  # Avg surface temp from 1880-1900, K
eps1 = 2 * (1 - (1 - alpha) * S / (4 * sigma * T1**4)) # average emissivity from 1880-1900
c1 = (291 + 296) / 2  # Avg CO2 concentration from 1880-1900, ppm
T2 = 287.8  # Avg surface temp in 2022, K
eps2 = 2 * (1 - (1 - alpha) * S / (4 * sigma * T2**4)) #emissivity in 2022
c2 = 418.56  # CO2 concentration in 2022, ppm
m = (eps2 - eps1) / (c2 - c1)  # Slope, 1/ppm
eps0 = eps1 - m * c1  # Intercept

# Timing
t0 = 0  # Initial time, s
dt = 365 * 24 * 3600  # Time step, s
K = 78  # Number of time steps
tf = t0 + K * dt  # Final time, s
t = np.arange(t0, tf + dt, dt)  # Time span, s
y = 2022 + t / (365 * 24 * 3600)  # Year

# ==============================================================================
# Plots
# ==============================================================================

# CO2 Concentration Plot

# emissivity vs. CO2 concentration
c_plot = np.arange(200, 501)
eps_values = eps0 + m * c_plot
temp_values = ((1 - alpha) * S / (4 * sigma * (1 - (eps0 + m * c_plot) / 2)))**(1 / 4)
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(c_plot, eps_values, label="Atmospheric emissivity", color="blue")
ax1.set_xlabel("Atmospheric CO$_2$ concentration (ppm)")
ax1.set_ylabel("Atmospheric emissivity", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.set_ylim(0.6, 0.8)

#surface temperature vs. CO2 concentration
ax2 = ax1.twinx()
ax2.plot(c_plot, k2c(temp_values), label="Global average surface temperature", color="orange")
ax2.set_ylabel("Global average surface temperature (°C)", color="orange")
ax2.tick_params(axis="y", labelcolor="orange")
ax2.set_ylim(12.5, 16)  # Match MATLAB y-axis range for temperature

#annotation
lw = 2
ax1.axvline(c1, linestyle="--", color="black", linewidth=lw)
ax1.text(c1, 0.61, "1880–1900:\n294 ppm", rotation=90, verticalalignment="bottom", horizontalalignment="center")
ax1.axvline(c2, linestyle="--", color="black", linewidth=lw)
ax1.text(c2, 0.61, "2022:\n419 ppm", rotation=90, verticalalignment="bottom", horizontalalignment="center")
ax1.grid(visible=True, linestyle="--", linewidth=0.5)
fig.tight_layout()

# ==============================================================================
# Nominal Simulation
# ==============================================================================

#action (emissivity, from atmospheric CO2 concentration)
u_hat = eps + (410 - 315) / 60 * 0.05 / 280 * np.arange(1, K + 1)
#continuous-time disturbance (albedo and solar constant)
alpha_hat = alpha * np.ones(K)
wt_hat = (1 - alpha_hat) * S * np.pi * R**2 / C
#state
x0 = ((1 - alpha) * S / (4 * (1 - eps / 2) * sigma))**(1/4) #initial global average surface temperature, K
x_hat = nonlinear_climate_sim(t, x0, u_hat, wt_hat, beta) #global average surface temperature, K

# ==============================================================================
# True Simulation
# ==============================================================================

#action (emissivity, from atmospheric CO2 concentration)
u = np.zeros(K)
u[0] = u_hat[0]
for k in range(K - 1):
    u[k + 1] = u[k] - 0.5 * (u_hat[k + 1] - u_hat[k])
u *= (1 + 0.01 * np.sin(2 * np.pi * y[:K] / 10))  # Perturbed albedo

#continuous-time disturbance (scaled albedo and solar constant)
alpha_t = alpha * (1 + 0.01 * np.sin(y[:K])) # Perturbed albedo
wt = (1 - alpha_t) * S * np.pi * R**2 / C
x = nonlinear_climate_sim(t, x0, u, wt, beta) # global average surface temperature, K

fig, axs = plt.subplots(3, 1, figsize=(10, 12))
fig.subplots_adjust(hspace=0.5)

# First subplot: Atmospheric emissivity
axs[0].step(y[:K], u_hat, linestyle="--", color="k", label="Nominal")
axs[0].step(y[:K], u, color="b", label="True")
axs[0].set_ylabel("Atmospheric\nemissivity\n$u(t)$")
axs[0].legend(loc="upper left")

# Second subplot: Atmospheric albedo
axs[1].step(y[:K], alpha_hat, linestyle="--", color="k", label="Nominal")
axs[1].step(y[:K], alpha_t, color="b", label="True")
axs[1].set_ylabel("Atmospheric\nalbedo\n$\\alpha(t)$")
axs[1].legend(loc="upper left")

# Third subplot: Surface temperature
axs[2].plot(y, k2c(x_hat), linestyle="--", color="k", label="Nominal")
axs[2].plot(y, k2c(x), color="b", label="True")
axs[2].plot(y, k2c(linearized_climate_sim(t, x_hat, u_hat, u - u_hat, wt - wt_hat, beta)),
            marker="o", linestyle="none", color="magenta", label="Linearized")
axs[2].set_ylabel("Surface\ntemperature\n$x(t)$ (°C)")
axs[2].set_xlabel("Year")
axs[2].legend(loc="upper left")

# ==============================================================================
# linearized simulation
# ==============================================================================

# Control perturbation
du = u - u_hat

# Continuous-time disturbance perturbation
dwt = wt - wt_hat

# Linearized state
x_lin = linearized_climate_sim(t, x_hat, u_hat, du, dwt, beta)  #  Global average surface temperature perturbation, K

# Convert x_lin to Celsius
x_lin_celsius = k2c(x_lin)

# Error plot
plt.figure(3, figsize=(10, 6))
plt.plot(y, x_lin_celsius - k2c(x), "k")  # Difference between linearized and true
plt.ylabel("Prediction error $x^{\\rm lin}(t) - x(t)$ ($^\circ$C)")
plt.xlabel("Year")
plt.xlim([y[0], y[-1]])
plt.grid(visible=True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.pause(0.001)
plt.show()
