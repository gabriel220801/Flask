from flask import render_template, Blueprint, jsonify, request, redirect, url_for
from app import app
from Base_Datos import db  
from mysql.connector import Error
from app.main.user_model import User 
from flask import session
from werkzeug.security import generate_password_hash
from flask_paginate import Pagination, get_page_args
import os
from flask_bcrypt import check_password_hash
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
def home():
    success_message = request.args.get('success_message')
    template_path = 'home.html'
    full_template_path = os.path.join(app.template_folder, template_path)
    print(f'Trying to render template from path: {full_template_path}')
    return render_template(template_path, success_message=success_message)

    



@main_blueprint.route('/realizar-compra', methods=['POST'])
def realizar_compra():
    try:
        if 'id' not in session:
            return jsonify({'error': 'Usuario no autenticado'}), 401

        id_usuario = session['id']
        productos_ids = request.json.get('productosIds', [])

        # Lógica para procesar la compra utilizando los productos_ids
        # ...

        return jsonify({'message': 'Compra realizada exitosamente'})

    except Exception as e:
        return jsonify({'error': str(e)})


#----------------------------ERRORES--------------------------------------------
@main_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main_blueprint.route('/ruta_que_no_existe')
def ruta_que_no_existe():
    return redirect(url_for('main.page_not_found'))

#-----------------------------------FIN ERRORES-----------------------------------------




#-------------------------------------LOGIN---------------------------------------------

@main_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        try:
            db.ping(True)
            correo = request.form['txtCorreo']
            contraseña = request.form['txtPassword']

            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE correo=%s", (correo,))
            user = cursor.fetchone()
            cursor.close()

            if user and bcrypt.check_password_hash(user[4], contraseña):
                # Inicio de sesión exitoso
                session['id'] = user[0]  # Establecer el ID en la sesión
                session['correo'] = correo
                session['nombre'] = user[1]
                
                # Verificar el rol del usuario
                if user[5] == 'administrador':
                    # Redirigir al panel de administrador
                    return redirect(url_for('admin.lista_productos'))
                
                else:
                    # Mensaje de éxito para mostrar en la interfaz de usuario
                    success_message = '¡Hola y Bienvenido, {}!'.format(user[1])
                    
                    # Redirige a la página home con el mensaje de éxito directamente en el contexto
                    return redirect(url_for('main.home') + '?success_message=' + success_message)

            else:
                # Inicio de sesión fallido
                error_message = 'Inicio de sesión fallido. Verifica tus Datos.'
                return render_template('login.html', error_message=error_message)

        except Error as e:
            # Error al conectarse a la base de datos
            error_message = 'Error al conectar con la base de datos. Por favor, inténtalo de nuevo más tarde.'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

#_------------------------------------------FIN LOGIN-----------------------------------------



#-------------------------------------------REGISTRO USUARIO-----------------------------------

@main_blueprint.route('/crear-registro', methods=['GET', 'POST'])
def crear_registro():
    error_message = None

    if request.method == 'POST':
        try:
            # Verificar la conexión a la base de datos
            with db.cursor() as cursor:
                db.ping(True)

                # Obtener datos del formulario
                nombre = request.form['txtNombre']
                telefono = request.form['txtTelefono']
                correo = request.form['txtCorreo']
                contraseña = request.form['txtPassword']

                # Validar campos
                if not nombre or not telefono or not correo or not contraseña:
                    error_message = 'Todos los campos son obligatorios. Por favor, completa todos los campos.'
                elif len(contraseña) < 4:
                    error_message = 'La contraseña debe tener al menos 4 caracteres.'
                elif any(char.isdigit() for char in nombre):
                    error_message = 'El nombre no puede contener números.'
                # Puedes agregar más validaciones aquí según tus necesidades

                else:
                    hashed_contraseña = bcrypt.generate_password_hash(contraseña).decode('utf-8')
                    
                    # Verificar si el correo ya está registrado
                    cursor.execute("SELECT * FROM users WHERE correo=%s", (correo,))
                    existing_user = cursor.fetchone()

                    if existing_user:
                        error_message = 'El correo ya está registrado. Por favor, inicia sesión.'
                    else:
                        # Insertar nuevo usuario en la base de datos con el rol 'usuario'
                        cursor.execute("INSERT INTO users (nombre, telefono, correo, contraseña, rol) VALUES (%s, %s, %s, %s, 'usuario')",
                                    (nombre, telefono, correo, hashed_contraseña))
                        db.commit()

                        error_message = 'Registro exitoso. ¡Inicia sesión ahora!'

        except Error as e:
            # Error al conectarse a la base de datos
            error_message = 'Error al conectar con la base de datos. Por favor, inténtalo de nuevo más tarde.'

    return render_template('login.html', error_message=error_message)

#-----------------------------FIN REGISTRO-----------------------------------------------



#-----------------------------CERRAR SESION----------------------------------------------

@main_blueprint.route('/logout')
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
    return redirect(url_for('home'))


#---------------------------------FIN LOGOUT-----------------------------------------------




#--------------------------------PRODUCTOS----------------------------------------------

@main_blueprint.route('/productos')
def productos():
    return render_template('productos.html')

@main_blueprint.route('/productos/maquinas')
def maquinas():
    # Obtener el número de página actual
    page = request.args.get('page', 1, type=int)

    # Definir la cantidad de productos por página
    products_per_page = 9

    # Realizar consulta a la base de datos para obtener productos de la categoría "Maquinas"
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre, precio, descripcion, cantidad, imagen FROM productos WHERE id_cat = 1")
    productos = cursor.fetchall()
    cursor.close()

    productos = [(producto[0], producto[1], int(producto[2]), producto[3], producto[4], producto[5]) for producto in productos]

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page

    # Seleccionar los productos correspondientes a la página actual
    productos_pagina = productos[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos), per_page=products_per_page, css_framework='bootstrap4')

    return render_template('maquinas.html', productos=productos_pagina, pagination=pagination)
    

@main_blueprint.route('/productos/secadores')
def secadores():

    # Obtener el número de página actual
    page = request.args.get('page', 1, type=int)

    # Definir la cantidad de productos por página
    products_per_page = 9

    # Realizar consulta a la base de datos para obtener productos de la categoría "Secadores"
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre, precio, descripcion, cantidad, imagen FROM productos WHERE id_cat = 2")
    productos = cursor.fetchall()
    cursor.close()

    productos = [(producto[0], producto[1], int(producto[2]), producto[3], producto[4], producto[5]) for producto in productos]

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page

    # Seleccionar los productos correspondientes a la página actual
    productos_pagina = productos[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos), per_page=products_per_page, css_framework='bootstrap4')

    return render_template('secadores.html', productos=productos_pagina, pagination=pagination)


@main_blueprint.route('/productos/otros_articulos')
def otros_articulos():

    # Obtener el número de página actual
    page = request.args.get('page', 1, type=int)

    # Definir la cantidad de productos por página
    products_per_page = 9

    # Realizar consulta a la base de datos para obtener productos de la categoría "Otros_Articulos"
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre, precio, descripcion, cantidad, imagen FROM productos WHERE id_cat = 3")
    productos = cursor.fetchall()
    cursor.close()

    productos = [(producto[0], producto[1], int(producto[2]), producto[3], producto[4], producto[5]) for producto in productos]

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page

    # Seleccionar los productos correspondientes a la página actual
    productos_pagina = productos[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos), per_page=products_per_page, css_framework='bootstrap4')

    return render_template('otros_articulos.html', productos=productos_pagina, pagination=pagination)



#----------------------------------FIN PRODUCTOS------------------------------------------





#---------------------------------------NOSOTROS-------------------------------------------

@main_blueprint.route('/acercade')
def acercade():
    return render_template ('acercade.html')

#------------------------------------FIN NOSOTROS------------------------------------------



# ------------------------------ CARRITO DE COMPRAS -----------------------------------------

# Ruta para agregar un producto al carrito
@main_blueprint.route('/agregar-al-carrito', methods=['POST'])
def agregar_al_carrito():
    if request.method == 'POST':
        try:
            id_producto = request.form.get('id_producto')
            cantidad = request.form.get('cantidad')

            # Crear una instancia del usuario actual (si está autenticado)
            user = User(nombre='', telefono='', correo='', contraseña='', id=session.get('id'))

            # Llamar al método para agregar producto al carrito
            result = user.agregar_producto_al_carrito(id_producto, cantidad)

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)})

# Ruta para ver el carrito
@main_blueprint.route('/ver-carrito')
def ver_carrito():
    # Crear una instancia del usuario actual (si está autenticado)
    user = User(nombre='', telefono='', correo='', contraseña='', id=session.get('id'))

    # Llamar al método para obtener el contenido del carrito
    carrito = user.obtener_carrito()

    return render_template('carrito.html', carrito=carrito)

# Ruta para eliminar un producto del carrito
@main_blueprint.route('/eliminar-del-carrito/<int:id_carrito>', methods=['POST'])
def eliminar_del_carrito(id_carrito):
    # Crear una instancia del usuario actual (si está autenticado)
    user = User(nombre='', telefono='', correo='', contraseña='', id=session.get('id'))

    # Llamar al método para eliminar producto del carrito
    result = user.eliminar_producto_carrito(id_carrito)

    return jsonify(result)


# ------------------------------ Fin CARRITO DE COMPRAS -----------------------------------------



