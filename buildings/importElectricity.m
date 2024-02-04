function P = importElectricity(fileName,t)
% importElectricity imports and processes electrical load data from the
% MFRED (Multi Family Residential Electricity Demand) csv file. This
% dataset contains electricity demand profiles for 390 multifamily
% apartments in New York City, anonymized by averaging the 390 into 26 
% groups of 15 apartments each.
%
% Input:
%   fileName, the name of the MFRED file.
%   t, the datetime span.
%
% Output:
%   P, a length(t) x 26 matrix of electricity demand data

% import raw data
opts = detectImportOptions(fileName);
opts.PreserveVariableNames = 1;
rawData = readtable(fileName,opts);

% extract power data
powerTime = rawData{:,1}; % time stamp
if powerTime.Year(1) < 2000
    powerTime.Year = 2000+powerTime.Year; % fix year from e.g. 20 to 2020
end
powerTime = powerTime - hours(5); % convert UTC to eastern
iPower = 5:3:size(rawData,2); % indices of kW columns
individualPower = rawData{:,iPower}; % individual power profiles
powerData = array2timetable(individualPower,'RowTimes',powerTime);

% fill any missing data
powerData = fillmissing(powerData,'linear');

% retime to the desired time span
powerData = retime(powerData,t);

% fill any missing data again
powerData = fillmissing(powerData,'linear');

% extract power data from timetable into matrix
P = powerData{:,:};

end

