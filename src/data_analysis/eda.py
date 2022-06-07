import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File
attempt = '2'  # Types: '1', '2', '3'
stress_type = 'sysbench'  # Types: 'nocharge', 'asmfish', 'sysbench', 'radiance', 'example'
machine = 'pfe1'  # Types: '34', '35', '36', '37', '38 (MEC) / 'pfe1', 'pfe2', 'pfe3', 'pfe4, 'pfe5' (UPM)
location = 'UPM'  # Types: 'MEC', 'UPM'

filename = '../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_' + machine

# Create dataframe
energy_df = pd.read_csv(filename + '.csv')

# Stress index
if stress_type == 'radiance':
	stress = 'rpic'
elif stress_type == 'asmfish':
	stress = 'asmfish_1'
elif stress_type == 'sysbench':
	stress = 'sysbench_cpu'

if location == 'MEC':
	energy_df = energy_df[[
		'cpu_usage_1', 'cpu_usage_2', 'cpu_usage_3', 'cpu_usage_4', 'memory_usage', stress,
		'active_power_1', 'power_factor_1', 'current_1', 'voltage_1'
	]]
else:
	energy_df = energy_df[[
		stress, 'active_power_1', 'power_factor_1', 'current_1', 'voltage_1'
	]]

correlation_mat = energy_df.corr()
sns.heatmap(correlation_mat, annot=True)
plt.savefig('../images/correlation_' + location + '.png')
plt.show()
