function plotResults(t,x,p,qd,xMin,xMax,phMax,prMax,xr,figNum)
% plotResults plots water heater simulation results.
%
% Input:
%   t, a K+1 vector time span in h
%   x, a K+1 vector of energy states in kWh
%   p, a K vector of total input electrical powers in kW
%   qd, a K vector of water withdrawal thermal powers in kW
%   xMin, a minimum tank energy in kWh
%   xMax, a tank energy capacity in kWh
%   phMax, a heat pump electrical power capacity in kW
%   prMax, a resistor electrical power capacity in kW
%   xr, an energy threshold below which the resistor turns on in kWh
%       (only relevant in the hybrid case)
%   figNum, the figure number to plot into

% parameters
tLimits = [t(1), t(end)]; % time axis limits, h
tTicks = t(1):6:t(end); % time axis ticks
xLimits = [xMin, xMax]; % energy axis limits, kWh
pLimits = [0, ceil(phMax + prMax)]; % electrical power axis limits, kW
qLimits = [0, ceil(max(qd))]; % electrical power axis limits, kW

% water withdrawal thermal power
figure(figNum), clf
subplot(3,1,1), fullStairs(t,qd), grid on
xlim(tLimits), xticks(tTicks)
ylim(qLimits)
ylabel({'Thermal power','draw (kW)'})

% stored energy
subplot(3,1,2), stairs(t,x), grid on
if phMax > 0 && prMax > 0
    hold on, plot(t,0*t + xr,'m--')
    text(mean(t),xr,'$x_r$','color','m','verticalalignment','bottom',...
        'horizontalalignment','right')
end
xlim(tLimits), xticks(tTicks)
ylim(xLimits)
ylabel({'Stored thermal','energy (kWh)'})

% charging power
subplot(3,1,3), fullStairs(t,p), grid on
xlim(tLimits), xticks(tTicks)
ylim(pLimits)
ylabel({'Electrical','power (kW)'})
xlabel('Hour (0 = midnight)')

end

