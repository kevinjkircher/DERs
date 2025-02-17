function configureGraphics()
% configureGraphics configures graphics settings, such as using LaTeX for
% text in figures, increasing font size, and increasing line thickness.
%
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

end

