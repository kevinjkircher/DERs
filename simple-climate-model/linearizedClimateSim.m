function xLin = linearizedClimateSim(t,xHat,uHat,du,dwt,beta)
% linearizedClimateSim simulates nonlinear climate dynamics.
%
% Inputs:
%   t, a time span in seconds
%   xHat, a K+1-vector of nominal global average surface temperatures in K
%   uHat, a K-vector of nominal atmospheric emissivities
%   du, a K-vector of atmospheric emissivity perturbations
%   dwt, a K-vector of continuous-time disturbance perturbations in K/s
%   beta, a parameter in K^3/s
%
% Output:
%   xLin, a K+1-vector of approximate global average surface temperatures in K

% simulation
K = length(uHat); % number of time steps
dx = 0*xHat; % global average surface temperature perturbations in K
for k=1:K
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
end
xLin = xHat + dx; % approximate global average surface temperatures in K

end

