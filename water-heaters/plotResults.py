import numpy as np
import matplotlib.pyplot as plt


def plot_results(t, x, p, qd, xMin, xMax, phMax, prMax, xr, figNum):
    """
    % plotResults plots water heater simulation results.
    %
    % Input:
    %   t, a K+1 vector time span in h
    %   x, a K+1 vector of energy states in kWh
    %   p, a K vector of total input electrical powers in kW
    %   qd, a K vector of water withdrawal thermal powers in kW
    %   xMin, a minimum tank energy in kWh
    %   xMax, a tank energy capacity in kWh
    %   phMax, a heat pump electrical power capacity in kW
    %   prMax, a resistor electrical power capacity in kW
    %   xr, an energy threshold below which the resistor turns on in kWh
    %       (only relevant in the hybrid case)
    %   figNum, the figure number to plot into
    """
    # Define limits
    tLimits = [t[0], t[-1]]  # Time axis limits, hours
    tTicks = np.arange(t[0], t[-1] + 1, 6)  # Time axis ticks
    xLimits = [xMin, xMax]  # Energy axis limits, kWh
    pLimits = [0, np.ceil(phMax + prMax)]  # Electrical power axis limits, kW
    qLimits = [0, np.ceil(np.max(qd))]  # Electrical power axis limits, kW


    # Water withdrawal thermal power
    plt.figure(figNum, figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.step(t[:-1], qd, where='post')
    plt.grid(True)
    plt.xlim(tLimits)
    plt.xticks(tTicks, rotation=30)
    plt.ylim(qLimits)
    plt.ylabel("Thermal \n power \n draw \n (kW)")


    # Stored energy
    plt.subplot(3, 1, 2)
    plt.step(t, x, where='post')
    plt.grid(True)
    plt.xlim(tLimits)
    plt.xticks(tTicks, rotation=30)
    plt.ylim([xMin, xMax * 1.05])
    plt.ylabel("Stored \n thermal \n energy\n (kWh)")
    if phMax > 0 and prMax > 0:
        plt.axhline(y=xr, color='m', linestyle='--')
        plt.text(np.mean(t), xr, r'$x_r$', color='m', fontsize=12, verticalalignment='bottom',
                 horizontalalignment='right')

    # Charging power
    plt.subplot(3, 1, 3)
    plt.step(t[:-1], p, where='post')
    plt.grid(True)
    plt.xlim(tLimits)
    plt.xticks(tTicks, rotation=30)
    plt.ylim(pLimits)
    plt.ylabel("Electrical \n power \n (kW)")
    plt.xlabel("Hour (0 = midnight)")

    plt.tight_layout()
    plt.show()

