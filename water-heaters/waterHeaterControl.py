import numpy as np

def water_heater_control(x0, xMax, phMax, prMax, a, w, eta, alpha, xr):
    """
    % waterHeaterControl simulates control of an electric water heater
    % in any of three configurations: resistance only, heat pump only, or
    % hybrid resistance/heat pump.
    %
    % Input:
    %   x0, an initial tank energy in kWh
    %   xMax, a tank energy capacity in kWh
    %   phMax, a heat pump electrical power capacity in kW
    %   prMax, a resistor electrical power capacity in kW
    %   a, a discrete-time dynamics parameter
    %   w, a K vector of thermal power disturbances in kW
    %   eta, a K vector of heat pump coefficients of performance in kW
    %   alpha = 1/(R*C), a continuous-time dynamics parameter in 1/h
    %   xr, an energy threshold below which the resistor turns on in kWh
    %       (only relevant in the hybrid case)
    %
    % Output:
    %   x, a K+1 vector of energy states in kWh
    %   p, a K vector of total input electrical powers in kW
    """

    # data storage
    K = len(w)  # Number of time steps
    x = np.zeros(K + 1) # stored thermal energy, kWh
    x[0] = x0 # initial energy, kWh
    q = np.zeros(K) # thermal power supply to water, kW

    # simulation

    for k in range(K):
        # Resistance-only case
        # your
        # code
        # here

        # Heat-pump-only case
        # your
        # code
        # here

        # Hybrid case
        #
        # your
        #
        # code
        #
        # here
        #

        # Dynamic update
        # your code here

    # Input electrical power, kW
    # your code here

    return x, p