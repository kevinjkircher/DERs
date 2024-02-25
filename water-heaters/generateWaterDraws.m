function qd = generateWaterDraws(t,n)
% generateWaterDraws generates thermal power withdrawals from a domestic
% hot water tank.
%
% Inputs:
%   t, the K+1 x 1 or 1 x K+1 time span in h
%   n, the number of occupants
%
% Output:
%   qd, the K x 1 or 1 x K thermal power draw in kW

% get timing
K = length(t) - 1; % number of time steps
dt = t(2) - t(1); % time step duration, h

% set number of showers
nShower = n*round((t(end)-t(1))/24);

% thermal power draw generation
qd = zeros(K,1); % thermal power withdrawal, kW
for i=1:nShower
    % generate a plausible time index for shower start
    isValid = 0; % indicator of valid water withdrawal
    while isValid == 0
        k = randi(K); % time index for shower start
        if ((mod(t(k),24) >= 5 && mod(t(k),24) <= 9) || (mod(t(k),24) >= 20 && mod(t(k),24) <= 22)) ... % time is in morning or evening
                && max(qd(k:min(K,k+ceil((10/60)/dt)))) == 0 % no one else is in shower
            isValid = 1;
        end
    end
    
    % generate a plausible duration and thermal power
    duration = (7 + 6*rand)/60; % shower duration, h
    power = 17 + 4*rand; % thermal power withdrawal, kW
    energy = power*duration; % heat withdrawal, kWh
    
    % spread heat withdrawal over appropriate time steps
    if dt >= duration
        qd(k) = qd(k) + energy/dt; % spread energy evenly over time step
    else
        while energy > 0
            qd(k) = qd(k) + min(power,energy/dt); % spread remaining energy evenly over time step
            energy = max(0,energy - power*dt); % deduct spent energy
            k = k + 1; % move to next time step
        end
    end
end
end

