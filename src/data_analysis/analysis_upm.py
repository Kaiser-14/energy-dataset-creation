import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

pd.set_option('display.float_format', '{:.3f}'.format)

# Parameters
attempt = '1'  # Types: '1', '2', '3'
stress_type = 'nocharge'  # Types: 'nocharge', 'asmfish', 'sysbench', 'radiance'
machine = 'pfe1'  # Types: 'pfe1', 'pfe2', 'pfe3', 'pfe4', 'pfe5'

# Parameters
save_figures = False
show_figures = True
save_csv = False
hybrid = True

stress_hybrid = ['rpic', 'asmfish_1', 'sysbench_cpu']

if not hybrid:
	filename = '../logs/UPM/' + stress_type + '/' + attempt + '/log_' + stress_type + '_' + machine
else:
	filename = '../logs/UPM/hybrid/' + attempt + '/log_' + stress_type + '_' + machine

# Load data from csv
energy_df = pd.read_csv(filename + '.csv')

# Finally, plot and save images

# General plot
energy_df.plot()
if save_figures:
	plt.title('general_analysis')
	if not hybrid:
		plt.savefig('../images/UPM/' + stress_type + '/' + attempt + '/' + machine + '/general_analysis.png')
	else:
		plt.savefig('../images/UPM/hybrid/' + attempt + '/' + machine + '/general_analysis.png')
if show_figures:
	plt.show()

# Features plot
for key in energy_df.keys():
	energy_df[key].plot()
	plt.title(key)
	plt.xlabel('Iterations')
	plt.ylabel('Value')
	if save_figures:
		if not hybrid:
			plt.savefig('../images/UPM/' + stress_type + '/' + attempt + '/' + machine + '/' + key + '.png')
		else:
			plt.savefig('../images/UPM/hybrid' + '/' + attempt + '/' + machine + '/' + key + '.png')
	if show_figures:
		plt.show()
	plt.close()

# Correlation matrix
# Filter by stress type
if not hybrid:
	if stress_type == 'radiance':
		label = 'rpic'
		stress_name = 'rpic'
	else:
		label = stress_type
		if stress_type == 'asmfish':
			stress_name = 'asmfish_1'
		elif stress_type == 'sysbench':
			stress_name = 'sysbench_cpu'
		else:
			stress_name = None
# Simplify dataframe to more important data
if not hybrid:
	if stress_name is not None:
		energy_df = energy_df[
			[stress_name, 'active_power_1', 'power_factor_1', 'current_1', 'voltage_1']]
		labels = [label, 'ActPow', 'PowFact', 'Current', 'Voltage']
	else:
		energy_df = energy_df[
			['active_power_1', 'power_factor_1', 'current_1', 'voltage_1']]
		labels = ['ActPow', 'PowFact', 'Current', 'Voltage']
else:
	energy_df = energy_df[
		['cpu_usage', 'rpic', 'asmfish_1', 'sysbench_cpu', 'active_power_2', 'power_factor_2', 'current_2', 'voltage_2']]
	labels = ['CPU', 'rpic', 'asmfish', 'sysbench', 'ActPow', 'PowFact', 'Current', 'Voltage']

# Correlation matrix
correlation_mat = energy_df.corr()
sns.heatmap(correlation_mat, annot=True, xticklabels=labels, yticklabels=labels)
if save_figures:
	if not hybrid:
		plt.savefig('../images/' + stress_type + '/' + attempt + '/' + machine + '/features_correlation.png')
	else:
		plt.savefig('../images/hybrid/' + attempt + '/' + machine + '/features_correlation.png')
if show_figures:
	plt.show()

# List all machines
if not hybrid:
	df_34 = pd.read_csv('../logs/UPM/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe1' + '.csv')
	df_35 = pd.read_csv('../logs/UPM/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe2' + '.csv')
	df_36 = pd.read_csv('../logs/UPM/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe3' + '.csv')
	df_37 = pd.read_csv('../logs/UPM/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe4' + '.csv')
	df_38 = pd.read_csv('../logs/UPM/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe5' + '.csv')
else:
	df_34 = pd.read_csv('../logs/UPM/hybrid/' + attempt + '/log_' + 'hybrid' + '_34' + '.csv')
	df_35 = pd.read_csv('../logs/UPM/hybrid/' + attempt + '/log_' + 'hybrid' + '_35' + '.csv')
	df_36 = pd.read_csv('../logs/UPM/hybrid/' + attempt + '/log_' + 'hybrid' + '_36' + '.csv')
	df_37 = pd.read_csv('../logs/UPM/hybrid/' + attempt + '/log_' + 'hybrid' + '_37' + '.csv')
	df_38 = pd.read_csv('../logs/UPM/hybrid/' + attempt + '/log_' + 'hybrid' + '_38' + '.csv')

min_shape = np.min(np.array([df_34.shape[0], df_35.shape[0], df_36.shape[0], df_37.shape[0], df_38.shape[0]]))
df_34 = df_34[:min_shape]
df_35 = df_35[:min_shape]
df_36 = df_36[:min_shape]
df_37 = df_37[:min_shape]
df_38 = df_38[:min_shape]
energy_df = energy_df[:min_shape]

energy_df['active_power_total'] = df_34['active_power_1'] + df_34['active_power_2'] + df_34['active_power_3'] \
	+ df_34['active_power_4'] + df_34['active_power_5'] + df_34['active_power_6']


# Correlation matrix with total CPUs + total cpu usage of stress type + energy features from specific source
if not hybrid:
	if stress_name is not None:
		energy_df[stress_name] = \
			df_34[stress_name] + df_35[stress_name] + df_36[stress_name] + df_37[stress_name] + df_38[stress_name]
		total_energy_df = \
			energy_df[[stress_name, 'active_power_total', 'power_factor_1', 'current_1', 'voltage_1']]
	else:
		total_energy_df = energy_df[['active_power_total', 'power_factor_1', 'current_1', 'voltage_1']]
else:
	for stress in stress_hybrid:
		energy_df[stress] = \
			df_34[stress] + df_35[stress] + df_36[stress] + df_37[stress] + df_38[stress]
	total_energy_df = energy_df[[
			'cpu_usage', 'rpic', 'asmfish_1', 'sysbench_cpu', 'active_power_total', 'power_factor_2',
			'current_2', 'voltage_2']]

correlation_mat = total_energy_df.corr()
sns.heatmap(correlation_mat, annot=True, xticklabels=labels, yticklabels=labels)
if save_figures:
	if not hybrid:
		plt.savefig('../images/UPM/' + stress_type + '/' + attempt + '/total_features_correlation.png')
	else:
		plt.savefig('../images/UPM/hybrid/' + attempt + '/total_features_correlation.png')
if show_figures:
	plt.show()

# Correlation matrix: total CPUs + stress type + active power for every source
# Get active power per source
for i in range(6):
	key = 'active_power_' + str(i + 1)
	energy_df[key] = df_34[key]

# Extract specific columns
if not hybrid:
	if stress_name is not None:
		energy_df[stress_name] = \
			df_34[stress_name] + df_35[stress_name] + df_36[stress_name] + df_37[stress_name] + df_38[stress_name]
		total_energy_df = energy_df[[
			stress_name, 'active_power_1', 'active_power_2', 'active_power_3', 'active_power_4',
			'active_power_5', 'active_power_6']]
		labels = [label, 'ActPow1', 'ActPow2', 'ActPow3', 'ActPow4', 'ActPow5', 'ActPow6']
	else:
		total_energy_df = energy_df[[
			'active_power_1', 'active_power_2', 'active_power_3', 'active_power_4', 'active_power_5',
			'active_power_6']]
		labels = ['ActPow1', 'ActPow2', 'ActPow3', 'ActPow4', 'ActPow5', 'ActPow6']
else:
	for stress in stress_hybrid:
		energy_df[stress] = \
			df_34[stress] + df_35[stress] + df_36[stress] + df_37[stress] + df_38[stress]
	total_energy_df = \
		energy_df[[
			'cpu_usage', 'rpic', 'asmfish_1', 'sysbench_cpu', 'active_power_1', 'active_power_2', 'active_power_3',
			'active_power_4', 'active_power_5', 'active_power_6']]
	labels = ['CPU', 'rpic', 'asmfish', 'sysbench', 'ActPow1', 'ActPow2', 'ActPow3', 'ActPow4', 'ActPow5', 'ActPow6']

correlation_mat = total_energy_df.corr()
sns.heatmap(correlation_mat, annot=True, xticklabels=labels, yticklabels=labels)
if not hybrid:
	plt.savefig('../images/UPM/' + stress_type + '/' + attempt + '/total_activepower_correlation.png')
else:
	plt.savefig('../images/UPM/hybrid/' + attempt + '/total_activepower_correlation.png')
plt.show()

# Stats
if save_csv:
	if not hybrid:
		df_34.describe().to_csv(
			'../logs/UPM/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_34' + '.csv')
		df_35.describe().to_csv(
			'../logs/UPM/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_35' + '.csv')
		df_36.describe().to_csv(
			'../logs/UPM/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_36' + '.csv')
		df_37.describe().to_csv(
			'../logs/UPM/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_37' + '.csv')
		df_38.describe().to_csv(
			'../logs/UPM/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_38' + '.csv')
		df_34.iloc[:, 15:].describe().to_csv(
			'../logs/UPM/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '.csv')
	else:
		df_34.describe().to_csv(
			'../logs/UPM/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_34' + '.csv')
		df_35.describe().to_csv(
			'../logs/UPM/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_35' + '.csv')
		df_36.describe().to_csv(
			'../logs/UPM/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_36' + '.csv')
		df_37.describe().to_csv(
			'../logs/UPM/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_37' + '.csv')
		df_38.describe().to_csv(
			'../logs/UPM/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_38' + '.csv')
		df_34.iloc[:, 15:].describe().to_csv(
			'../logs/UPM/hybrid/' + attempt + '/summary_dataframe.csv')
