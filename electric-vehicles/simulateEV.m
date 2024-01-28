%% introduction
% This script simulates three charging policies for an electric vehicle.

%% data
% timing
t0 = 0; % initial time, h
nd = 7; % number of days in time span
tf = t0 + 24*nd; % final time, h
dt = 1/60; % time step duration, h
t = (t0:dt:tf)'; % time span, h
K = length(t) - 1; % number of time steps

% EV parameters
tau = 1600; % self-dissipation time constant, h
a = exp(-dt/tau); % discrete-time dynamics parameter
etac = 0.95; % charging efficiency
etad = etac; % discharging efficiency
pcMax = 11.5; % charging capacity, kW
pdMax = 0; % discharging capacity, kW
xMax = 80; % energy capacity, kWh
x0 = xMax; % initial energy, kWh
xMin = 0.5*xMax; % minimum acceptable energy capacity, kWh
alph = 0.3*ones(K,1); % energy intensity of driving, kWh/km

% generate discharge powers for driving
pChemDrive = generateDrivingPower(t,alph); % chemical power discharged to drive EV, kW

% plugged-in hours
z = zeros(K,1); % indicator that vehicle is plugged in
z(mod(t(1:K),24) < 6 | mod(t(1:K),24) > 20) = 1; % plug in overnight
z(pChemDrive > 0) = 0; % unplug if vehicle is driving

%% input signal plot
% plot parameters
tLim = [t0 tf]; % time axis limits, h
eLim = [0,xMax]; % energy axis limits, kWh
pLim = [0,pcMax]; % electric power axis limits, kW
pChemLim = [0,ceil(max(pChemDrive)/5)*5]; % checmical power axis limits, kW

% driving power plot with plugged-in periods shaded
figure(1), clf
area(t(1:K),max(pChemLim)*z,'facecolor',0.95*[1 1 1],'edgecolor',[1 1 1])
hold on, fullStairs(t,pChemDrive,'k')
xlim(tLim), ylim(pChemLim)
ylabel({'Power discharged','for driving (kW)'})
xlabel('Hour (0 = midnight)')

%% policy 1: when plugged in, charge at maximum until full
% simulation
[x1,p1] = simulatePolicy1(x0,z,pChemDrive,a,tau,etac,etad,pcMax,xMax);

% plot simulation results
plotEVresults(t,x1,p1,z,xMax,xMin,pcMax,2)

%% policy 2: when energy gets low, charge at maximum until full
% simulation
[x2,p2] = simulatePolicy2(x0,z,pChemDrive,a,tau,etac,etad,pcMax,xMax,xMin);

% plot simulation results
plotEVresults(t,x2,p2,z,xMax,xMin,pcMax,3)

%% policy 3: when energy gets low, charge at constant power to meet deadline
% parameters
hDeadline = 6; % hour of day of charging deadline, h
xStar = xMax; % charging target, kWh

% simulation
[x3,p3] = simulatePolicy3(x0,z,pChemDrive,a,tau,etac,etad,pcMax,xMax,xMin,t,hDeadline,xStar);

% plot simulation results
plotEVresults(t,x3,p3,z,xMax,xMin,pcMax,4)









