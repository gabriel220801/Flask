from mysql.connector import Error
from flask import session
from Base_Datos import db


# User model
class User:
    def __init__(self, nombre, telefono, correo, contraseña,rol, id=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.contraseña = contraseña
        self.rol = rol

    def obtener_lista_usuarios(self):  # Agregué 'self' como primer parámetro
        try:
            cursor = db.cursor()
            cursor.execute("SELECT id, nombre, telefono, correo, rol FROM users ")
            lista_usuarios = cursor.fetchall()
            cursor.close()
            return lista_usuarios
        except Error as e:
            print(f"Error al obtener la lista de usuarios: {str(e)}")
            return []

    def agregar_producto_al_carrito(self, id_producto, cantidad):
        try:
            if 'id' not in session:
                return {'error': 'Usuario no autenticado'}, 401

            id_usuario = session['id']

            cursor = db.cursor()
            cursor.execute("SELECT nombre, precio, imagen FROM productos WHERE id = %s", (id_producto,))
            producto_info = cursor.fetchone()

            if not producto_info:
                cursor.close()
                return {'error': 'Producto no encontrado en la base de datos'}

            cursor.execute(
                "INSERT INTO carrito (id_usuario, id_producto, cantidad) VALUES (%s, %s, %s)",
                (id_usuario, id_producto, cantidad)
            )
            db.commit()
            cursor.close()

            return {
                'message': 'Producto agregado al carrito exitosamente',
                'producto': {
                    'nombre': producto_info[0],
                    'precio': float(producto_info[1]),
                    'imagen': producto_info[2]
                }
            }

        except Error as e:
            print(f"Error inesperado al agregar producto al carrito: {str(e)}")
            return {'error': 'Error al agregar producto al carrito'}

    def obtener_carrito(self):
        try:
            if 'id' not in session:
                return None

            id_usuario = session['id']

            cursor = db.cursor()
            cursor.execute(
                "SELECT carrito.id_carrito, productos.nombre, productos.precio, productos.imagen, carrito.cantidad FROM carrito INNER JOIN productos ON carrito.id_producto = productos.id WHERE carrito.id_usuario = %s;",
                (id_usuario,)
            )

            carrito = cursor.fetchall()
            cursor.close()

            return carrito
        except Error as e:
            print(f"Error al obtener el carrito: {str(e)}")
            return None



    def eliminar_producto_carrito(self, id_carrito):
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM carrito WHERE id_carrito = %s AND id_usuario = %s", (id_carrito, self.id))
            db.commit()
            cursor.close()
            return {'message': 'Producto eliminado del carrito exitosamente'}
        except Error as e:
            print(f"Error inesperado al eliminar producto del carrito: {str(e)}")
            return {'error': 'Error al eliminar producto del carrito'}

    def comprar_todo(self):
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM carrito WHERE id_usuario = %s", (self.id,))
            db.commit()
            cursor.close()
            return {'message': 'Compra exitosa. ¡Gracias por tu compra!'}
        except Error as e:
            print(f"Error inesperado al realizar la compra: {str(e)}")
            return {'error': 'Error al realizar la compra'}
    
   