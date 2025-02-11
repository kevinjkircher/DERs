import numpy as np


def generate_water_draws(t, n):
    """
    %generateWaterDraws generates thermal power withdrawals from a domestic
    %hot water tank.

    %Parameters:
    %t : numpy array, The (K+1,) time span in hours.
    %n : The number of occupants.

    % Output:
    % qd : numpy array, The (K,) thermal power draw in kW.
    """
    # Get timing
    K = len(t) - 1  # Number of time steps
    dt = t[1] - t[0]  # Time step duration, hours

    # Set number of showers
    n_shower = n * round((t[-1] - t[0]) / 24)

    # Thermal power draw generation
    qd = np.zeros(K)  # Thermal power withdrawal, kW

    for _ in range(n_shower):
        # Generate a plausible time index for shower start
        is_valid = False  # Indicator of valid water withdrawal
        while not is_valid:
            k = np.random.randint(K)  # time index for shower start
            if ((5 <= t[k] % 24 <= 9) or (20 <= t[k] % 24 <= 22)) and np.max(qd[k:min(K, k + int(np.ceil((10/60) / dt)))]) == 0:
                # time is in morning or evening
                is_valid = True

        # Generate a plausible duration and thermal power
        duration = (7 + 6 * np.random.rand()) / 60  # Shower duration, hours
        power = 17 + 4 * np.random.rand()  # Thermal power withdrawal, kW
        energy = power * duration  # Heat withdrawal, kWh

        # Spread heat withdrawal over appropriate time steps
        if dt >= duration:
            qd[k] += energy / dt  # Spread energy evenly over time step
        else:
            while energy > 0:
                qd[k] += min(power, energy / dt)  # Spread remaining energy evenly over time step
                energy = max(0, energy - power * dt)  # Deduct spent energy
                k += 1  # Move to next time step
                if k >= K:
                    break

    return qd
