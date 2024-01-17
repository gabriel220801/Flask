# admin_routes.py

from flask import render_template, Blueprint, jsonify, request, redirect, url_for, flash
from Base_Datos import db  
from app.main.user_model import User  # Importa la clase User desde main.user_model
from app import app
import os
from werkzeug.utils import secure_filename
from mysql.connector import Error
from flask import session
import os

# Crea una instancia de Blueprint para el paquete "admin"

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

UPLOAD_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

def get_subfolder_by_category(category_id):
    return str(category_id)
#----------------------------ERRORES--------------------------------------------

@admin_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@admin_blueprint.route('/ruta_que_no_existe')
def ruta_que_no_existe():
    # Puedes redirigir a la página de inicio o a cualquier otra ruta
    return redirect(url_for('admin.page_not_found'))

#-----------------------------------FIN ERRORES-----------------------------------------


#-----------------------------CERRAR SESION----------------------------------------------

@admin_blueprint.route('/logout')
def logout():
    # Verificar si el usuario está actualmente autenticado
    if 'correo' in session:
        # Eliminar la clave 'correo' de la sesión
        session.pop('correo', None)

        # Mensaje de éxito para mostrar al cerrar sesión
        success_message = '¡Hasta pronto!'
        
        # Redirige a la página home con el mensaje de éxito
        return redirect(url_for('main.home') + '?success_message=' + success_message)

    # Redirigir al usuario de nuevo a la página de inicio si no estaba autenticado
    return redirect(url_for('main.home'))


#---------------------------------FIN LOGOUT-----------------------------------------------


def obtener_cantidad_productos_por_categoria():
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id_cat, COUNT(*) as cantidad FROM productos GROUP BY id_cat")
            results = cursor.fetchall()

            cantidad_por_categoria = {1: 0, 2: 0, 3: 0}

            for row in results:
                categoria_id, cantidad = row
                cantidad_por_categoria[categoria_id] = cantidad

            print("Cantidad por categoría:", cantidad_por_categoria)  # Agrega esta línea para imprimir

            return cantidad_por_categoria[1], cantidad_por_categoria[2], cantidad_por_categoria[3]

    except Error as e:
        print(f"Error al obtener la cantidad de productos por categoría: {str(e)}")
        return 0, 0, 0


@admin_blueprint.route('/admin')
def lista_productos():
    # Obtener cantidad de productos por categoría
    cantidad_secadores, cantidad_maquinas, cantidad_otros = obtener_cantidad_productos_por_categoria()

    # Renderizar la plantilla con las cantidades
    return render_template('admin.html', cantidades={
        'secadores': cantidad_maquinas,
        'maquinas': cantidad_secadores,
        'otros': cantidad_otros
    })

@admin_blueprint.route('/admin/users')
def admin():
    # Crear una instancia de User
    user = User(nombre='', telefono='', correo='', contraseña='', rol='')
    lista_usuarios = user.obtener_lista_usuarios()
    return render_template('users_admin.html', lista_usuarios=lista_usuarios)


@admin_blueprint.route('/admin/categorias')
def lista_categorias():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categorias")
        categorias = cursor.fetchall()
        cursor.close()

        # Pasa la lista de productos de máquinas a la plantilla
        return render_template('categorias.html', lista_categorias=categorias)

    except Error as e:
        print(f"Error al obtener Categoria: {str(e)}")
        # Manejo del error, redirigir o mostrar un mensaje de error según sea necesario
        return render_template('categorias.html', error_message='Error al obtener categorias')
    

@admin_blueprint.route('/admin/productos-maquinas')
def productos_maquinas_admin():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, precio, descripcion, cantidad, imagen FROM productos WHERE id_cat = 1")
        productos_maquinas = cursor.fetchall()
        cursor.close()

        # Pasa la lista de productos de máquinas a la plantilla
        return render_template('maquinas_admin.html', lista_productos=productos_maquinas)

    except Error as e:
        print(f"Error al obtener productos de máquinas: {str(e)}")
        # Manejo del error, redirigir o mostrar un mensaje de error según sea necesario
        return render_template('maquinas_admin.html', error_message='Error al obtener productos de máquinas')
    

@admin_blueprint.route('/admin/productos-secadores')
def productos_secadores_admin():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, precio, descripcion, cantidad, imagen FROM productos WHERE id_cat = 2")
        productos_secadores = cursor.fetchall()
        cursor.close()

        # Pasa la lista de productos de secadores a la plantilla
        return render_template('secadores_admin.html', lista_productos=productos_secadores)

    except Error as e:
        print(f"Error al obtener productos de secadores: {str(e)}")
        # Manejo del error, redirigir o mostrar un mensaje de error según sea necesario
        return render_template('secadores_admin.html', error_message='Error al obtener productos de secadores')

@admin_blueprint.route('/admin/productos-otros')
def productos_otros_admin():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, precio, descripcion, cantidad, imagen FROM productos WHERE id_cat = 3")
        productos_otros = cursor.fetchall()
        cursor.close()

        # Pasa la lista de otros productos a la plantilla
        return render_template('otros_admin.html', lista_productos=productos_otros)

    except Error as e:
        print(f"Error al obtener otros productos: {str(e)}")
        # Manejo del error, redirigir o mostrar un mensaje de error según sea necesario
        return render_template('otros_admin.html', error_message='Error al obtener otros productos')



# Agregar Producto
@admin_blueprint.route('/admin/agregar-producto', methods=['GET', 'POST'])
def agregar_producto():
    try:
        # Obtiene la lista de categorías desde la base de datos
        cursor = db.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categorias")
        categorias = cursor.fetchall()
        cursor.close()

        if request.method == 'POST':
            # Lógica para procesar el formulario de agregar producto y agregar a la base de datos
            nuevo_nombre = request.form.get('nuevo_nombre')
            nuevo_precio = request.form.get('nuevo_precio')

            # Accede al archivo de la solicitud
            nueva_imagen = request.files['nueva_imagen']

            # Obtiene la descripción y cantidad del formulario
            nueva_descripcion = request.form.get('nueva_descripcion')
            nueva_cantidad = request.form.get('nueva_cantidad')

            # Obtiene la categoría del formulario
            id_cat = request.form.get('id_cat')

            # Verifica si se seleccionó una imagen
            if nueva_imagen and allowed_file(nueva_imagen.filename):
                # Define la subcarpeta según la categoría del producto
                subfolder = get_subfolder_by_category(id_cat)

                # Guarda la imagen en la carpeta 'static/img' según la estructura especificada
                filename = secure_filename(nueva_imagen.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Asegúrate de que la carpeta exista, si no, créala
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

                nueva_imagen.save(save_path)

                # Guarda la información del producto en la base de datos
                cursor = db.cursor()
                cursor.execute("INSERT INTO productos (nombre, precio, imagen, descripcion, cantidad, id_cat) VALUES (%s, %s, %s, %s, %s, %s)",
                            (nuevo_nombre, nuevo_precio, filename, nueva_descripcion, nueva_cantidad, id_cat))
                db.commit()
                cursor.close()

                # Redirige a la página inicio después de agregar
                return redirect(url_for('admin.lista_productos'))

    except Error as e:
        print(f"Error al obtener categorías o agregar producto: {str(e)}")
        # Manejo del error, redirigir o mostrar un mensaje de error según sea necesario
        return render_template('agregar_producto.html', error_message='Error al obtener categorías o agregar producto')

    # Renderiza el formulario de agregar producto con la lista de categorías
    return render_template('agregar_producto.html', categorias=categorias)


# ---------------------------------------MAQUINAS------------------------------------

@admin_blueprint.route('/admin/productos-maquinas/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_maquina(producto_id):
    if request.method == 'GET':
        # Lógica para cargar la información del producto y mostrar el formulario de edición
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, precio, descripcion, cantidad FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        cursor.close()

        return render_template('editar_producto.html', producto=producto)

    elif request.method == 'POST':
        # Lógica para procesar el formulario de edición y actualizar el producto en la base de datos
        nuevo_nombre = request.form.get('nuevo_nombre')
        nuevo_precio = request.form.get('nuevo_precio')
        nueva_descripcion = request.form.get('nueva_descripcion')
        nueva_cantidad = request.form.get('nueva_cantidad')

        cursor = db.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, descripcion=%s, cantidad=%s WHERE id=%s",
                    (nuevo_nombre, nuevo_precio, nueva_descripcion, nueva_cantidad, producto_id))
        db.commit()
        cursor.close()

        # Redirigir a la página de lista de productos después de editar
        return redirect(url_for('admin.productos_maquinas_admin'))

# ---------------------------------------SECADORES-----------------------------------

@admin_blueprint.route('/admin/productos-secadores/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_secador(producto_id):
    if request.method == 'GET':
        # Lógica para cargar la información del producto y mostrar el formulario de edición
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, precio, descripcion, cantidad FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        cursor.close()

        return render_template('editar_producto.html', producto=producto)

    elif request.method == 'POST':
        # Lógica para procesar el formulario de edición y actualizar el producto en la base de datos
        nuevo_nombre = request.form.get('nuevo_nombre')
        nuevo_precio = request.form.get('nuevo_precio')
        nueva_descripcion = request.form.get('nueva_descripcion')
        nueva_cantidad = request.form.get('nueva_cantidad')

        cursor = db.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, descripcion=%s, cantidad=%s WHERE id=%s",
                    (nuevo_nombre, nuevo_precio, nueva_descripcion, nueva_cantidad, producto_id))
        db.commit()
        cursor.close()

        # Redirigir a la página de lista de productos después de editar
        return redirect(url_for('admin.productos_secadores_admin'))

# -----------------------------------OTROS ARTICULOS--------------------------------------

@admin_blueprint.route('/admin/productos-otros/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_otro(producto_id):
    if request.method == 'GET':
        # Lógica para cargar la información del producto y mostrar el formulario de edición
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, precio, descripcion, cantidad FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        cursor.close()

        return render_template('editar_producto.html', producto=producto)

    elif request.method == 'POST':
        # Lógica para procesar el formulario de edición y actualizar el producto en la base de datos
        nuevo_nombre = request.form.get('nuevo_nombre')
        nuevo_precio = request.form.get('nuevo_precio')
        nueva_descripcion = request.form.get('nueva_descripcion')
        nueva_cantidad = request.form.get('nueva_cantidad')

        cursor = db.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, descripcion=%s, cantidad=%s WHERE id=%s",
                    (nuevo_nombre, nuevo_precio, nueva_descripcion, nueva_cantidad, producto_id))
        db.commit()
        cursor.close()

        # Redirigir a la página de lista de productos después de editar
        return redirect(url_for('admin.productos_otros_admin'))

@admin_blueprint.route('/admin/eliminar-producto/<int:producto_id>', methods=['GET'])
def eliminar_producto(producto_id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
        db.commit()
        cursor.close()

        print("Producto eliminado con éxito.")  # Agregar esta línea

        return redirect(url_for('admin.lista_productos'))

    except Error as e:
        print(f"Error al eliminar producto: {str(e)}")
        # Puedes manejar el error según tus necesidades, redirigir o mostrar un mensaje de error
        return redirect(url_for('admin.lista_productos', error_message='Error al eliminar producto'))
    


@admin_blueprint.route('/admin/eliminar-usuario/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (usuario_id,))
        db.commit()
        cursor.close()

        print("Usuario eliminado con éxito.")  # Agregar esta línea

        return jsonify(success=True)

    except Error as e:
        print(f"Error al eliminar usuario: {str(e)}")
        # Puedes manejar el error según tus necesidades, redirigir o mostrar un mensaje de error
        return jsonify(success=False, error_message='Error al eliminar usuario')
    
@admin_blueprint.route('/admin/editar-usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    if request.method == 'GET':
        try:
            # Obtener la información del usuario y los roles disponibles
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s", (usuario_id,))
            usuario = cursor.fetchone()

            cursor.execute("SHOW COLUMNS FROM users LIKE 'rol'")
            column_info = cursor.fetchone()
            roles = [role.strip("',()") for role in column_info[1].split("'")[1::2]] if column_info else []

            return render_template('editar_usuario.html', usuario=usuario, roles=roles)
        except Error as e:
            print(f"Error al obtener información del usuario: {str(e)}")
            # Puedes manejar el error según tus necesidades, redirigir o mostrar un mensaje de error
            return render_template('error.html', message='Error al obtener información del usuario')

    elif request.method == 'POST':
        try:
            # Actualizar el rol del usuario en la base de datos
            nuevo_rol = request.form.get('rol')
            cursor = db.cursor()
            cursor.execute("UPDATE users SET rol = %s WHERE id = %s", (nuevo_rol, usuario_id))
            db.commit()
            cursor.close()

            flash('Rol actualizado correctamente.', 'success')
            return redirect(url_for('admin.admin'))
        except Error as e:
            print(f"Error al editar rol del usuario: {str(e)}")
            # Puedes manejar el error según tus necesidades, redirigir o mostrar un mensaje de error
            return render_template('error.html', message='Error al editar rol del usuario')






@admin_blueprint.route('/admin/agregar-categoria', methods=['GET', 'POST'])
def agregar_categoria():
    if request.method == 'POST':
        try:
            # Lógica para procesar el formulario de agregar producto y agregar a la base de datos
            nuevo_nombre = request.form.get('nuevo_nombre')

            # Guarda la información del producto en la base de datos
            cursor = db.cursor()
            cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)",
                        (nuevo_nombre,))  # Asegúrate de tener una coma al final para crear una tupla
            db.commit()
            cursor.close()

            # Redirige a la página inicio después de agregar
            return redirect(url_for('admin.lista_categorias'))

        except Error as e:
            print(f"Error al agregar categoria: {str(e)}")
            # Manejo del error, redirigir o mostrar un mensaje de error según sea necesario
            return render_template('agregar_categoria.html', error_message='Error al agregar categoria')

    elif request.method == 'GET':
        # Renderiza el formulario de agregar producto
        return render_template('agregar_categoria.html')

    

@admin_blueprint.route('/admin/editar-categoria/<int:categoria_id>', methods=['GET', 'POST'])
def editar_categoria(categoria_id):
    if request.method == 'GET':
        # Lógica para cargar la información del producto y mostrar el formulario de edición
        cursor = db.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categorias WHERE id_categoria = %s", (categoria_id,))
        categoria = cursor.fetchone()
        cursor.close()

        return render_template('editar_categoria.html', categoria=categoria)

    elif request.method == 'POST':
        # Lógica para procesar el formulario de edición y actualizar el producto en la base de datos
        nuevo_nombre = request.form.get('nuevo_nombre')

        cursor = db.cursor()
        cursor.execute("UPDATE categorias SET nombre=%s WHERE id_categoria=%s",
                    (nuevo_nombre, categoria_id))
        db.commit()
        cursor.close()

        # Redirigir a la página de lista de productos después de editar
        return redirect(url_for('admin.lista_categorias'))
    

@admin_blueprint.route('/admin/eliminar-categoria/<int:categoria_id>', methods=['GET'])
def eliminar_categoria(categoria_id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (categoria_id,))
        db.commit()
        cursor.close()

        print("Categoria eliminado con éxito.")  # Agregar esta línea

        return redirect(url_for('admin.lista_categorias'))

    except Error as e:
        print(f"Error al eliminar categoria: {str(e)}")
        # Puedes manejar el error según tus necesidades, redirigir o mostrar un mensaje de error
        return redirect(url_for('admin.lista_categorias', error_message='Error al eliminar categoria'))
