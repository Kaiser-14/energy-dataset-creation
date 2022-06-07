import numpy as np
import pandas as pd
import re
import os
import json
import glob
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

pd.set_option('display.float_format', '{:.3f}'.format)

# Parameters
attempt = '2'  # Types: '1', '2', '3'
stress_type = 'nocharge'  # Types: 'nocharge', 'asmfish', 'sysbench', 'radiance', 'example', 'h1_asmfish'
machine = 'pfe1'  # Types: '34', '35', '36', '37', '38 (MEC) / 'pfe1', 'pfe2', 'pfe3', 'pfe4, 'pfe5' (UPM)
location = 'UPM'  # Types: 'MEC', 'UPM'

filename = '../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_' + machine

# Parameters
save_figures = False
show_figures = True

# Load data from csv
energy_df = pd.read_csv(filename + '.csv')

# Finally, plot and save images

# General plot
energy_df.plot()
if save_figures:
	plt.title('general_analysis')
	plt.savefig('../images/' + location + '/' + stress_type + '/' + attempt + '/' + machine + '/general_analysis.png')
if show_figures:
	plt.show()

# Features plot
for key in energy_df.keys():
	energy_df[key].plot()
	plt.title(key)
	plt.xlabel('Iterations')
	plt.ylabel('Value')
	if save_figures:
		plt.savefig('../images/' + location + '/' + stress_type + '/' + attempt + '/' + machine + '/' + key + '.png')
	if show_figures:
		plt.show()
	plt.close()

# Correlation matrix

# Filter by stress type
if stress_type == 'radiance':
	label = 'rpic'
	data = 'rpic'
else:
	label = stress_type
	if stress_type == 'asmfish':
		data = 'asmfish_1'
	elif stress_type == 'sysbench':
		data = 'sysbench_cpu'
	else:
		data = None

# Sum every CPU data from every dataframe

if data is not None:
	energy_df = energy_df[
		['cpu_usage', data, 'active_power_2', 'power_factor_2', 'current_2', 'voltage_2']]
	labels = ['CPU', label, 'ActPow', 'PowFact', 'Current', 'Voltage']
else:
	energy_df = energy_df[
		['cpu_usage', 'active_power_2', 'power_factor_2', 'current_2', 'voltage_2']]
	labels = ['CPU', 'ActPow', 'PowFact', 'Current', 'Voltage']


correlation_mat = energy_df.corr()
sns.heatmap(correlation_mat, annot=True, xticklabels=labels, yticklabels=labels)
plt.savefig('../images/' + stress_type + '/' + attempt + '/' + machine + '/features_correlation.png')
plt.show()

# List all machines
df_34 = pd.read_csv('../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_34' + '.csv')
df_35 = pd.read_csv('../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_35' + '.csv')
df_36 = pd.read_csv('../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_36' + '.csv')
df_37 = pd.read_csv('../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_37' + '.csv')
df_38 = pd.read_csv('../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_38' + '.csv')

min_shape = np.min(np.array([df_34.shape[0], df_35.shape[0], df_36.shape[0], df_37.shape[0], df_38.shape[0]]))
df_34 = df_34[:min_shape]
df_35 = df_35[:min_shape]
df_36 = df_36[:min_shape]
df_37 = df_37[:min_shape]
df_38 = df_38[:min_shape]
energy_df = energy_df[:min_shape]

energy_df['cpu_total'] = \
	df_34['cpu_usage'] + df_35['cpu_usage'] + df_36['cpu_usage'] + df_37['cpu_usage'] + df_38['cpu_usage']
energy_df['active_power_total'] = \
	df_34['active_power_1'] + df_34['active_power_2'] + df_34['active_power_3'] + df_34['active_power_4'] +\
	df_34['active_power_5'] + df_34['active_power_6']

# Correlation matrix with total CPUs + total cpu usage of stress type
if data is not None:
	energy_df[data] = df_34[data] + df_35[data] + df_36[data] + df_37[data] + df_38[data]
	total_energy_df = energy_df[['cpu_total', data, 'active_power_total', 'power_factor_2', 'current_2', 'voltage_2']]
else:
	total_energy_df = energy_df[['cpu_total', 'active_power_total', 'power_factor_2', 'current_2', 'voltage_2']]

correlation_mat = total_energy_df.corr()
sns.heatmap(correlation_mat, annot=True, xticklabels=labels, yticklabels=labels)
plt.savefig('../images/' + location + '/' + stress_type + '/' + attempt + '/total_features_correlation.png')
plt.show()

# Stats
df_34.describe().to_csv(
	'../logs/' + location + '/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_34' + '.csv')
df_35.describe().to_csv(
	'../logs/' + location + '/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_35' + '.csv')
df_36.describe().to_csv(
	'../logs/' + location + '/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_36' + '.csv')
df_37.describe().to_csv(
	'../logs/' + location + '/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_37' + '.csv')
df_38.describe().to_csv(
	'../logs/' + location + '/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_38' + '.csv')
df_34.iloc[:, 15:].describe().to_csv(
	'../logs/' + location + '/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '.csv')
