function x = nonlinearClimateSim(t,x0,u,wt,beta)
% nonlinearClimateSim simulates nonlinear climate dynamics.
%
% Inputs:
%   t, a time span in seconds
%   x0, a scalar initial global average surface temperature in K
%   u, a K-vector of atmospheric emissivities
%   wt, a K-vector of continuous-time disturbances in K/s
%   beta, a parameter in K^3/s
%
% Output:
%   x, a K+1-vector of global average surface temperatures in K

% dimensions and data storage
K = length(u); % number of time steps
if isrow(u)
    x = zeros(1,K+1);
elseif iscolumn(u)
    x = zeros(K+1,1);
else
    error('u must be a vector.')
end

% simulation
x(1) = x0; % initial state
for k=1:K
    % your
    % code
    % here
end

end

