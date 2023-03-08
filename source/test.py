
import pymssql

#     print("ID=%d, Name=%s" % (row['id'], row['name']))
def obtenerArticulos():
    conn = pymssql.connect("basescurso.database.windows.net", "adminBases", "Tantan20", "dbTarea1")
    cursor = conn.cursor(as_dict=True)
    results=[]
    cursor.execute('EXEC dbo.SelectArticles;')
    for row in cursor:
        results.append(row)
        print(row)
    conn.close()
    return results