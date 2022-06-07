import glob

import pandas as pd

files = [f for f in glob.glob('*.csv')]

df = pd.concat(map(pd.read_csv, files), ignore_index=True)

df.to_csv('dataset.csv', mode='a', header=True, index=False)