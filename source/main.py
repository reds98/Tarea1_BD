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
def insertarArticulo(nombre, precio):
    try:
        # Establecer la conexión con SQL Server
        conn = pymssql.connect("34.30.51.145", "sqlserver", "Tantan20", "Tarea1")
        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para insertar un nuevo artículo
        cursor.execute("EXEC dbo.InsertarArticulo @Nombre=%s, @Precio=%s", (nombre, precio))

        # Obtener el resultado
        result = cursor.fetchone()
        codigo = result['Codigo']
        mensaje = result['Mensaje']

        # Confirmar la transacción
        conn.commit()

        # Imprimir el código y el mensaje
        print(f"Código: {codigo}, Mensaje: {mensaje}")

    except pymssql.Error as e:
        # Manejar cualquier error que ocurra
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión
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
            print("RESULT INSERTED==>",resultInsert)
            print("Code INSERTED==>",resultInsert[0])
            print("Message INSERTED==>",resultInsert[1])
            if(resultInsert[0]==409):
                return render_template('create.html',error=resultInsert[1])
            else:
                articulos=obtenerArticulos()
                return render_template('index.html',articulos=articulos,message=resultInsert[1]) 


        
    #  print(articulos)
        
    else:
        return render_template('create.html')
