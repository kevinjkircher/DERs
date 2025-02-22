import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from importElectricty import import_electricity  # Assuming this function exists

import matplotlib.dates as mdates

def generate_electricity_demand(t_span, electricity_file, Af, N, theta, total_horizontal, to_plot):
    # generateElectricityDemand generates an electricity demand profile for a
    # building, including heating/cooling equipment and everything else, over a
    # given time span.

    # Input:
    #   t_span, the K x 1 time span as a datetime object
    #   electricity_file, a string containing the electricity data file name
    #   Af, the floor area, m^2
    #   N, the number of stories
    #   theta, the K x 1 outdoor temperature, C
    #   total_horizontal, the K x 1 total horizontal solar irradiance, kW/m^2
    #   to_plot, an indicator of whether to plot simulation data and results

    # Output:
    #   p, a K x 1 vector of total electricity demand, kW

    # timing
    K = len(t_span)  # number of time steps
    dt = (t_span[1] - t_span[0]).total_seconds() / 3600  # time step, h

    # electricity data import
    t_elec = t_span.copy()
    t_elec = t_elec.map(lambda t: t.replace(year=2019))  # electricity time span (data are from 2019)
    plug_powers = import_electricity(electricity_file, t_elec)  # 'everything else' electricity data import
    plug_powers = plug_powers * (0.005 * Af / np.mean(plug_powers, axis=0)) # plug powers rescaled by floor area to 5 W/m^2, kW


    # 1R1C building model parameters
    C = 0.0125 * Af  # air thermal capacitance, kWh/C
    R = 1 / (0.016 * np.sqrt(N * Af))  # indoor-outdoor thermal resistance, C/kW
    a = np.exp(-dt / (R * C))  # discrete-time dynamics parameter

    # indoor temperature setpoint
    is_winter = (t_span <= pd.Timestamp("2022-04-15")) | (t_span >= pd.Timestamp("2022-10-15"))  # indicator of heating season
    is_summer = (t_span >= pd.Timestamp("2022-05-01")) & (t_span <= pd.Timestamp("2022-09-30"))  # indicator of cooling season
    T_set = np.full(K, 21)  # indoor temperature setpoint, C
    T_set[is_summer] = 25  # cooling temperature setpoint, C

    # heat pump coefficient of performance
    eta = np.ones(K)  # heat pump coefficient of performance (initialized at 1 to avoid dividing qc by 0 when calculating p)
    eta[is_winter] = np.maximum(1, 0.0449 * theta[is_winter] + 2.57)  # heating COP
    eta[is_summer] = 0.197 * theta[is_summer] - 10.3  # cooling COP

    # coefficient of performance plot
    if to_plot:
        plt.figure(1, figsize=(8, 6))
        plots = [
            (theta, 'Outdoor\ntemperature (°C)', [-20, 0, 20, 40]),
            (eta, 'Heat pump coefficient\nof performance',
             np.arange(np.floor(min(eta)), np.ceil(max(eta)) + 1, step=5))
        ]

        for i, (y_data, ylabel, yticks) in enumerate(plots, 1):
            ax = plt.subplot(2, 1, i)
            plt.plot(t_span, y_data, 'k', linewidth=2)
            ax.set(ylabel=ylabel, yticks=yticks)
            ax.tick_params(axis='both', labelsize=16)
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            ax.grid(True)
            if i == 2:
                ax.text(t_span[-1], min(eta) - 4, '2022', fontsize=16, ha='right', va='center', fontname='serif')


    # exogenous thermal power
    i_power = plug_powers.shape[1] - 5 # index of power profile
    c = np.full(K, 0.8)  # solar heat gain coefficient
    c[is_summer] = 0.5  # lower SHGC in summer to emulate shading

    qe = (plug_powers[:, i_power] + 0.19 * np.sqrt(N * Af) * c * total_horizontal
          + 0.5 + (0.25 / 3) * np.random.randn(K))  # from everything else

    # exogenous thermal power plot
    if to_plot:
        plt.figure(2, figsize=(8, 6))
        plots = [
            (plug_powers[:, i_power], 'Plug\npower (kW)'),
            (qe, 'Exogenous thermal\npower (kW)')
        ]

        for i, (y_data, ylabel) in enumerate(plots, 1):
            ax = plt.subplot(2, 1, i)
            plt.plot(t_span, y_data, 'k', linewidth=2)
            ax.set(ylabel=ylabel)
            ax.tick_params(axis='both', labelsize=16)
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            ax.grid(True)
            if i == 2:
                ax.text(t_span[-1], min(qe) - 3, '2022', fontsize=16, ha='right', va='center', fontname='serif')


    # heat pump sizing
    kd = np.argmin(np.abs(theta - np.quantile(theta, 0.01)))  # time index of design condition
    p_max = 1.2 * ((T_set[kd] - theta[kd]) / R - qe[kd]) / eta[kd]  # heat pump electric power capacity, kW
    qc_max = np.zeros(K)  # maximum heat pump thermal power, kW
    qc_max[is_winter] = p_max * eta[is_winter]  # nonzero heating capacity in winter
    qc_min = np.zeros(K)  # minimum heat pump thermal power, kW
    qc_min[is_summer] = p_max * eta[is_summer]  # nonzero cooling capacity in summer

    # data storage
    T = np.zeros(K + 1)  # indoor temperature, C
    T[0] = T_set[0]  # initial state, C
    qc = np.zeros(K)  # heat pump thermal power, kW

    # thermal simulation
    for k in range(K):
        # thermal load to exactly track setpoint
        lk = ((T_set[min(k + 1, K - 1)] - a * T[k]) / (1 - a) - theta[k]) / R - qe[k]  # thermal load, kW

        # heat pump thermal power
        qc[k] = np.clip(lk, qc_min[k], qc_max[k])  # heat pump thermal power, kW
        if not (is_winter[k] or is_summer[k]):  # if it's not heating or cooling season
            qc[k] = 0  # turn heat pump off

        # temperature update
        T[k + 1] = a * T[k] + (1 - a) * (theta[k] + R * (qc[k] + qe[k]))  # C

    # electric power simulation
    p = plug_powers[:, i_power] + qc / eta  # total building electrical load, kW

    # building simulation results plot
    if to_plot:
        plt.figure(3, figsize=(8, 6))
        plots = [
            (T[:-1], 'Indoor\ntemperature\n(°C)', None),
            (qc, 'Heat pump\nthermal power\n(kW)', None),
            (p, 'Total electrical\npower (kW)', [0, 5, 10])
        ]

        for i, (y_data, ylabel, yticks) in enumerate(plots, 1):
            ax = plt.subplot(3, 1, i)
            plt.plot(t_span, y_data, 'k', linewidth=2)
            ax.set_ylabel(ylabel, labelpad=10, loc='center', fontname='serif', fontsize=20)
            ax.tick_params(axis='both', labelsize=16)
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            ax.grid(True)
            if yticks is not None:
                ax.set_yticks(yticks)
            if i == 3:
                ax.text(t_span[-1], min(p) - 3, '2022', fontsize=16, ha='right', va='center', fontname='serif')

    return p
