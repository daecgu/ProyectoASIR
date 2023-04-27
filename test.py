# Importamos el ORM
from flask_sqlalchemy import SQLAlchemy
# Importamos Flask, render template para los archivos html y url for para los links.
from flask import Flask, render_template, url_for, request, redirect
# Importamos para gestionar login
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
# Importamos de los models los el usuario, la instancia del orm y el login manager.
from models import User, login_manager, db
# Importamos la clase para validar el formulario
# from forms import SignupForm

# Creamos una instancia Flask que se llama app
app = Flask(__name__)
# Establecemos seguridad para nuestro programa:
app.config['SECRET_KEY'] = 'erjkqhfvdnie783492hjsdhy4herqoi$()djhfejroejakjior$hrejkd347[]7$'
# Configuramos SQLAlchemy para que se comunique con nuestra base de datos Postgre
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://daniel:asir23@Localhost:5432/proyectodb'
# Como ahora es un entorno de pruebas establecemos que no se nos envíe una señal cada vez que realizamos cambios.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Hacemos que el ORM se utilice en la app
db.init_app(app)

# Creamos el objeto de la clase LoginManager que llamamos login_manager. Esto permitirá el control de sesiones.
login_manager.init_app(app)
login_manager.login_view = "login"


# Utilizamos esto para crear tabla por convención se llama create_table. Necesitamos utilizar uan función
# llamada create_all con la instancia de sqlalchemy (db).
# El decorador hace que se llame solo la primera vez
""""@app.before_first_request
def create_table():
    db.create_all()
"""


@app.route("/")
def app_proyecto():
    return render_template('index.html')


@app.route('/acceso', methods=["GET", "POST"])
def acceso():
    if request.method == "POST":
        return redirect(url_for("app_proyecto"))
    return render_template("acceso.html")


@app.route('/informacion')
def informacion():
    return render_template("informacion.html")


@app.route('/registros', methods=["GET", "POST"])
def registros():
    if request.method == "POST":
        return redirect(url_for("app_proyecto"))

    """form = SignupForm()

    if form.validate_on_submit():
        return redirect(url_for("app_proyecto"))"""
    """ , form=form"""

    return render_template("registros.html")


"""def hola():
    # return "<h1 style='color:blue'> Este test Funciona! </h1>" para la prueba inicial.
    # return "<h1 style='color:green'> Funciona gunicorn! </h1>"
    return "<h1 style='color:red'> Funciona NGINX! </h1>"""""

if __name__ == "__main__":
    app.run(host='0.0.0.0')
