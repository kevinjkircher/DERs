%% introduction
% This script adapts a simple climate model from https://www.e-education.psu.edu/meteo469/node/198
% and uses it to illustrate linearization and discrete-time simulation of a
% nonlinear dynamical system.
%
% Kevin J. Kircher, Purdue University, 2024
%
% Please make sure the following functions are on your Matlab path:
%   k2c.m (unit conversion)
%   fullStairs.m (stairstep plots)
%   nonlinearClimateSim (students fill this in)
%   linearizedClimateSim (students fill this in)

%% graphics settings
% I recommend adding these to your startup.m file. Matlab runs that file at
% startup, effectively turning these settings into new defaults.

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
% parameters
alpha = 0.3; % albedo of earth's atmosphere
S = 1366; % solar constant, W/m^2
eps = 0.767; % emissivity of earth's atmosphere
sigma = 5.67e-8; % Stefan-Boltzmann constant, W/m^2/K^4
rho = 997; % density of water, kg/m^3
c = 4.186e3; % specific heat of water, J/kg/K
R = 6.378e6; % radius of the earth, m
l = 70; % depth of well-mixed water layer on earth's surface, m
C = 0.7*4*pi*R^2*rho*c*l; % thermal capacitance of earth's surface, J/K
beta = 4*sigma*pi*R^2/C; % intermediate coefficient, K^3/s

% linear emissivity vs. CO2 concentration fit, eps = eps0 + m*conc
T1 = 286.7; % average surface temperature from 1880-1900, K
eps1 = 2*(1 - (1-alpha)*S/(4*sigma*T1^4)); % average emissivity from 1880-1900
c1 = (291 + 296)/2; % average CO2 concentration from 1880-1900, ppm
T2 = 287.8; % average surface temperature in 2022, K
eps2 = 2*(1 - (1-alpha)*S/(4*sigma*T2^4)); % emissivity in 2022
c2 = 418.56; % CO2 concentration in 2022, ppm
m = (eps2 - eps1)/(c2 - c1); % slope, 1/ppm
eps0 = eps1 - m*c1; % intercept

% timing
t0 = 0; % initial time, s
dt = 365*24*3600; % time step, s
K = 78; % number of time steps
tf = t0 + K*dt; % final time, s
t = t0:dt:tf; % time span, s
y = 2022 + t/(365*24*3600); % year

%% CO2 concentration plot
% emissivity vs. CO2 concentration
cPlot = 200:500; % CO2 concentrations to plot, ppm
figure(1), clf, yyaxis left
plot(cPlot,eps0 + m*cPlot)
xlim([min(cPlot),max(cPlot)]), ylim([0.6,0.8])
ylabel('Atmospheric emissivity')

% annotation
lw = 2; 
xline(c1,'k--','linewidth',lw)
text(c1,min(ylim)+0.025,'1880--1900:','rotation',90,'verticalalignment','bottom','horizontalalignment','center')
text(c1,min(ylim)+0.025,sprintf('%.3g ppm',c1),'rotation',90,'verticalalignment','top','horizontalalignment','center')
xline(c2,'k--','linewidth',lw)
text(c2,min(ylim)+0.025,'2022:','rotation',90,'verticalalignment','bottom','horizontalalignment','center')
text(c2,min(ylim)+0.025,sprintf('%.3g ppm',c2),'rotation',90,'verticalalignment','top','horizontalalignment','center')

% surface temperature vs. CO2 concentration
yyaxis right
plot(cPlot,k2c(((1-alpha)*S./(4*sigma*(1 - (eps0 + m*cPlot)/2))).^(1/4)))
ylabel('Global average surface temperature ($^\circ$C)')
xlabel('Atmospheric CO$_2$ concentration (parts per million)')

%% nominal simulation
% action (emissivity, from atmospheric CO2 concentration)
uHat = eps + (410-315)/60*0.05/280*(1:K);

% continuous-time disturbance (albedo and solar constant)
alphaHat = alpha*ones(1,K); % albedo
wtHat = (1-alphaHat)*S*pi*R^2/C; % continuous-time disturbance

% state
x0 = ((1-alpha)*S/(4*(1-eps/2)*sigma))^(1/4); % initial global average surface temperature, K
xHat = nonlinearClimateSim(t,x0,uHat,wtHat,beta); % global average surface temperature, K

% plot
figure(2), clf
subplot(3,1,1), fullStairs(y,uHat,'k--')
xlim([y(1), y(end)]), ylabel({'Atmospheric', 'emissivity', '$u(t)$'})
subplot(3,1,2), fullStairs(y,alphaHat,'k--')
xlim([y(1), y(end)]), ylabel({'Atmospheric', 'albedo', '$\alpha(t)$'})
subplot(3,1,3), plot(y,k2c(xHat),'k--')
xlim([y(1), y(end)]), ylabel({'Global-average sur-', 'face temperature', '$x(t)$ ($^\circ$C)'})
xlabel('Year')

%% true simulation
% action (emissivity, from atmospheric CO2 concentration)
u = zeros(1,K);
u(1) = uHat(1);
for k=1:K-1
    u(k+1) = u(k) - 0.5*(uHat(k+1) - uHat(k));
end
u = u.*(1 + 0.01*sin(2*pi*y(1:K)/10)); % perturbed albedo

% continuous-time disturbance (scaled albedo and solar constant)
alphat = alpha*(1 + 0.01*sin(y(1:K))); % perturbed albedo
wt = (1-alphat)*S*pi*R^2/C;

% state
x = nonlinearClimateSim(t,x0,u,wt,beta); % global average surface temperature, K

% plot
figure(2)
subplot(3,1,1), hold on, fullStairs(y,u,'b')
subplot(3,1,2), hold on, fullStairs(y,alphat,'b')
subplot(3,1,3), hold on, plot(y,k2c(x),'b')

%% linearized simulation
% control perturbation
du = u - uHat;

% continuous-time disturbance perturbation
dwt = wt - wtHat;

% state
xLin = linearizedClimateSim(t,xHat,uHat,du,dwt,beta); % global average surface temperature perturbation, K

% plot
figure(2)
subplot(3,1,3), hold on, plot(y,k2c(xLin),'mo')
legend('Nominal','True','Linearized','location','northwest')

% error plot
figure(3), clf
plot(y,xLin-x,'k')
ylabel('Prediction error $x^{\rm lin}(t) - x(t)$ ($^\circ$C)')
xlabel('Year')
xlim([y(1), y(end)])







