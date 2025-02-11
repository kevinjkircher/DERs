"""
%% introduction
% This script simulates closed-loop operation of an electric water heater
% in any of three configurations: resistance only, heat pump only, or
% hybrid resistance/heat pump.
%
% Kevin J. Kircher, Purdue University, 2025
%
Please make sure the following functions are available:
%   getWaterHeaterParameters.py (generates water heater parameters)
%   generateWaterDraws.py (generates random hot water draws)
%   plotResults.py (plots simulation results)
%   waterHeaterControl.py (students fill this in)
"""

# ==============================================================================
# Required imports
# ==============================================================================

import matplotlib.pyplot as plt
import numpy as np
from getWaterHeaterParameters import get_water_heater_parameters
from generateWaterDraws import generate_water_draws
from plotResults import plot_results
from waterHeaterControl import water_heater_control

# ==============================================================================
# Graphics settings
# ==============================================================================

plt.rc('font', size=20)
plt.rc('axes', titlesize=24, labelsize=18)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.rc('legend', fontsize=12)
plt.rc('figure', titlesize=20)
plt.rc('lines', linewidth=3)

### input data
# Water heater parameters
V = 0.19  # tank volume, m^3
U = 0.0005  # tank thermal transmittance, kW/m^2/C
R, C = get_water_heater_parameters(V, U)  # thermal capacitance C (kWh/C) and resistance R (C/kW)

# Timing
t0 = 0  # initial time, h
tf = 5 * 24  # final time, h
dt = 5 / 60  # time step, h
t = np.arange(t0, tf + dt, dt)  # time span, h
K = len(t) - 1  # number of time steps

# Water draws
n = 4  # number of occupants
qd = generate_water_draws(t, n)  # thermal power withdrawal, kW

# Parameters
Th = 52  # Hot water temperature, C
Tc = 15  # Inlet water temperature, C
xMin = 0  # Minimum thermal energy, kWh
xMax = C * (Th - Tc)  # Maximum thermal energy, kWh
x0 = xMax  # Initial state, kWh
alpha = 1 / (R * C)  # Continuous-time dynamics parameter, 1/h
a = np.exp(-alpha * dt)  # Discrete-time dynamics parameter
Ta = 20  # Ambient air temperature, Celsius
w = (Ta - Tc) / R - qd  # Disturbance, kW

### Resistance-only simulation
# parameters
prMax = 4.5  # Heating element capacity, kW
phMax = 0  # Heat pump capacity, kW
xr = xMax  # Energy threshold for resistor turn-on in hybrid case, kWh
eta = 3 * np.ones(K)  # Heat pump coefficient of performance
# simulation
x1, p1 = water_heater_control(x0, xMax, phMax, prMax, a, w, eta, alpha, xr)
# plots
plot_results(t, x1, p1, qd, xMin, xMax, phMax, prMax, xr, 1)

### Heat-pump-only simulation
# parameters
prMax = 0  # Heating element capacity, kW
phMax = 0.5  # Heat pump capacity, kW
xr = 0  # Energy threshold for resistor turn-on in hybrid case, kWh
# simulation
x2, p2 = water_heater_control(x0, xMax, phMax, prMax, a, w, eta, alpha, xr)
# plots
plot_results(t, x2, p2, qd, xMin, xMax, phMax, prMax, xr, 2)

### Hybrid simulation
# parameters
prMax = 4.5  # Heating element capacity, kW
phMax = 0.5  # Heat pump capacity, kW
xr = 0.5 * (xMax - xMin)  # Energy threshold for resistor turn-on in hybrid case, kWh
# simulation
x3, p3 = water_heater_control(x0, xMax, phMax, prMax, a, w, eta, alpha, xr)
# plots
plot_results(t, x3, p3, qd, xMin, xMax, phMax, prMax, xr, 3)