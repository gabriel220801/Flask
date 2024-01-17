import mysql.connector



# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="BD_TiendaBarberia"
)