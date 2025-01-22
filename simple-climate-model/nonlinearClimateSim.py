import numpy as np
from scipy.integrate import solve_ivp


def nonlinear_climate_sim(t, x0, u, wt, beta):
    """
    Simulates nonlinear climate dynamics.

    Args:
        t (array-like): Time span in seconds.
        x0 (float): Initial global average surface temperature in K.
        u (np.ndarray): K vector of atmospheric emissivities.
        wt (np.ndarray): K vector of continuous-time disturbances in K/s.
        beta (float): Parameter in K^3/s.

    Returns:
        x: K+1 vector of global average surface temperatures in K.
    """
    K = len(u)  # Number of time steps
    # Ensure input is a 1D vector
    if u.ndim != 1 or wt.ndim != 1:
        raise ValueError("u and wt must be 1D arrays (vectors).")

    # Initialize output array
    x = np.zeros(K + 1)  #  K+1 vector for global average surface temperatures in K
    x[0] = x0  # Initial state

    # Perform the simulation
    for k in range(K):
        # your
        # code
        # here

    return x
