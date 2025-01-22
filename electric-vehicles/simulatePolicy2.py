import numpy as np

def simulate_policy2(x0, z, p_chem_drive, a, tau, etac, etad, pc_max, x_max, x_min):
    """
    simulatePolicy2 simulates the second electric vehicle charging policy
    (when plugged in and below minimum charge, charge at maximum until full).

    Inputs:
      x0, the battery's initial chemical energy, kWh
      z, a K x 1 of indicators that the vehicle is plugged in
      pChemDrive, a K x 1 of chemical powers discharged to drive, kW
      a, a scalar discrete-time dynamics parameter
      tau, the battery's self-dissipation time constant, h
      etac, the battery's charging efficiency
      etad, the battery's discharging efficiency
      pcMax, the battery's maximum charging electrical power, kW
      xMax, the battery's chemical energy capacity, kWh
      xMin, the minimum acceptable chemical energy, kWh

    Returns :
      x2, a K+1 x 1 vector of stored chemical energies, kWh
      p2, a K x 1 vector of electrical charging powers, kW
    """

    # dimensions
    K = len(z)

    # Initialization
    x2 = np.zeros(K + 1) # stored chemical energy, kWh
    x2[0] = x0 #initial state
    p_chem2 = -p_chem_drive # chemical charging power, kW
    y2 = np.zeros(K)  # Indicator for charging mode

    # Simulation
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
        x2[k + 1] = a * x2[k] + (1 - a) * tau * p_chem2[k]

    p2 = np.maximum(p_chem2 / etac, etad * p_chem2) # charging electrical power, kW

    p2[z == 0] = 0  # no electrical charging or discharging while unplugged

    return x2, p2
