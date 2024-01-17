#app.py

import logging
from flask import Flask
import secrets
from flask import render_template, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)





logging.basicConfig(filename="logs.log", format="%(levelname)s:%(name)s:%(message)s", level=logging.DEBUG)



#----------------------------ERRORES--------------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/ruta_que_no_existe')
def ruta_que_no_existe():
    # Puedes redirigir a la página de inicio o a cualquier otra ruta
    return redirect(url_for('404.html'))

#-----------------------------------FIN ERRORES-----------------------------------------



# Importar blueprints después de configurar la aplicación
from app.main.main_routes import main_blueprint
from app.admin.admin_routes import admin_blueprint

# Registrar blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
