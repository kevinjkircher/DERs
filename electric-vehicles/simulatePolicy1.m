function [x1,p1] = simulatePolicy1(x0,z,pChemDrive,a,tau,etac,etad,pcMax,xMax)
% simulatePolicy1 simulates the first electric vehicle charging policy
% (when plugged in, charge at maximum until full).
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
%
% Outputs:
%   x1, a K+1 x 1 vector of stored chemical energies, kWh
%   p1, a K x 1 vector of electrical charging powers, kW

% timing
K = length(z); % number of time steps

% initialization
x1 = zeros(K+1,1); % stored chemical energy, kWh
x1(1) = x0; % initial state
pChem1 = -pChemDrive; % chemical charging power, kW (initialized with power used for driving)

% simulation
for k=1:K
    % charging decision
    % your 
    % code 
    % here 
    
    % dynamic update
    x1(k+1) = a*x1(k) + (1-a)*tau*pChem1(k);
end
p1 = max(pChem1/etac,etad*pChem1); % charging electrical power, kW

end

