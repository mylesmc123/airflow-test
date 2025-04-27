# %%
# Open the observed csv file and the forecast csv file and combine them
import pandas as pd

# %%
gage = 'WLTO2'
obs_df = pd.read_csv(f'{gage}_HGIRG_observed.csv')
forec_df = pd.read_csv(f'{gage}_HGIFF_forecast.csv')

# %%
# if xUnit is 'ft', rename 'x' column to to stage (ft).
#else if xUnit is 'm', rename 'x' column to to stage (m).
# else if xUnit is 'kcfs', rename 'x' column to to flow (cfs).
def update_columns(gage_df):
    gage_df['validTime'] = pd.to_datetime(gage_df['validTime'])
    gage_df['validTime'] = gage_df['validTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    for coltype in ('primary', 'secondary'):
        if gage_df[f'{coltype}Units'][0] == 'ft':
            gage_df.rename(columns={f'{coltype}': 'stage (ft)'}, inplace=True)
        elif gage_df[f'{coltype}Units'][0] == 'm':
            gage_df.rename(columns={f'{coltype}': 'stage (m)'}, inplace=True)
        elif gage_df[f'{coltype}Units'][0] == 'kcfs':
        # convert kcfs to cfs
            gage_df[f'{coltype}'] = gage_df[f'{coltype}'] * 1000
            gage_df.rename(columns={f'{coltype}': 'flow (cfs)'}, inplace=True)
    # drop the columns 'primaryUnits'and 'secondaryUnits'
        gage_df.drop(columns=[f'{coltype}Units'], inplace=True)
    return gage_df
obs_df = update_columns(obs_df)
forec_df = update_columns(forec_df)

# %%
# merge the two dataframes
merged_df = pd.merge(obs_df, forec_df, how='outer')

# %%
last_observed_time = obs_df['validTime'].iloc[-1]
# the forecast time will be the first forecast time after the last observed time
# get the last_observed_time in merged_df and then get the next row as the first forecast time
merged_df = merged_df.sort_values(by='validTime')
merged_df = merged_df.reset_index(drop=True)
# get the row index of the last observed time
last_observed_time_index = merged_df[merged_df['validTime'] == last_observed_time].index[0]
# get +1 row index of the last observed time index
first_forecast_time_index = last_observed_time_index + 1
# get the first forecast time
forecast_time = merged_df.iloc[first_forecast_time_index]['validTime']


# %%
simulation_window = {
    'start': merged_df['validTime'].iloc[0],
    'end': merged_df['validTime'].iloc[-1],
    'forecast_time': forecast_time
}
simulation_window
# %%
# plot the obs_df and forec_df over each other as a time series
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import matplotlib.ticker as ticker

# Set the figure size
plt.figure(figsize=(12, 6))
# Set the date format
date_format = mdates.DateFormatter('%m-%d')
# Set the x-axis major locator
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=72))
ax.xaxis.set_major_formatter(date_format)
# Set the x-axis major formatter
ax.xaxis.set_major_formatter(date_format)
# Set the x-axis minor formatter
ax.xaxis.set_minor_formatter(date_format)
# assign the data
obs_time = pd.to_datetime(obs_df['validTime'])
obs_stage = obs_df['stage (ft)']
forec_time = pd.to_datetime(forec_df['validTime'])
forec_stage = forec_df['stage (ft)']
# Plot the observed data
plt.plot(obs_time, obs_stage, label='Observed', color='blue', linewidth=2)
# Plot the forecast data
plt.plot(forec_time, forec_stage, label='Forecast', color='orange', linewidth=2)
# Set the title and labels
plt.title('Observed and Forecasted Gage Data')
plt.xlabel('Date')
plt.ylabel('Stage (ft)')
# Set the legend
plt.legend()
plt.show
# %%
# get the max value of the merged_df['stage (ft)'] and the validTime at which it occurs.
max_stage_time = merged_df.loc[merged_df['stage (ft)'].idxmax()]['validTime']
max_stage = merged_df['stage (ft)'].max()

# TODO get the last time a forecast run has been made.
# TODO If the last forecast time is greater than the max stage time, then the forecast is still valid and no new forecast is needed.
# TODO If the last forecast time is less than the max stage time, then an updated forecast is needed.

last_run_forecast_time = None
# IF no previous forecast is available, and the stage exceeds the action_stage, then a new forecast is needed.
action_stage = 15.0
if last_run_forecast_time is None and max_stage >= action_stage:
    print(f"A new forecast is needed. The maximum stage is {max_stage} ft at {max_stage_time}.")
    run = True
elif last_run_forecast_time is None and max_stage < action_stage:
    print(f"No new forecast is needed. The maximum stage is {max_stage} ft at {max_stage_time}.")
    run = False
# %%
# save the run info to a json file
import json
run_info = {
    'runForecast': run,
    'max_stage': max_stage,
    'max_stage_time': max_stage_time,
    'action_stage': action_stage,
    'last_run_forecast_time': last_run_forecast_time,
    'simulation_window': simulation_window
}
with open(f'{gage}_run_info.json', 'w') as f:
    json.dump(run_info, f, indent=4)
# %%