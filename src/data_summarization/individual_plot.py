import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

pd.set_option('display.float_format', '{:.3f}'.format)

# Parameters
attempt = '2'  # Types: '1', '2', '3'
stress_type = 'asmfish'  # Types: 'nocharge', 'asmfish', 'sysbench', 'radiance', 'example', 'h1_asmfish'
machine = 'pfe2'  # Types: '34', '35', '36', '37', '38 (MEC) / 'pfe1', 'pfe2', 'pfe3', 'pfe4, 'pfe5' (UPM)
location = 'UPM'  # Types: 'MEC', 'UPM'

# Parameters
save_figures = False
show_figures = True
save_csv = True
hybrid = False

filename = '../logs/' + location + '/' + stress_type + '/' + attempt + '/log_' + stress_type + '_' + machine

# Load data from csv
energy_df = pd.read_csv(filename + '.csv')

# Correlation matrix
labels = ['asmfish', 'active_power_1', 'power_factor_1', 'current_1', 'voltage_1']
df = energy_df[['asmfish_1', 'active_power_1', 'power_factor_1', 'current_1', 'voltage_1']]

correlation_mat = df.corr()
sns.heatmap(correlation_mat, annot=True, xticklabels=labels, yticklabels=labels)
plt.show()

# Plot things
for key in df.keys():
	energy_df[key].plot()
	plt.title(key)
	plt.xlabel('Iterations')
	plt.ylabel('Value')
	plt.show()
	plt.close()

# fig = plt.figure()
fig, axs = plt.subplots(2)
axs[0].plot(energy_df['asmfish_1'][:1000])
axs[1].plot(energy_df['active_power_1'][:1000])
# axs[0].plot(energy_df['rpic'])
# axs[1].plot(energy_df['active_power_1'])
plt.show()
