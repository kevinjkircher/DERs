function [R,C] = getWaterHeaterParameters(V,U)
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

% geometry
h = 1.5; % tank height, m
r = sqrt(V./(pi*h)); % tank radius, m
A = 2*V.*(1./r + 1./h); % tank wall surface area, m^2

% thermal resistance and capacitance
R = 1./(U.*A); % tank wall thermal resistance, C/kW
C = 1.2*V; % tank thermal capacitance, kWh/C

end

