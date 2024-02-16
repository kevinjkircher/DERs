%% introduction
% This script simulates closed-loop operation of an electric water heater
% in any of three configurations: resistance only, heat pump only, or
% hybrid resistance/heat pump.
%
% Kevin J. Kircher, Purdue University, 2024
%
% Please make sure the following functions are on your Matlab path:
%   getWaterHeaterParameters.m (generates water heater parameters)
%   generateWaterDraws.m (generates random hot water draws)
%   plotResults.m (plots simulation results)
%   fullStairs.m (stairstep plots)
%   waterHeaterControl.m (students fill this in)

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

%% input data
% water heater parameters
V = 0.19; % tank volume, m^3
U = 0.0005; % tank wall thermal transmittance, kW/m^2/C
[R,C] = getWaterHeaterParameters(V,U); % thermal capacitance C (kWh/C) and resistance R (C/kW)

% timing
t0 = 0; % initial time, h
tf = 24; % final time, h
dt = 5/60; % time step, h
t = (t0:dt:tf)'; % time span, h
K = length(t)-1; % number of time steps

% water draws
n = 4; % number of occupants
qd = generateWaterDraws(t,n); % thermal power withdrawal, kW

% parameters
Th = 52; % hot water temperature, C
Tc = 15; % inlet water temperature, C
xMin = 0; % minimum thermal energy, kWh
xMax = C*(Th - Tc); % maximum thermal energy, kWh
x0 = xMax; % initial state, kWh5
alpha = 1/(R*C); % continuous-time dynamics parameter, 1/h
a = exp(-alpha*dt); % discrete-time dynamics parameter
Ta = 20; % ambient air temperature, C
w = (Ta - Tc)/R - qd; % disturbance, kW

%% resistance-only simulation
% parameters
prMax = 4.5; % heating element capacity, kW
phMax = 0; % heat pump capacity, kW
xr = xMax; % energy threshold for resistor turn-on in hybrid case, kWh

% simulation
[x1,p1] = waterHeaterControl(x0,xMax,phMax,prMax,a,w,1,alpha,xr);

% plots
plotResults(t,x1,p1,qd,xMin,xMax,phMax,prMax,xr,1)

%% heat-pump-only simulation
% parameters
prMax = 0; % heating element capacity, kW
phMax = 0.5; % heat pump capacity, kW
xr = 0; % energy threshold for resistor turn-on in hybrid case, kWh
eta = 3*ones(K,1); % heat pump coefficient of performance

% simulation
[x2,p2] = waterHeaterControl(x0,xMax,phMax,prMax,a,w,eta,alpha,xr);

% plots
plotResults(t,x2,p2,qd,xMin,xMax,phMax,prMax,xr,2)

%% hybrid simulation
% parameters
prMax = 4.5; % heating element capacity, kW
phMax = 0.5; % heat pump capacity, kW
xr = 0.5*(xMax - xMin); % energy threshold for resistor turn-on in hybrid case, kWh

% simulation
[x3,p3] = waterHeaterControl(x0,xMax,phMax,prMax,a,w,eta,alpha,xr);

% plots
plotResults(t,x3,p3,qd,xMin,xMax,phMax,prMax,xr,3)














