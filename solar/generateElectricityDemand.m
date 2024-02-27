function p = generateElectricityDemand(tSpan,electricityFile,Af,N,theta,...
    totalHorizontal,toPlot)
% generateElectricityDemand generates an electricity demand profile for a
% building, including heating/cooling equipment and everything else, over a
% given time span.
%
% Input:
%   tSpan, the K x 1 time span as a datetime object
%   electricityFile, a string containing the electricity data file name
%   Af, the floor area, m^2
%   N, the number of stories
%   theta, the K x 1 outdoor temperature, C
%   totalHorizontal, the K x 1 total horizontal solar irradiance, kW/m^2
%   toPlot, an indicator of whether to plot simulation data and results
%
% Output:
%   p, a K x 1 vector of total electricity demand, kW

% timing
K = length(tSpan); % number of time steps
dt = hours(tSpan(2) - tSpan(1)); % time step, h

% electricity data import
tElec = tSpan; tElec.Year = 2019; % electricity time span (data are from 2019)
plugPowers = importElectricity(electricityFile,tElec); % 'everything else' electricity data import
plugPowers = plugPowers*0.005*Af./mean(plugPowers); % plug powers rescaled by floor area to 5 W/m^2, kW

% 1R1C building model parameters
C = 0.0125*Af; % air thermal capacitance, kWh/C
R = 1./(0.016*sqrt(N*Af)); % indoor-outdoor thermal resistance, C/kW
a = exp(-dt/R/C); % discrete-time dynamics parameter

% indoor temperature setpoint
isWinter = tSpan <= datetime(2022,4,15) | tSpan >= datetime(2022,10,15); % indicator of heating season
isSummer = tSpan >= datetime(2022,5,1) & tSpan <= datetime(2022,9,31); % indicator of cooling season
Tset = 21*ones(K,1); % indoor temperature setpoint, C
Tset(isSummer) = 25; % cooling temperature setpoint, C

% heat pump coefficient of performance
eta = ones(K,1); % heat pump coefficient of performance (initialized at 1 to avoid dividing qc by 0 when calculating p)
eta(isWinter) = max(1,0.0449*theta(isWinter) + 2.57); % heating COP
eta(isSummer) = 0.197*theta(isSummer) - 10.3; % cooling COP

% coefficient of performance plot
if toPlot
    figure(1), clf
    subplot(2,1,1), plot(tSpan,theta,'k')
    ylabel({'Outdoor','temperature ($^\circ$C)'})
    subplot(2,1,2), plot(tSpan,eta,'k')
    ylabel({'Heat pump coefficient','of performance'})
end

% exogenous thermal power
iPower = size(plugPowers,2) - 4; %randi(size(plugPowers,2)); % index of power profile
c = 0.8*ones(K,1); % solar heat gain coefficient
c(isSummer) = 0.5; % lower SHGC in summer to emulate shading
qe = plugPowers(:,iPower) ... % from plugged-in devices
    + 0.19*sqrt(N*Af)*c.*totalHorizontal ... % from the sun
    + 0.5 + (0.25/3)*randn(K,1); % from everything else

% exogenous thermal power plot
if toPlot
    figure(2), clf
    subplot(2,1,1), plot(tSpan,plugPowers(:,iPower),'k')
    ylabel({'Plug','power (kW)'})
    subplot(2,1,2), plot(tSpan,qe,'k')
    ylabel({'Exogenous thermal','power (kW)'})
end

% heat pump sizing
[~,kd] = min(abs(theta - quantile(theta,0.01))); % time index of design condition
pMax = 1.2*((Tset(kd) - theta(kd))/R - qe(kd))/eta(kd); % heat pump electric power capacity, kW
qcMax = zeros(K,1); % maximum heat pump thermal power, kW
qcMax(isWinter) = pMax*eta(isWinter); % nonzero heating capacity in winter
qcMin = zeros(K,1); % minimum heat pump thermal power, kW
qcMin(isSummer) = pMax*eta(isSummer); % nonzero cooling capacity in summer

% data storage
T = zeros(K+1,1); % indoor temperature, C
T(1) = Tset(1); % initial state, C
qc = zeros(K,1); % heat pump thermal power, kW

% thermal simulation
for k=1:K
    % thermal load to exactly track setpoint
    lk = ((Tset(min(k+1,K)) - a*T(k))/(1-a) - theta(k))/R - qe(k); % thermal load, kW
    
    % heat pump thermal power
    qc(k) = max(qcMin(k), min(qcMax(k), lk)); % heat pump thermal power, kW
    if ~(isWinter(k) || isSummer(k)) % if it's not heating or cooling season
        qc(k) = 0; % turn heat pump off
    end
    
    % temperature update
    T(k+1) = a*T(k) + (1-a)*(theta(k) + R*(qc(k) + qe(k))); % C
end

% electric power simulation
p = plugPowers(:,iPower) + qc./eta; % total building electrical load, kW

% building simulation results plot
if toPlot
    figure(3), clf
    subplot(3,1,1), plot(tSpan,T(1:K),'k')
    ylabel({'Indoor','temperature ($^\circ$C)'})
    subplot(3,1,2), plot(tSpan,qc,'k')
    ylabel({'Heat pump','thermal power (kW)'})
    subplot(3,1,3), plot(tSpan,p,'k')
    ylabel({'Total electrical','power (kW)'})
end

end

