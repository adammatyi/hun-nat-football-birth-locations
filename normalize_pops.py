import numpy as np
import pandas as pd

df = pd.read_csv("data-CqRw2.csv")

df['log_population'] = np.log10(df['population'])
df['sqrt_population'] = np.sqrt(df['population'])
df['cbrt_population'] = np.cbrt(df['population'])


df.to_csv('city_pops_scaled.csv', index=False)