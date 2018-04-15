import read_data

resp_file = '../data/2002FemPreg.dat.gz'
table = read_data.Pregnancies(resp_file)
table.read_pregnancies_file()
# dict
"""
outcome = table.df['outcome'].tolist()
out_come_result = dict((num, outcome.count(num)) for num in outcome)

print(out_come_result)
"""
#  outcome = 1 live
first = table.df[table.df['outcome'] == 1]
more = table.df[table.df['outcome'] > 1]

print(len(table.df))
print(len(first))
print(len(more))
