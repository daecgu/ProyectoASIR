# Importamos el ORM
from flask_sqlalchemy import SQLAlchemy
# Importamos Flask, render template para los archivos html y url for para los links.
from flask import Flask, render_template, url_for, request, redirect
# Importamos para gestionar login
from flask_login import current_user, login_user, logout_user, login_required
# Importamos de los models los el usuario, la instancia del orm y el login manager.
from models import User, login_manager, db, get_user
# Importamos la clase para validar el formulario
from forms import SignupForm, LoginForm

# Creamos una instancia Flask que se llama app
app = Flask(__name__)
# Establecemos seguridad para nuestro programa:
# noinspection SpellCheckingInspection
app.config['SECRET_KEY'] = 'erjkqhfvdnie783492hjsdhy4herqoi$()djhfejroejakjior$hrejkd347[]7$'
# Configuramos SQLAlchemy para que se comunique con nuestra base de datos Postgre
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://daniel:asir23@Localhost:5432/proyectodb'
# Como ahora es un entorno de pruebas establecemos que no se nos envíe una señal cada vez que realizamos cambios.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Hacemos que el ORM se utilice en la app
db.init_app(app)

# Creamos el objeto de la clase LoginManager que llamamos login_manager. Esto permitirá el control de sesiones.
login_manager.init_app(app)
# Si no está logeado e intenta acceder a una parte de la web restringida a usuarios registrados le llevará a acceso
login_manager.login_view = "acceso"


# Utilizamos esto para crear tabla por convención se llama create_table. Necesitamos utilizar uan función
# llamada create_all con la instancia de sqlalchemy (db).
# El decorador hace que se llame solo la primera vez
"""@app.before_first_request
def create_table():
    db.create_all()
"""


@app.route("/")
def app_proyecto():
    return render_template('index.html')


@app.route('/acceso', methods=["GET", "POST"])
def acceso():
    if current_user.is_authenticated:
        return redirect(url_for("app_proyecto"))

    form = LoginForm()
    if form.validate_on_submit():
        # esto hay que hacer algo 131
        """ if user is not None and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get("next")
                if not next_page:
                    next_page=url_for("acceso")
                return redirect(next_page)
                #aquí hay varias cosas que no entiendo voy a ver si puedo entender el código más adelante"""
        print('Hello world')

    """
    # Método de validación simple    
    if request.method == "POST":
        return redirect(url_for("app_proyecto"))
    """

    return render_template("acceso.html", form=form)

# Login_required nos indica que necesitas estar logeado para poder acceder.
@app.route('/informacion')
@login_required
def informacion():
    return render_template("informacion.html")


@app.route('/registros', methods=["GET", "POST"])
def registros():
    """
    # Comprobación básica de que funciona un formulario http sencillo.
    if request.method == "POST":
        return redirect(url_for("app_proyecto"))
        """

    form = SignupForm()
    if form.validate_on_submit():
        return redirect(url_for("app_proyecto"))

    return render_template("registros.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("app_proyecto"))


"""def hola():
    # return "<h1 style='color:blue'> Este test Funciona! </h1>" para la prueba inicial.
    # return "<h1 style='color:green'> Funciona gunicorn! </h1>"
    return "<h1 style='color:red'> Funciona NGINX! </h1>"""""

if __name__ == "__main__":
    app.run(host='0.0.0.0')
