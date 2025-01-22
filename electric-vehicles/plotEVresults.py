import matplotlib.pyplot as plt
import numpy as np

def plot_ev_results(t, x, p, z, x_max, x_min, pc_max, fig_num):
    """
    plotEVresults plots electric vehicle simulation results.

    Inputs:
        t: a K+1 vector time span in h
        x: a K+1 vector of stored energies in kWh
        p: a K vector of charging powers in kW
        z: a K vector of indicator variables that the vehicle is plugged in
        x_max: the battery capacity in kWh
        x_min: the minimum acceptable stored energy in kWh
        pc_max: the electric charging power capacity in kW
        fig_num: the figure number to plot into
    """
    # parameters
    K = len(t) - 1  # number of time steps
    t_lim = [t[0], t[-1]]  # time axis limits, h

    # energy plot
    plt.figure(fig_num, figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.step(t, x, where='post', color='k', linewidth=1.5)  # Proper step plot
    plt.xlim(t_lim)
    plt.ylim([0, x_max])
    plt.ylabel('Stored energy (kWh)')
    plt.axhline(y=x_min, color='m', linestyle='--', label='Minimum energy ($x_{min}$)')
    plt.text(np.mean(t_lim) / 4, x_min, '$x_{min}$', color='m',
             horizontalalignment='left', verticalalignment='top')
    plt.legend()
    plt.grid(True, linestyle='--')

    # charging power plot
    plt.subplot(2, 1, 2)
    plt.fill_between(t[:-1], 0, pc_max * z, color='0.95')
    plt.step(t[:-1], p, where='post', color='k', linewidth=1.5)
    plt.xlim(t_lim)
    plt.ylim([0, pc_max + 0.1])
    plt.ylabel('Charging power (kW)')
    plt.xlabel('Hour (0 = midnight)')
    plt.grid(True, linestyle='--')
    plt.tight_layout()
    plt.show()
