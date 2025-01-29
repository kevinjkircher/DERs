import pandas as pd

def import_electricity(file_name, t_span):
    """
    importElectricity imports and processes electrical load data from the
    MFRED (Multi Family Residential Electricity Demand) csv file. This
    dataset contains electricity demand profiles for 390 multifamily
    apartments in New York City, anonymized by averaging the 390 into 26
    groups of 15 apartments each.

    Input:
      fileName, the name of the MFRED file.
      t, the datetime span.

    Output:
      P, a length(t) x 26 matrix of electricity demand data
    """

    # import raw data
    raw_data = pd.read_csv(file_name)

    # extract power data
    raw_data['timestamp'] = pd.to_datetime(
        raw_data.iloc[:, 0],
        format='%m/%d/%y %H:%M',
        errors='coerce'
    )

    # fix year from e.g. 20 to 2020
    if raw_data['timestamp'].dt.year.iloc[0] < 2000:
        raw_data.loc[:, 'timestamp'] = raw_data['timestamp'].apply(lambda x: x.replace(year=x.year + 2000))

    # convert UTC to eastern
    raw_data['timestamp'] -= pd.Timedelta(hours=5)

    # set timestamp as index
    raw_data.set_index('timestamp', inplace=True)

    # indices of kW columns
    power_columns = raw_data.columns[4::3]
    individual_power = raw_data[power_columns].copy()  # individual power profiles

    # fill any missing data
    individual_power.interpolate(method='linear', inplace=True)

    # retime to the desired time span
    individual_power = individual_power.reindex(t_span).interpolate(method='linear')

    # fill any missing data again
    individual_power.interpolate(method='linear', inplace=True)

    # extract power data from dataframe into matrix
    P = individual_power.to_numpy()

    return P
