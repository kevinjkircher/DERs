function [x2,p2] = simulatePolicy2(x0,z,pChemDrive,a,tau,etac,etad,pcMax,xMax,xMin)
% simulatePolicy2 simulates the second electric vehicle charging policy
% (when plugged in and below minimum charge, charge at maximum until full).
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
%
% Outputs:
%   x2, a K+1 x 1 vector of stored chemical energies, kWh
%   p2, a K x 1 vector of electrical charging powers, kW

% dimensions
K = length(z);

% initialization
x2 = zeros(K+1,1); % stored chemical energy, kWh
x2(1) = x0; % initial state
pChem2 = -pChemDrive; % chemical charging power, kW
y2 = zeros(K,1); % indicator of charging mode

% simulation
for k=1:K
    % charging decision
    % y
    % o 
    % u 
    % r
    %
    % c
    % o 
    % d 
    % e
    %
    % h
    % e 
    % r 
    % e
    
    % dynamic update
    x2(k+1) = a*x2(k) + (1-a)*tau*pChem2(k);
end
p2 = max(pChem2/etac,etad*pChem2);  % charging electrical power, kW

end

