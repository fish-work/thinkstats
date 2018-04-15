import read_data
import numpy as np

resp_file = '../data/2002FemPreg.dat.gz'
table = read_data.Pregnancies(resp_file)
table.read_pregnancies_file()

df_compute = table.df[['birthord', 'prglength']]
df_compute = df_compute[df_compute['birthord'] != 'na']

df_prelength_first = df_compute[df_compute['birthord'] == 1]
df_prelength_more = df_compute[df_compute['birthord'] != 1]

# 38.5605596852
print(df_prelength_first.mean())
# 10.9484814398
print(df_prelength_more.mean())

print((df_prelength_first['prglength'].mean() - df_prelength_more['prglength'].mean()) * 7)