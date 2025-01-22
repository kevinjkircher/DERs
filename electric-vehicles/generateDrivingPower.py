import numpy as np


def generate_driving_power(t, alpha):
    """
    generateDrivingPower generates a time series of chemical power discharged
    to drive an electric vehicle.

    Inputs:
        t: the K+1 vector time span in h
        alpha: the K vector energy intensity of driving in kWh/km

    Output:
        p_chem_drive: a K vector of chemical powers discharged to drive in kW
    """
    # timing
    K = len(t) - 1  # number of time steps
    dt = t[1] - t[0]  # time step duration, h
    nd = K * dt / 24  # number of days in time span
    if nd % 1 != 0:
        raise ValueError('The time span must contain an integer number of days.')

    # reshape energy intensity
    alpha = np.reshape(alpha, (int(K / nd), int(nd)))

    # generate discharge powers for driving
    nt = 3  # number of trips per day
    p_chem_drive = np.zeros((int(K / nd), int(nd)))  # chemical discharge powers for driving, kW
    d_trip = np.zeros((nt, int(nd)))  # trip distances, km
    for j in range(int(nd)):  # day index
        for i in range(nt):  # trip index
            # generate trip start time of day
            h_start = 6 + 14 * np.random.rand()  # trip start time of day, h
            k_start = int(h_start // dt)  # trip start time of day index
            while p_chem_drive[k_start, j] > 0:
                h_start = 6 + 14 * np.random.rand()  # trip start time of day, h
                k_start = int(h_start // dt)  # trip start time of day index

            # generate trip distance
            d_trip[i, j] = min(100, np.random.lognormal(1.8, 1.24))  # trip distance, km

            # set trip speed
            if d_trip[i, j] < 15:
                s_trip = 40  # short trip speed, km/h
            else:
                s_trip = 90  # long trip speed, km/h

            # set trip duration
            t_trip = d_trip[i, j] / s_trip  # trip duration, h

            # spread trip discharge energy over the appropriate time steps
            while t_trip > 0:
                p_chem_drive[k_start, j] = alpha[k_start, j] * s_trip * min(dt, t_trip) / dt
                t_trip -= min(dt, t_trip)
                k_start += 1

    # rewrite matrix as stacked vector
    p_chem_drive = p_chem_drive.flatten('F')

    return p_chem_drive
