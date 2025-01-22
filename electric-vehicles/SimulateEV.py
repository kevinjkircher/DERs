"""
Introduction:
This script simulates three charging policies for an electric vehicle.

Author: Kevin J. Kircher, Purdue University, 2025

Required Python Functions:
- generate_driving_power
- plotEVresults
- simulate_policy1 (students fill this in)
- simulate_policy2 (students fill this in)
- simulate_policy3 (students fill this in)

This script contains randomness in trip generation, which may lead to different results on each run.
However, the overall behavior should remain consistent.

Notes:
Ensure you install the required libraries before running the script
"""

# ==============================================================================
# Required imports
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from generateDrivingPower import generate_driving_power
from simulatePolicy1 import simulate_policy1
from simulatePolicy2 import simulate_policy2
from simulatePolicy3 import simulate_policy3
from plotEVresults import plot_ev_results

# ==============================================================================
# Graphics settings
# ==============================================================================
plt.rc('font', size=24)
plt.rc('axes', titlesize=24, labelsize=24)
plt.rc('xtick', labelsize=24)
plt.rc('ytick', labelsize=24)
plt.rc('legend', fontsize=12)
plt.rc('figure', titlesize=24)
plt.rc('lines', linewidth=3)


def full_stairs(tspan, u, **kwargs):
    u = np.append(u, u[-1])
    plt.step(tspan, u, where='post', **kwargs)

def simulate_ev():

    # timing
    t0 = 0  # initial time, h
    nd = 7  # number of days in time span
    tf = t0 + 24 * nd  # final time, h
    dt = 1/60  # time step duration, h
    t = np.linspace(t0, tf, int((tf - t0) / dt) + 1)  # time span, h
    K = len(t) - 1  # number of time steps

    # EV parameters
    tau = 1600  # self-dissipation time constant, h
    a = np.exp(-dt/tau)  # discrete-time dynamics parameter
    etac = 0.95  # charging efficiency
    etad = etac  # discharging efficiency
    pc_max = 11.5  # charging capacity, kW
    pd_max = 0  # discharging capacity, kW
    x_max = 80  # energy capacity, kWh
    x0 = x_max  # initial energy, kWh
    x_min = 0.5 * x_max  # minimum acceptable energy capacity, kWh
    alph = 0.3 * np.ones(K)  # energy intensity of driving, kWh/km

    # generate discharge powers for driving
    pChemDrive = generate_driving_power(t, alph)  # chemical power discharged to drive EV, kW

    # plugged-in hours
    z = np.zeros(K)  # indicator that vehicle is plugged in
    z[np.mod(t[:K], 24) < 6] = 1  # plug in overnight
    z[np.mod(t[:K], 24) > 20] = 1  # plug in overnight
    z[pChemDrive > 0] = 0  # unplug if vehicle is driving

    # input signal plot
    t_lim = [t0, tf]  # time axis limits, h
    e_lim = [0, x_max]  # energy axis limits, kWh
    p_lim = [0, pc_max]  # electric power axis limits, kW
    pChemLim = [0, np.ceil(np.max(pChemDrive) / 5) * 5]  # chemical power axis limits, kW

    # driving power plot with plugged-in periods shaded
    plt.figure(figsize=(10, 5))
    plt.fill_between(t[:K], max(pChemLim) * z, color='0.95', step='post')
    full_stairs(t, pChemDrive, color='k')
    plt.xlim(t_lim)
    plt.ylim(pChemLim)
    plt.ylabel('Power discharged for driving (kW)')
    plt.xlabel('Hour (0 = midnight)')
    plt.grid()
    plt.show()


    # policy 1: when plugged in, charge at maximum until full
    # simulation
    x1, p1 = simulate_policy1(x0, z, pChemDrive, a, tau, etac, etad, pc_max, x_max)

    # plot simulation results
    plot_ev_results(t, x1, p1, z, x_max, x_min, pc_max, 2)

    # policy 2: when energy gets low, charge at maximum until full
    # simulation
    x2, p2 = simulate_policy2(x0, z, pChemDrive, a, tau, etac, etad, pc_max, x_max, x_min)

    # plot simulation results
    plot_ev_results(t, x2, p2, z, x_max, x_min, pc_max, 3)

    # policy 3: when energy gets low, charge at constant power to meet deadline
    # parameters
    h_deadline = 6  # hour of day of charging deadline, h
    x_star = x_max  # charging target, kWh

    # simulation
    x3, p3 = simulate_policy3(x0, z, pChemDrive, a, tau, etac, etad, pc_max, x_max, x_min, t, h_deadline, x_star)

    # plot simulation results
    plot_ev_results(t, x3, p3, z, x_max, x_min, pc_max, 4)

    plt.show()

if __name__ == "__main__":
    simulate_ev()
