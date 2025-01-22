import numpy as np

def simulate_policy1(x0, z, p_chem_drive, a, tau, etac, etad, pc_max, x_max):
    """
    Simulates the first electric vehicle charging policy
    (when plugged in, charge at maximum until full).
    Parameters:
    x0: The battery's initial chemical energy, kWh
    z: A K x 1 of indicators that the vehicle is plugged in
    p_chem_drive:  a K x 1 of chemical powers discharged to drive, kW
    a: A scalar discrete-time dynamics parameter
    tau: The battery's self-dissipation time constant, h
    etac: The battery's charging efficiency
    etad: The battery's discharging efficiency
    pc_max: The battery's maximum charging electrical power, kW
    x_max: The battery's chemical energy capacity, kWh

    Returns:
   x1, a K+1 x 1 vector of stored chemical energies, kWh
   p1, a K x 1 vector of electrical charging powers, kW

    """

    # dimensions
    K = len(z)

    # initialization
    x1 = np.zeros(K + 1) #stored chemical energy, kWh
    x1[0] = x0 #initial state
    p_chem1 = -p_chem_drive #chemical charging power, kW (initialized with power used for driving)

    # simulation
    for k in range(K):
        # charging decision
        # your
        # code
        # here



        # dynamic update
        x1[k + 1] = a * x1[k] + (1 - a) * tau * p_chem1[k]

    p1 = np.maximum(p_chem1 / etac, etad * p_chem1) #charging electrical power, kW
    p1[z == 0] = 0 # no electrical charging or discharging while unplugged

    return x1, p1