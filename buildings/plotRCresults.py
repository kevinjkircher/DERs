import matplotlib.pyplot as plt
import numpy as np


def plot_rc_results(t, Tset, T, Tm, Qdotc, fig_num):
    """
    % plotRCresults plots RC thermal circuit simulation results.
    %
    % Input:
    %   t, the K vector time span in h
    %   Tset, the indoor temperature setpoint in C
    %   T, the K+1 vector indoor air temperature in C
    %   Tm, the K+1 vector thermal mass temperature in C
    %   Qdotc, the K vector HVAC thermal power in kW
    %   figNum, the figure number to plot into
    """

    # parameters
    t_lim = [t[0], t[-1]]  # Time axis limits, h
    T_lim = [np.floor(np.min(Tset)), np.ceil(np.max(Tset)) + 1]  # Temperature axis limits

    plt.figure(fig_num)
    plt.clf()

    # Temperature plot
    plt.subplot(2, 1, 1)
    plt.step(t, T, 'k', where='post', label='Air')
    plt.step(t, Tm, 'r', where='post', label='Mass')
    plt.step(t, Tset, 'm--', where='post', label='Setpoint')
    plt.xlim(t_lim)
    plt.ylim(T_lim)
    plt.ylabel('Temperature \n (°C)')
    #plt.legend(['Air', 'Mass', 'Setpoint'], loc='upper center', ncol=3, frameon=False)
    plt.legend(['Air', 'Mass', 'Setpoint'], loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3, frameon=False)

    # Thermal power plot
    plt.subplot(2, 1, 2)
    plt.step(t, Qdotc, 'k', where='post')
    plt.xlim(t_lim)
    plt.ylabel('Thermal Power \n (kW)')
    plt.xlabel('Hour (0 = midnight)')

    plt.tight_layout()
    plt.show()
