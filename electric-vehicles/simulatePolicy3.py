import numpy as np


def simulate_policy3(x0, z, p_chem_drive, a, tau, etac, etad, pc_max, x_max, x_min, t, h_deadline, x_star):
    """
    simulatePolicy3 simulates the third electric vehicle charging policy
    (when plugged in and below minimum charge, charge just fast enough to
    meet a deadline).

    Inputs:
        x0: the battery's initial chemical energy, kWh
        z: a K x 1 array of indicators that the vehicle is plugged in
        p_chem_drive: a K x 1 array of chemical powers discharged to drive, kW
        a: a scalar discrete-time dynamics parameter
        tau: the battery's self-dissipation time constant, h
        etac: the battery's charging efficiency
        etad: the battery's discharging efficiency
        pc_max: the battery's maximum charging electrical power, kW
        x_max: the battery's chemical energy capacity, kWh
        x_min: the minimum acceptable chemical energy, kWh
        t: the simulation time span, h
        h_deadline: the hour of day of the charging deadline (0 = midnight)
        x_star: the desired charge at the deadline, kWh

    Outputs:
        x3: a K+1 x 1 vector of stored chemical energies, kWh
        p3: a K x 1 vector of electrical charging powers, kW
    """
    # timing
    K = len(z)  # number of time steps
    dt = t[1] - t[0]  # time step duration, h

    # data storage
    x3 = np.zeros(K + 1)  # stored chemical energy, kWh
    x3[0] = x0  # initial state
    p_chem3 = -p_chem_drive  # chemical charging power, kW
    y3 = np.zeros(K)  # indicator of charging mode

    # simulation
    for k in range(K):
        # charging decision
        # y
        # o
        # u
        # r
        #
        # c
        # o
        # d
        # e
        #
        # h
        # e
        # r
        # e

        # dynamic update
        x3[k + 1] = a * x3[k] + (1 - a) * tau * p_chem3[k]

    p3 = np.maximum(p_chem3 / etac, etad * p_chem3)  # charging electrical power, kW
    p3[z == 0] = 0  # no electrical charging or discharging while unplugged

    return x3, p3
