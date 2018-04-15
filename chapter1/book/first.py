import survey

table = survey.Pregnancies()
table.ReadRecords()
print(len(table.records))