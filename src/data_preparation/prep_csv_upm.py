import json
import os
import re

import numpy as np
import pandas as pd

pd.set_option('display.float_format', '{:.2f}'.format)

# Parameters
attempt = '1'  # Types: '1', '2', '3'
stress_type = 'hybrid'  # Types: 'nocharge', 'asmfish', 'sysbench', 'radiance'
machine = 'pfe1'  # Types: 'pfe1', 'pfe2', 'pfe3', 'pfe4, 'pfe5',

# Parameters
save_figures = True
show_figures = True
txt = True
hybrid = False

if not hybrid:
	filename = '../logs/UPM/' + stress_type + '/' + attempt + '/log_' + stress_type + '_' + machine
else:
	filename = '../logs/UPM/hybrid/' + attempt + '/log_' + stress_type + '_' + machine

# Import data from txt logs and save into csv
filename_base = os.path.basename(filename + '.txt')
df = open(filename + '.txt', 'r')
df_array = np.array(df.readlines())
# print(df_array)

# Create filename directories if not exist
if save_figures:
	if not os.path.exists('../images/UPM/' + stress_type + '/' + attempt + '/' + machine):
		os.makedirs('../images/UPM/' + stress_type + '/' + attempt + '/' + machine)

indices = [i for i, elem in enumerate(df_array) if 'time: 163' in elem]

# Create dataframe
energy_df = pd.DataFrame()

for index in indices:
	# Timestamp line
	data = df_array[index]
	s = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(data))]
	# print(s)
	timestamp = s[0]

	# Search for specific topics (rpic)
	new_array = df_array[index:index+5]
	rpic_indices = [i for i, elem in enumerate(new_array) if 'rpic' in elem]
	# print(rpic_indices)
	rpic_cpu = 0
	# for i, idx in enumerate(rpic_indices):
	# 	data = new_array[idx]
	# 	s = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(data))]
	# 	rpic_cpu[i] = s[6]
	if rpic_indices:
		data = new_array[rpic_indices[0]]
		s = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(data))]
		# print(s)
		rpic_cpu = s[0]

	# Search for specific topics (asmfish)
	new_array = df_array[index:index + 5]
	asmfish_indices = [i for i, elem in enumerate(new_array) if './LinuxOS_binar' in elem]
	# print(asmfish_indices)
	asmfish_cpu = np.zeros(5)
	cpu = np.zeros(5)
	for i, idx in enumerate(asmfish_indices):
		data = new_array[idx]
		s = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(data))]
		asmfish_cpu[i] = s[0]
		cpu[i] = s[5]

	# Search for specific topics (sysbench)
	new_array = df_array[index:index + 5]
	sysbench_indices = [i for i, elem in enumerate(new_array) if './src/sysbench' in elem]
	# print(sysbench_indices)
	sysbench_cpu = 0
	if sysbench_indices:
		data = new_array[sysbench_indices[0]]
		s = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(data))]
		# print(s)
		sysbench_cpu = s[0]

	# Sum 4 CPUs usages
	# cpu_usage = cpu_usage_1 + cpu_usage_2 + cpu_usage_3 + cpu_usage_4

	# Merge data and append to dataframe
	data = [
		[
			timestamp, rpic_cpu, asmfish_cpu[0], asmfish_cpu[1], asmfish_cpu[2], asmfish_cpu[3],
			asmfish_cpu[4], sysbench_cpu
		]
	]

	energy_df = energy_df.append(data, ignore_index=True)

energy_df.columns = [
	'timestamp', 'rpic', 'asmfish_1', 'asmfish_2', 'asmfish_3', 'asmfish_4', 'asmfish_5', 'sysbench_cpu',
]

# Concatenate API data
api_df = pd.DataFrame(data=None)
# file = open('logs/nocharge/1/server.txt', 'r')
if not hybrid:
	file = open('../logs/UPM/' + stress_type + '/' + attempt + '/server.txt', 'r')
else:
	file = open('../logs/UPM/hybrid/' + attempt + '/server.txt', 'r')
lines = file.readlines()

# Extract data from each line and append into dictionary. Finally, create dataframe based on dict
for line in lines:
	data_json = json.loads(line.strip())
	data_dict = {}

	for item in data_json:
		for key, value in item.items():
			if key != 'id':
				if key == 'timestamp':
					data_dict[key] = value
				else:
					data_dict[key + '_' + str(item['id'])] = value

	api_df = api_df.append(data_dict, ignore_index=True)

file.close()

# Iterate over energy dataframe to append API data based on closest timestamp
aps = []
api_aux = api_df.drop('timestamp', axis=1)

# Iterate over dataframe to append data based on closest timestamp
for _, row in energy_df.iterrows():
	# Extract indexes to fill
	indexes = api_df[row[0] < api_df['timestamp']].index

	# Get specific row
	api_sample = api_df.drop(indexes)
	try:
		index = api_sample['timestamp'].idxmax(axis=0)
	except:
		index = 0

	aps.append(api_df.iloc[index][api_aux.columns])

energy_df[api_aux.columns] = aps

# Extract specific columns
energy_df = energy_df[
	[
		'timestamp', 'rpic',
		'asmfish_1', 'asmfish_2', 'asmfish_3', 'asmfish_4', 'asmfish_5', 'sysbench_cpu',
		'voltage_1', 'power_factor_1', 'active_power_1', 'current_1',
		'voltage_2', 'power_factor_2', 'active_power_2', 'current_2',
		'voltage_3', 'power_factor_3', 'active_power_3', 'current_3',
		'voltage_4', 'power_factor_4', 'active_power_4', 'current_4',
		'voltage_5', 'power_factor_5', 'active_power_5', 'current_5',
		'voltage_6', 'power_factor_6', 'active_power_6', 'current_6',
	]
]

# Export data to .csv
energy_df.to_csv(filename + '.csv', index=False)
