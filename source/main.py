from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(__name__)
import pymssql


#     print("ID=%d, Name=%s" % (row['id'], row['name']))
def obtenerArticulos():
    conn = pymssql.connect("34.30.51.145", "sqlserver", "Tantan20", "Tarea1")
    cursor = conn.cursor(as_dict=True)
    results=[]
    cursor.execute('EXEC dbo.GetArticulosOrdenados;')
    for row in cursor:
        results.append(row)
        print(row)
    conn.commit()
    conn.close()
    return results
#     print("ID=%d, Name=%s" % (row['id'], row['name']))
# def insertarArticulo(nombre,precio):
    
#     conn = pymssql.connect("basescurso.database.windows.net", "adminBases", "Tantan20", "dbTarea1")
#     cursor = conn.cursor(as_dict=True)
#     results=[]
#     cursor.execute(f"EXEC dbo.InsertarArticulo @Nombre  ='{nombre}' , @Precio={precio} ;")
#     for row in cursor:
#         results.append(row)
#         print(row)
#     conn.commit()
#     conn.close()
#     return results
# def insertarArticulo(nombre, precio):
#     try:
#         # Establecer la conexión con SQL Server
#         conn = pymssql.connect("34.30.51.145", "sqlserver", "Tantan20", "Tarea1")
#         cursor = conn.cursor()

#         # Ejecutar el procedimiento almacenado para insertar un nuevo artículo
#         cursor.execute("EXEC dbo.InsertarArticulo @Nombre=%s, @Precio=%s", (nombre, precio))

#         # Obtener el resultado
#         result = cursor.fetchone()
#         codigo = result['Codigo']
#         mensaje = result['Mensaje']

#         # Confirmar la transacción
#         conn.commit()

#         # Imprimir el código y el mensaje
#         print(f"Código: {codigo}, Mensaje: {mensaje}")

#     except pymssql.Error as e:
#         # Manejar cualquier error que ocurra
#         print(f"Error: {e}")

#     finally:
#         # Cerrar la conexión\
#         cursor.close()
#         conn.close()
#         return result
def insertarArticulo(nombre, precio):
    result = {}
    try:
        # Establecer la conexión con SQL Server
        conn = pymssql.connect("34.30.51.145", "sqlserver", "Tantan20", "Tarea1")
        
        # Usar el mismo tipo de cursor que en obtenerArticulos
        cursor = conn.cursor(as_dict=True)

        # Imprimir el estado de la conexión (esto es más para depuración)
        # print(f"Estado de la conexión antes de ejecutar el SP: {conn._conn.connected()}")
        print(f"Estado de la conexión antes de ejecutar el SP: {conn._conn.connected}")

        # Ejecutar el procedimiento almacenado para insertar un nuevo artículo
        cursor.execute("EXEC dbo.InsertarArticulo @Nombre=%s, @Precio=%s", (nombre, float(precio)))

        # Imprimir el estado de la conexión (esto es más para depuración)
        # print(f"Estado de la conexión después de ejecutar el SP: {conn._conn.connected()}")
        print(f"Estado de la conexión después de ejecutar el SP: {conn._conn.connected}")

        # Obtener el resultado
        result = cursor.fetchone()

        print("RESULT===>",result)

        # Confirmar la transacción
        conn.commit()

        # Imprimir el resultado (esto es más para depuración)
        print(f"Código: {result['Codigo']}, Mensaje: {result['Mensaje']}")

    except pymssql.Error as e:
        # Manejar cualquier error que ocurra
        print(f"Error: {e}")
        result = {'Codigo': 500, 'Mensaje': 'Error desconocido'}

    finally:
        # Cerrar la conexión
        cursor.close()
        conn.close()

    return result



@app.route('/')
def index():
     articulos=obtenerArticulos()
    #  print(articulos)
     return render_template('index.html',articulos=articulos)



@app.route('/createArticle',methods=["POST","GET"])
def createArticle():
    if request.method=="POST":
        print("ES EL POST")
        print("REQUEST FORM",request.form)
        if (request.form['articlePrice']):
            print("DENTRO DEL IF")
            articleName=request.form["articleName"]
            articlePrice=request.form["articlePrice"]
            print("DATA TO BE INSERTED ",articleName,articlePrice)
            resultInsert=insertarArticulo(articleName,articlePrice)
            codigo=resultInsert.get("Codigo")
            Mensaje=resultInsert.get("Mensaje")
            # resultInsert=insertarArticuloSimple(articleName,articlePrice)
           
            if(codigo==409):
                return render_template('create.html',error=Mensaje)
            else:
                articulos=obtenerArticulos()
                return render_template('index.html',articulos=articulos,message=Mensaje) 


        
    #  print(articulos)
        
    else:
        return render_template('create.html')
