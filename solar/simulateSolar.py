
"""
introduction:
This script simulates residential electricity demand and solar photovoltaic power output.
It computes the annual cost savings from solar under one-to-one net metering and
net metering with a reduced buyback price.

Author: Kevin J. Kircher, Purdue University, 2025

Required Files:
- west-lafayette-2022-weather.csv (Oikolab weather data CSV)
- MFRED-2019-NYC-Apartments-Electricity-Data.csv (MFRED electricity data CSV)
- configureGraphics.py (configures graphics settings)
- importWeather.py (imports Oikolab weather data from CSV)
- importElectricity.py (imports MFRED electric power data from CSV)
- generateElectricityDemand.py (generates electricity demand time series)
- solarAngles.py (computes solar azimuth and elevation angles)
- surfaceIrradiance.py (computes irradiance on surfaces)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from importWeather import import_weather
from generateElectricityDemand import generate_electricity_demand
from solarAngles import solar_angles
from surfaceIrradiance import surface_irradiance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker  # Import ticker for formatting

# ==============================================================================
# graphics settings
# ==============================================================================

plt.rc('font', size=22)
plt.rc('axes', titlesize=20, labelsize=18)
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
plt.rc('legend', fontsize=18)
plt.rc('figure', titlesize=22)
plt.rc('lines', linewidth=3)

# ==============================================================================
# input data
# ==============================================================================

# timing
dt = 0.25  # time step, h
t_span = pd.date_range(start='2022-01-01', end='2022-12-31 23:00:00', freq=f'{int(dt*60)}T') # time span as datetime
K = len(t_span)  # number of time steps
t = np.arange(0, K * dt, dt)  # time span as floating-point, h

# weather data import
weather_file = 'west-lafayette-2022-weather.csv'  # weather file name
theta, total_horizontal, beam_normal, diffuse_horizontal, offset_gmt = import_weather(weather_file, t_span)  # weather data import

# ==============================================================================
# building electricity demand
# ==============================================================================

electricity_file = 'MFRED-2019-NYC-Apartments-Electricity-Data.csv'  # electricity file name
Af = 200  # floor area, m^2
N = 2  # number of stories
to_plot = 1  # indicator of whether to plot simulation data and results
p = generate_electricity_demand(t_span, electricity_file, Af, N, theta, total_horizontal, to_plot)  # total electricity demand, kW

# ==============================================================================
# irradiance
# ==============================================================================

# solar angles
lat = 40.4259  # latitude, degrees
t_long = -86.9081  # longitude, degrees
el, az = solar_angles(lat, t_long, t_span, offset_gmt)  # sun elevation and azimuth angles, degrees

# surface irradiance
bet = lat  # surface tilt angle, degrees
az0 = 0  # surface azimuth angle, degrees
Stot, Sb, Sd = surface_irradiance(az, el, az0, bet, beam_normal, diffuse_horizontal)  # total, beam, and diffuse irradiance on surface, kW/m^2

# irradiance plot
p_lim = [0, 1]
t_lim = [t_span[0], t_span[-1]]
plt.figure(4, figsize=(10, 6), constrained_layout=True)
irradiance_data = [(Stot, 'Total surface\nirradiance\n(kW/m$^2$)', p_lim, [0, 0.5, 1]),
                   (Sb, 'Beam surface\nirradiance\n(kW/m$^2$)', p_lim, [0, 0.5, 1]),
                   (Sd, 'Diffuse surface\nirradiance\n(kW/m$^2$)', p_lim, [0, 0.5, 1])]

for i, (y_data, ylabel, ylim, yticks) in enumerate(irradiance_data, start=1):
    ax = plt.subplot(3, 1, i)
    plt.plot(t_span, y_data, 'k', linewidth=2)
    plt.grid(True)
    ax.set_ylabel(ylabel, labelpad=10, loc='center', fontname='serif')
    ax.set_ylim(ylim)
    ax.set_yticks(yticks)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x)}' if x.is_integer() else f'{x}'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.text(t_span[-1], ylim[0] - 0.4, '2022', fontsize=16, ha='right', va='center', fontname='serif')
plt.draw()


# ==============================================================================
# solar power supply
# ==============================================================================

# solar array efficiency
rated_eta = 0.18  # rated solar array efficiency
rated_t = 25  # rated temperature, C
zero_t = 270  # temperature at which power output stops, C
solar_eta = np.nan
# ^^^^ YOUR CODE HERE ^^^^

# solar power supply
panel_a = Af / 4  # solar panel area, m^2
p_sun = panel_a * solar_eta * Stot  # solar power supply, kW

# Power plot
plt.figure(5, figsize=(10, 6), constrained_layout=True)
data = [(p, 'Power demand\n(kW)', (0, 10), [0, 5, 10]),
        (p_sun, 'Solar power\nsupply (kW)', (0, 10), [0, 5, 10]),
        (p - p_sun, 'Net power\ndemand (kW)', (-10, 10), [-10, 0, 10])]

for i, (y_data, ylabel, ylim, yticks) in enumerate(data, start=1):
    ax = plt.subplot(3, 1, i)
    plt.plot(t_span, y_data, 'k', linewidth=2)
    plt.grid(True)
    ax.set_ylabel(ylabel, labelpad=10, loc='center', fontname='serif')
    ax.set_ylim(ylim)
    ax.set_yticks(yticks)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.text(t_span[-1], ylim[0] - 5, '2022', fontsize=16, ha='right', va='center', fontname='serif')

plt.draw()


# ==============================================================================
# electricity costs
# ==============================================================================

# cost without solar
pi_buy = 0.15  # price at which user buys electricity, $/kWh
c1 = round(pi_buy * dt * np.sum(p))  # electricity cost, $

print('--------------------------------------------------------------')
print(f'Electricity cost without solar: ${c1}.')

# cost with one-to-one net metering
c2 = round(pi_buy * dt * np.sum(p - p_sun))  # electricity cost, $
print(f'Electricity cost with solar and one-to-one net metering: ${c2}.')
print(f'Cost reduction from solar with one-to-one net metering: ${c1 - c2} ({round(100 * (1 - c2 / c1))}%).')

# cost with reduced net metering
pi_sell = 0.03  # reduced price at which user sells electricity, $/kWh
c3 = np.nan
# ^^^^ YOUR CODE HERE ^^^^

print(f'Electricity cost with solar and reduced net metering: ${c3}.')
print(f'Cost reduction from solar with reduced net metering: ${c1 - c3} ({round(100 * (1 - c3 / c1))}%).')

plt.ioff()
plt.show()