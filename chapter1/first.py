"""
import survey

data_dir = '../data/'
table = survey.Pregnancies()
table.read_records(data_dir)
print(len(table.records))
"""
import read_data

resp_file = '../data/2002FemPreg.dat.gz'
table = read_data.Pregnancies(resp_file)
table.read_pregnancies_file()
print(len(table.df))
