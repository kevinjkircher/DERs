%% introduction
% This script simulates residential electricity demand and solar
% photovoltaic power output. It computes the annual cost savings from solar
% under one-to-one net metering and net metering with a reduced buyback
% price.
%
% Kevin J. Kircher, Purdue University, 2024
%
% Please make sure the following files are on your Matlab path:
%   west-lafayette-2022-weather.csv (Oikolab weather data CSV
%   MFRED-2019-NYC-Apartments-Electricity-Data.csv (MFRED electricity data CSV)
%   configureGraphics.m (configures graphics settings)
%   importWeather.m (imports Oikolab weather data from CSV)
%   importElectricity.m (imports MFRED electric power data from CSV)
%   generateElectricityDemand.m (generates electricity demand time series)
%   solarAngles.m (computes solar azimuth and elevation angles)
%   surfaceIrradiance.m (computes irradiance on surfaces)

%% graphics settings
configureGraphics; % changes font sizes, line widths, text interpreter

%% input data
% timing
dt = 0.25; % time step, h
tSpan = (datetime(2022,1,1,0,0,0):hours(dt):datetime(2022,12,31,23,0,0))'; % time span as datetime
K = length(tSpan); % number of time steps
t = (0:dt:K*dt)'; % time span as floating-point, h

% weather data import
weatherFile = 'west-lafayette-2022-weather.csv'; % weather file name
[theta,totalHorizontal,beamNormal,diffuseHorizontal,offsetGMT] = ...
    importWeather(weatherFile,tSpan); % weather data import

%% building electricity demand
electricityFile = 'MFRED-2019-NYC-Apartments-Electricity-Data.csv'; % electricity file name
Af = 200; % floor area, m^2
N = 2; % number of stories
toPlot = 0; % indicator of whether to plot simulation data and results
p = generateElectricityDemand(tSpan,electricityFile,Af,N,theta,totalHorizontal,toPlot); % total electricity demand, kW

%% irradiance
% solar angles
lat = 40.4259; % latitude, degrees
long = -86.9081; % longitude, degrees
[el,az] = solarAngles(lat,long,tSpan,offsetGMT); % sun elevation and azimuth angles, degrees

% surface irradiance
bet = lat; % surface tilt angle, degrees
az0 = 0; % surface azimuth angle, degrees
[Stot,Sb,Sd] = ... % total, beam, and diffuse irradiance on surface, kW/m^2
    surfaceIrradiance(az,el,az0,bet,beamNormal,diffuseHorizontal);

% irradiance plot
pLim = [0 1];
tLim = [tSpan(1) tSpan(end)];
figure(4), clf
subplot(3,1,1), plot(tSpan,Stot,'k'), grid on
ylim(pLim), xlim(tLim), ylabel({'Total surface','irradiance','(kW/m$^2$)'})
subplot(3,1,2), plot(tSpan,Sb,'k'), grid on
ylim(pLim), xlim(tLim), ylabel({'Beam surface','irradiance','(kW/m$^2$)'})
subplot(3,1,3), plot(tSpan,Sd,'k'), grid on
ylim(pLim), xlim(tLim), ylabel({'Diffuse surface','irradiance','(kW/m$^2$)'})

%% solar power supply
% solar array efficiency
ratedEta = 0.18; % rated solar array efficiency
ratedT = 25; % rated temperature, C
zeroT = 270; % temperature at which power output stops, C
solarEta = NaN; % solar conversion efficiency
%%%% ^^^^ YOUR CODE HERE ^^^^ %%%%

% solar power supply
panelA = Af/4; % solar panel area, m^2
pSun = panelA*solarEta.*Stot; % solar power supply, kW

% power plot
figure(5), clf
subplot(3,1,1), plot(tSpan,p,'k')
ylabel({'Power','demand (kW)'})
subplot(3,1,2), plot(tSpan,pSun,'k')
ylabel({'Solar power','supply (kW)'})
subplot(3,1,3), plot(tSpan,p - pSun,'k')
ylabel({'Net power','demand (kW)'})

%% electricity costs
% cost without solar
piBuy = 0.15; % price at which user buys electricity, $/kWh
c1 = round(piBuy*dt*sum(p)); % electricity cost, $
fprintf('--------------------------------------------------------------\n')
fprintf('Electricity cost without solar: $%i.\n',c1)

% cost with one-to-one net metering
c2 = round(piBuy*dt*sum(p - pSun)); % electricity cost, $
fprintf('Electricity cost with solar and one-to-one net metering: $%i.\n',c2)
fprintf('Cost reduction from solar with one-to-one net metering: $%i (%i%%).\n', ...
    c1 - c2, round(100*(1 - c2/c1)))

% cost with reduced net metering
piSell = 0.03; % reduced price at which user buys electricity, $/kWh
c3 = NaN; % electricity cost, $
%%%% ^^^^ YOUR CODE HERE ^^^^ %%%%
fprintf('Electricity cost with solar and reduced net metering: $%i.\n',c3)
fprintf('Cost reduction from solar with reduced net metering: $%i (%i%%).\n', ...
    c1 - c3, round(100*(1 - c3/c1)))



















