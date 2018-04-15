import read_data

resp_file = '../data/2002FemPreg.dat.gz'
table = read_data.Pregnancies(resp_file)
table.read_pregnancies_file()

birthord = table.df[table.df['outcome']==1]['birthord'].tolist()

birthord_result = dict((num, birthord.count(num)) for num in birthord)

print(birthord_result)
