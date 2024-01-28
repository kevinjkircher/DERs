function plotEVresults(t,x,p,z,xMax,xMin,pcMax,figNum)
% plotEVresults plots electric vehicle simulation results.
%
% Inputs:
%   t, a K+1 vector time span in h
%   x, a K+1 vector of stored energies in kWh
%   p, a K vector of charging powers in kW
%   z, a K vector of indicator variables that the vehicle is plugged in
%   xMax, the battery capacity in kWh
%   xMin, the minimum acceptable stored energy in kWh
%   pcMax, the electric charging power capacity in kW
%   figNum, the figure number to plot into

% parameters
K = length(t) - 1; % number of time steps
tLim = [t(1) t(end)]; % time axis limits, h

% energy plot
figure(figNum), clf
subplot(2,1,1), stairs(t,x,'k')
xlim(tLim), ylim([0,xMax])
ylabel({'Stored','energy (kWh)'})
hold on, plot(t,0*t + xMin,'m--')
text(mean(tLim)/4,xMin,'$\underline x$','color','m',...
    'horizontalalignment','left','verticalalignment','top')

% charging power plot
subplot(2,1,2), area(t(1:K),pcMax*z,'facecolor',0.95*[1 1 1],'edgecolor',[1 1 1])
hold on, fullStairs(t,max(0,p),'k')
xlim(tLim), ylim([0,pcMax])
ylabel({'Charging','power (kW)'})
xlabel('Hour (0 = midnight)')

end

