"""
%% introduction
This script models a building as a 2R2C thermal circuit and simulates its
dynamics both exactly and using a two-timing approximation.

Author: Kevin J. Kircher, Purdue University, 2025

Please make sure the following functions are available:
    importWeather.py (imports weather data)
    importElectricity.py (imports electricity load data)
    plotResults.py (plots simulation results)
    perfectTrackingControl.py (students fill this in)
    thermostaticControl.py (students fill this in)
"""

# ==============================================================================
# Required imports
# ==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from perfectTrackingError import perfect_tracking_control
from thermostaticControl import thermostatic_control
from plotRCresults import plot_rc_results
from scipy.linalg import expm
from importWeather import import_weather
from importElectricty import import_electricity


# ==============================================================================
# Graphics settings
# ==============================================================================

plt.rc('font', size=20)
plt.rc('axes', titlesize=24, labelsize=20)
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
plt.rc('legend', fontsize=12)
plt.rc('figure', titlesize=20)
plt.rc('lines', linewidth=3)


# ==============================================================================
# Parameters
# ==============================================================================
# Geometry
Af = 200  # floor area, m^2
N = 2  # number of stories

# Thermal capacitances
C = 0.0125 * Af  # air thermal capacitance, kWh/C
Cm = 12 * C  # mass thermal capacitance, kWh/C

# Thermal resistances
R = 1 / (0.016 * np.sqrt(N * Af))  # indoor-outdoor thermal resistance, C/kW
Rm = R / 6  # indoor-mass thermal resistance, C/kW

# Timing
dt = 0.25 #time step, h
t_span = pd.date_range("2022-12-22", "2022-12-27", freq="15T") #time span as datetime
K = len(t_span) # number of time steps
t = np.arange(0, K * dt, dt) # time span, h

# Heater capacity constraints
qcMin = np.zeros(K) #minimum HVAC thermal power, kW
qcMax = 14 * np.ones(K) #maximum HVAC thermal power, kW

# ==============================================================================
# 2R2C model
# ==============================================================================
# Continuous-time dynamics matrices
Ac = np.zeros((2, 2))  # continuous-time dynamics matrix
Bc = np.zeros((2, 1))  # continuous-time input matrix

# your
#
# code
#
# here

# Discrete-time dynamics matrices
# your code
# here


# ==============================================================================
# Input signals
# ==============================================================================
# Weather data import
weather_file = 'west-lafayette-2022-weather.csv'
Tout, I = import_weather(weather_file, t_span)

# Electricity data import
electricity_file = 'MFRED-2019-NYC-Apartments-Electricity-Data.csv'
t_elec = t_span.map(lambda x: x.replace(year=2019))
plug_powers = import_electricity(electricity_file, t_elec)

# Exogenous thermal power
qe = (plug_powers[:, np.random.randint(plug_powers.shape[1])] +  # from plugged-in devices
      0.19 * np.sqrt(N * Af) * I +  # from the sun
      1 + (0.5 / 3) * np.random.randn(K))  # from everything else
# Disturbance
w = qe + Tout / R  # kW

# Indoor temperature setpoint
Tset = 21 * np.ones(len(t) + 1) #day indoor temperature setpoint, C
Tset[:len(t)][np.mod(t, 24) < 6] = 18.5 #night setpoint, C
Tset[:len(t)][np.mod(t, 24) > 22] = 18.5 #night setpoint, C

# %% input signal plot
plt.figure(1)
plt.clf()

# First subplot (Outdoor Temperature)
ax1 = plt.subplot(2, 1, 1)
plt.plot(t_span, Tout, 'k')
plt.ylabel('Outdoor \n temperature \n (°C)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))

# Second subplot (Exogenous Thermal Power)
ax2 = plt.subplot(2, 1, 2)
plt.plot(t_span, qe, 'k')
plt.ylabel('Exogenous \n thermal power \n (kW)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))

plt.tight_layout()
plt.show()

# ==============================================================================

# %% (near-) perfect tracking simulation
# initial state
T0 = np.array([Tset[0], np.mean(Tset)])  # initial air and mass temperature, C

# simulation
T1, qc1 = perfect_tracking_control(A, B, w, T0, Tset, qcMin, qcMax)

# plot results
plot_rc_results(t, Tset[:-1], T1[0, :-1], T1[1, :-1], qc1, 2)

# ==============================================================================

# %% thermostatic control simulation
# simulation
dT = 0.5  # thermostat deadband halfwidth, C
T2, qc2 = thermostatic_control(A, B, w, T0, Tset, qcMin, qcMax, dT)

# plot results
plot_rc_results(t, Tset[:-1], T2[0, :-1], T2[1, :-1], qc2, 3)
