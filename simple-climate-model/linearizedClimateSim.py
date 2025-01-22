import numpy as np


def linearized_climate_sim(t, x_hat, u_hat, du, dwt, beta):
    """
    Simulates linearized climate dynamics.

    Args:
        t (array-like): Time span in seconds.
        x_hat (np.ndarray): K+1 vector of nominal global average surface temperatures in K.
        u_hat (np.ndarray): K vector of nominal atmospheric emissivities.
        du (np.ndarray): K vector of atmospheric emissivity perturbations.
        dwt (np.ndarray): K vector of continuous-time disturbance perturbations in K/s.
        beta (float): Parameter in K^3/s.

    Returns:
        xLin, a K+1-vector of approximate global average surface temperatures in K.
    """
    K = len(u_hat)  # Number of time steps
    dx = np.zeros_like(x_hat)  # global average surface temperature perturbations in K

    for k in range(K):
        # y
        # o
        # u
        # r

        # c
        # o
        # d
        # e

        # h
        # e
        # r
        # e

    x_lin = x_hat + dx  # Approximate global average surface temperatures
    return x_lin
