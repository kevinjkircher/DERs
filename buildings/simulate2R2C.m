%% introduction
% This script models a building as a 2R2C thermal circuit and simulates its
% dynamics both exactly and using a two-timing approximation.
%
% Kevin J. Kircher, Purdue University, 2024
%
% Please make sure the following functions are on your Matlab path:
%   importWeather.m (imports weather data)
%   importElectricity.m (imports electricity load data)
%   plotResults.m (plots simulation results)
%   fullStairs.m (stairstep plots)
%   perfectTrackingControl.m (students fill this in)
%   thermostaticControl.m (students fill this in)

%% graphics settings
% I recommend adding these to a startup.m file in your Matlab root 
% directory. Matlab runs that file at startup, effectively turning these 
% settings into new defaults.

% set LaTeX as the default text interpreter
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultLegendInterpreter','latex');
set(0,'DefaultAxesTickLabelInterpreter','latex');

% set the default font size for axes ticks/labels and figure titles
set(0,'DefaultAxesFontSize',24);

% set the default text size for figures and legends
set(0,'DefaultTextFontSize',24);
set(0,'DefaultLegendFontSizeMode','manual')
set(0,'DefaultLegendFontSize',24)

% set the default line width for plots and stairstep plots
set(0,'DefaultLineLineWidth',2.5);
set(0,'DefaultStairLineWidth',2.5);

%% parameters
% geometry
Af = 200; % floor area, m^2
N = 2; % number of stories

% thermal capacitances
C = 0.0125*Af; % air thermal capacitance, kWh/C
Cm = 12*C; % mass thermal capacitance, kWh/C

% thermal resistances
R = 1./(0.016*sqrt(N*Af)); % indoor-outdoor thermal resistance, C/kW
Rm = R/6; % indoor-mass thermal resistance, C/kW

% timing
dt = 0.25; % time step, h
tSpan = (datetime(2022,12,22,0,0,0):hours(dt):datetime(2022,12,26,23,0,0))'; % time span as datetime
K = length(tSpan); % number of time steps
t = (0:dt:K*dt)'; % time span as float, h

% heater capacity constraings
qcMin = zeros(K,1); % minimum HVAC thermal power, kW
qcMax = 14*ones(K,1); % maximum HVAC thermal power, kW

%% 2R2C system matrices
% continuous-time system matrices
Ac = zeros(2,2); % continuous-time dynamics matrix
Bc = zeros(2,1); % continuous-time input matrix
% your
% 
% code
% 
% here

% discrete-time system matrices
% your code
% here

%% input signals
% weather data import
weatherFile = 'west-lafayette-2022-weather.csv';
[Tout,I,~,~,~] = importWeather(weatherFile,tSpan);

% electricity data import
electricityFile = 'MFRED-2019-NYC-Apartments-Electricity-Data.csv';
tElec = tSpan; tElec.Year = 2019;
plugPowers = importElectricity(electricityFile,tElec);

% exogenous thermal power
lambda = 0.25; % glazing ratio
c = 0.4; % solar heat gain coefficient
qe = plugPowers(:,randi(size(plugPowers,2))) ... % from plugged-in devices
    + 4.8*c*lambda*sqrt(N*Af*I) ... % from the sun
    + 1 + (0.5/3)*randn(K,1); % from everything else

% disturbance
w = qe + Tout/R; % kW

% indoor temperature setpoint
Tset = 21*ones(K+1,1); % day indoor temperature setpoint, C
Tset(mod(t,24) < 6 | mod(t,24) > 22) = 18.5; % night setpoint, C

% input signal plot
figure(1), clf
subplot(2,1,1), plot(tSpan,Tout,'k')
ylabel({'Outdoor','temperature','($^\circ$C)'})
subplot(2,1,2), plot(tSpan,qe,'k')
ylabel({'Exogenous','thermal power','(kW)'})

%% (near-) perfect tracking simulation
% initial state
T0 = [Tset(1); % initial air temperature, C
    mean(Tset)]; % initial mass temperature, C

% simulation
[T1,qc1] = perfectTrackingControl(A,B,w,T0,Tset,qcMin,qcMax);

% plot results
plotRCresults(t,Tset,T1(1,:),T1(2,:),qc1,2)

%% thermostatic control simulation
% simulation
dT = 0.5; % thermostat deadband halfwidth, C
[T2,qc2] = thermostaticControl(A,B,w,T0,Tset,qcMin,qcMax,dT);

% plot results
plotRCresults(t,Tset,T2(1,:),T2(2,:),qc2,3)


















