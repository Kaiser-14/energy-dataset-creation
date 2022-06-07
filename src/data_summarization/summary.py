import pandas as pd
import numpy as np

# Parameters
attempt = '3'  # Types: '1', '2', '3'
stress_type = 'hybrid'  # Types: 'nocharge', 'asmfish', 'sysbench', 'radiance', 'example', 'h1_asmfish'
machine = 'pfe1'  # Types: '34', '35', '36', '37', '38, 'pfe1
hybrid = True

if not hybrid:
    df_34 = pd.read_csv('../logs/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe1' + '.csv')
    df_35 = pd.read_csv('../logs/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe2' + '.csv')
    df_36 = pd.read_csv('../logs/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe3' + '.csv')
    df_37 = pd.read_csv('../logs/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe4' + '.csv')
    df_38 = pd.read_csv('../logs/' + stress_type + '/' + attempt + '/log_' + stress_type + '_pfe5' + '.csv')
else:
    df_34 = pd.read_csv('../logs/hybrid/' + attempt + '/log_' + 'hybrid' + '_pfe1' + '.csv')
    df_35 = pd.read_csv('../logs/hybrid/' + attempt + '/log_' + 'hybrid' + '_pfe2' + '.csv')
    df_36 = pd.read_csv('../logs/hybrid/' + attempt + '/log_' + 'hybrid' + '_pfe3' + '.csv')
    df_37 = pd.read_csv('../logs/hybrid/' + attempt + '/log_' + 'hybrid' + '_pfe4' + '.csv')
    df_38 = pd.read_csv('../logs/hybrid/' + attempt + '/log_' + 'hybrid' + '_pfe5' + '.csv')

min_shape = np.min(np.array([df_34.shape[0], df_35.shape[0], df_36.shape[0], df_37.shape[0], df_38.shape[0]]))
df_34 = df_34[:min_shape]
df_35 = df_35[:min_shape]
df_36 = df_36[:min_shape]
df_37 = df_37[:min_shape]
df_38 = df_38[:min_shape]
# energy_df = energy_df[:min_shape]

# energy_df['cpu_total'] =
# df_34['cpu_usage'] + df_35['cpu_usage'] + df_36['cpu_usage'] + df_37['cpu_usage'] + df_38['cpu_usage']
# energy_df['active_power_total'] =
# df_34['active_power_1'] + df_34['active_power_2'] + df_34['active_power_3'] + df_34['active_power_4'] +
# df_34['active_power_5'] + df_34['active_power_6']

if not hybrid:
    df_34.describe().to_csv(
        '../logs/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_34' + '.csv')
    df_35.describe().to_csv(
        '../logs/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_35' + '.csv')
    df_36.describe().to_csv(
        '../logs/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_36' + '.csv')
    df_37.describe().to_csv(
        '../logs/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_37' + '.csv')
    df_38.describe().to_csv(
        '../logs/' + stress_type + '/' + attempt + '/summary_dataframe_' + stress_type + '_38' + '.csv')
    df_34.iloc[:, 15:].describe().to_csv(
        '../logs/' + stress_type + '/' + attempt + '/summary_dataframe.csv')
else:
    df_34.describe().to_csv(
        '../logs/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_34' + '.csv')
    df_35.describe().to_csv(
        '../logs/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_35' + '.csv')
    df_36.describe().to_csv(
        '../logs/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_36' + '.csv')
    df_37.describe().to_csv(
        '../logs/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_37' + '.csv')
    df_38.describe().to_csv(
        '../logs/hybrid/' + attempt + '/summary_dataframe_' + 'hybrid' + '_38' + '.csv')
    df_34.iloc[:, 15:].describe().to_csv(
        '../logs/hybrid/' + attempt + '/summary_dataframe.csv')