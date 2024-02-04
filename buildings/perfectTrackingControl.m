function [T,qc] = perfectTrackingControl(A,B,w,T0,Tset,qcMin,qcMax)
% perfectTrackingControl implements (near-) perfect setpoint tracking
% control for a 2R2C building model. The control policy attempts to place
% the next temperature exactly at the user-specified setpoint, but may
% saturate at an equipment capacity limit.
%
% Input:
%   A, the 2 x 2 discrete-time dynamics matrix
%   B, the 2 x 1 discrete-time input matrix
%   w, the K x 1 disturbance vector, kW
%   T0, the 2 x 1 initial state vector, C
%   Tset, the K+1 x 1 temperature setpoint vector, C
%   qcMin, the K x 1 minimum HVAC thermal power capacity, kW
%   qcMax, the K x 1 maximum HVAC thermal power capacity, kW
%
% Output:
%   T, the 2 x K+1 indoor temperature vector, C
%   qc, the K x 1 HVAC thermal power vector, kW

% dimensions
K = length(w);

% data storage
T = zeros(2,K+1); % state [indoor air temperature; thermal mass tempearture], C
T(:,1) = T0; % initial state, C
qc = zeros(K,1); % HVAC thermal power, kW

% simulation
for k=1:K
    % control decision
    % your code
    % here
    
    % dynamic update
    % your code here
end

end

