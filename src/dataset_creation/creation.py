import glob
import os

import pandas as pd

# Read all files in list and store them in a single dataframe, exporting to csv
# Extract the last attempt per test
logs = [f for f in glob.glob('../logs/UPM/hybrid/1/*.csv')]

columns = [
	'timestamp', 'rpic', 'asmfish_1', 'asmfish_2', 'asmfish_3', 'asmfish_4',
	'asmfish_5', 'sysbench_cpu', 'voltage_1', 'power_factor_1',
	'active_power_1', 'current_1', 'voltage_2', 'power_factor_2',
	'active_power_2', 'current_2', 'voltage_3', 'power_factor_3',
	'active_power_3', 'current_3', 'voltage_4', 'power_factor_4',
	'active_power_4', 'current_4', 'voltage_5', 'power_factor_5',
	'active_power_5', 'current_5', 'voltage_6', 'power_factor_6',
	'active_power_6', 'current_6', 'source'
]
df = pd.DataFrame()
first = True

for log in logs:
	filename, _ = os.path.splitext(log)
	df_pfe = pd.read_csv(log)
	df_pfe['source'] = filename[-4:]
	df = df.append(df_pfe)

df.to_csv('dataset.csv', mode='a', header=True, index=False)
