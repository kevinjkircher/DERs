function [x,p] = waterHeaterControl(x0,xMax,phMax,prMax,a,w,eta,alpha,xr)
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

% data storage
K = length(w); % number of time steps
x = zeros(K+1,1); % stored thermal energy, kWh
x(1) = x0; % initial energy, kWh
q = zeros(K,1); % thermal power supply to water, kW

% simulation
for k=1:K
    % resistance-only case
    % your
    % code
    % here
    
    % heat-pump-only case
    % your
    % code
    % here
    
    % hybrid case
    %
    % your
    %
    % code
    %
    % here
    %
    
    % dynamic update
    % your code here
end
% input electrical power, kW
% your code here

end

