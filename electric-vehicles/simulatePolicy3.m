function [x3,p3] = simulatePolicy3(x0,z,pChemDrive,a,tau,etac,etad,pcMax,xMax,xMin,t,hDeadline,xStar)
% simulatePolicy3 simulates the third electric vehicle charging policy
% (when plugged in and below minimum charge, charge just fast enough to
% meet a deadline).
%
% Inputs:
%   x0, the battery's initial chemical energy, kWh
%   z, a K x 1 of indicators that the vehicle is plugged in
%   pChemDrive, a K x 1 of chemical powers discharged to drive, kW
%   a, a scalar discrete-time dynamics parameter
%   tau, the battery's self-dissipation time constant, h
%   etac, the battery's charging efficiency
%   etad, the battery's discharging efficiency
%   pcMax, the battery's maximum charging electrical power, kW
%   xMax, the battery's chemical energy capacity, kWh
%   xMin, the minimum acceptable chemical energy, kWh
%   t, the simulation time span, h
%   hDeadline, the hour of day of the charging deadline (0 = midnight)
%   xStar, the desired charge at the deadline, kWh
%
% Outputs:
%   x3, a K+1 x 1 vector of stored chemical energies, kWh
%   p3, a K x 1 vector of electrical charging powers, kW

% timing
K = length(z); % number of time steps
dt = t(2) - t(1); % time step duration, h

% initialization
x3 = zeros(K+1,1); % stored chemical energy, kWh
x3(1) = x0; % initial state
pChem3 = -pChemDrive; % chemical charging power, kW (initialized with power used for driving)
y3 = zeros(K,1); % indicator of charging mode

% simulation
for k=1:K
    % charging decision
    %
    % y
    % o 
    % u 
    % r
    %
    %
    % c
    % o 
    % d 
    % e
    %
    %
    % h
    % e 
    % r 
    % e
    %
    
    % dynamic update
    x3(k+1) = a*x3(k) + (1-a)*tau*pChem3(k);
end
p3 = max(pChem3/etac,etad*pChem3); % charging electrical power, kW
p3(z==0) = 0; % no electrical charging or discharging while unplugged

end

