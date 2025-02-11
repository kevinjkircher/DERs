import numpy as np


def get_water_heater_parameters(V, U):
    """
    % getWaterHeaterParameters defines the thermal resistance and capacitance
    % based on the tank volume and thermal transmittance.
    %
    % Inputs:
    %   V, the water volume in m^3
    %   U, the tank wall thermal transmittance in kW/m^2/C
    %
    % Outputs:
    %   R, the tank wall thermal resistance in C/kW
    %   C, the water thermal resistance in kWh/C
    """
    # Geometry
    h = 1.5  # Tank height, meters
    r = np.sqrt(V / (np.pi * h))  # Tank radius, meters
    A = 2 * V * (1 / r + 1 / h)  # Tank wall surface area, m^2

    # Thermal resistance and capacitance
    R = 1 / (U * A)  # Tank wall thermal resistance, C/kW
    C = 1.2 * V  # Tank thermal capacitance, kWh/C

    return R, C
