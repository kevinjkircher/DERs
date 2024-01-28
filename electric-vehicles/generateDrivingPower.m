function pChemDrive = generateDrivingPower(t,alpha)
% generateDrivingPower generates a time series of chemical power discharged
% to drive an electric vehicle.
%
% Inputs:
%   t, the K+1 vector time span in h
%   alpha, the K vector energy intensity of driving in kWh/km
%
% Output:
%   pChemDrive, a K vector of chemical powers discharged to drive in kW

% timing
K = length(t) - 1; % number of time steps
dt = t(2) - t(1); % time step duration, h
nd = K*dt/24; % number of days in time span
if rem(nd,1) ~= 0
    error('The time span must contain an integer number of days.'); 
end

% reshape energy intensity
alpha = reshape(alpha(:),K/nd,nd);

% generate discharge powers for driving
nt = 3; % number of trips per day
pChemDrive = zeros(K/nd,nd); % chemical discharge powers for driving, kW
dTrip = zeros(nt,nd); % trip distances, km
for j=1:nd % day index
    for i=1:nt % trip index
        % generate trip start time of day
        hStart = 6 + 14*rand; % trip start time of day, h
        kStart = floor(hStart/dt); % trip start time of day index
        while pChemDrive(kStart,j) > 0
            hStart = 6 + 14*rand; % trip start time of day, h
            kStart = floor(hStart/dt); % trip start time of day index
        end
        
        % generate trip distance
        dTrip(i,j) = min(100,lognrnd(1.8,1.24)); % trip distance, km
        
        % set trip speed
        if dTrip(i,j) < 15
            sTrip = 40; % short trip speed, km/h
        else
            sTrip = 90; % long trip speed, km/h
        end
        
        % set trip duration
        tTrip = dTrip(i,j)/sTrip; % trip duration, h
        
        % spread trip discharge energy over the appropriate time steps
        while tTrip > 0
            pChemDrive(kStart,j) = alpha(kStart,j)*sTrip*min(dt,tTrip)/dt;
            tTrip = tTrip - min(dt,tTrip);
            kStart = kStart + 1;
        end
    end
end

% rewrite matrix as stacked vector
pChemDrive = pChemDrive(:); 

end

