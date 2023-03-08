
import pymssql
conn = pymssql.connect("basescurso.database.windows.net", "adminBases", "Tantan20", "dbTarea1")
cursor = conn.cursor(as_dict=True)

cursor.execute('EXEC dbo.SelectArticles;')
for row in cursor:
    print(row)
#     print("ID=%d, Name=%s" % (row['id'], row['name']))

conn.close()