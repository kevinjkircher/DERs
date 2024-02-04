function plotRCresults(t,Tset,T,Tm,Qdotc,figNum)
% plotRCresults plots RC thermal circuit simulation results.
%
% Input:
%   t, the K vector time span in h
%   Tset, the indoor temperature setpoint in C
%   T, the K+1 vector indoor air temperature in C
%   Tm, the K+1 vector thermal mass temperature in C
%   Qdotc, the K vector HVAC thermal power in kW
%   figNum, the figure number to plot into

% parameters
tLim = [t(1), t(end)]; % time axis limits, h
TLim = [floor(min(Tset)), ceil(max(Tset)) + 1]; % temperature axis limits

% temperature plot
figure(figNum), clf
subplot(2,1,1), stairs(t,T,'k')
hold on, stairs(t,Tm,'r')
stairs(t,Tset,'m--')
xlim(tLim)
ylim(TLim)
ylabel({'Temperature','($^\circ$C)'})
legend('Air','Mass','Setpoint','location','northoutside','orientation','horizontal')
legend boxoff

% thermal power plot
subplot(2,1,2), fullStairs(t,Qdotc,'k')
xlim(tLim)
ylabel({'Thermal','power (kW)'})
xlabel('Hour (0 = midnight)')

end

