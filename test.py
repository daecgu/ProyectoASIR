# Importamos Flask, render_template para los archivos html y url for para los links.
from flask import Flask, render_template, url_for, request, redirect
# Importamos para gestionar login
from flask_login import current_user, login_user, logout_user, login_required
# Importamos de los models los el usuario, la instancia del orm y el login manager.
from models import User, login_manager, db
# Importamos la clase para validar el formulario
from forms import SignupForm, LoginForm, ModifyForm, DeleteForm

# Creamos una instancia Flask que se llama app
app = Flask(__name__)
# Establecemos seguridad para nuestro programa. A una sesión con cada cliente se le asigna un ID de sesión. 
# Los datos de la sesión se almacenan sobre cookies y el servidor los firma criptográficamente. Para este cifrado
# las aplicaciones flask necesitan una "SECRET_KEY" definida, y es lo que hacemos con la siguiente línea. 
# noinspection SpellCheckingInspection
app.config['SECRET_KEY'] = 'erjkqhfvdnie783492hjsdhy4herqoi$()djhfejroejakjior$hrejkd347[]7$84932yutrewjgw89th4w84hh'
# Configuramos SQLAlchemy para que se comunique con nuestra base de datos Postgre
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://daniel:asir23@localhost:5432/proyectodb'
# Como ahora es un entorno de pruebas establecemos que no se nos envíe una señal cada vez que realizamos cambios.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Hacemos que el ORM, la instancia db de SQLAlchemy está en models, se utilice en la app
db.init_app(app)
# Creamos el objeto de la clase LoginManager que llamamos login_manager. Esto permitirá el control de sesiones.
login_manager.init_app(app)
# Si no ha iniciado sesión e intenta acceder a una parte restringida a usuarios registrados le llevará a acceso
login_manager.login_view = "acceso"


# Utilizamos esto para crear tabla las tablas: por convención se llama create_table. Necesitamos utilizar uan función
# llamada create_all con la instancia de sqlalchemy (db).
# El decorador hace que se llame solo la primera vez
@app.before_first_request
def create_table():
    db.create_all()

# el decorador @app.route indica la URL con la que vamos a visualizar la web
# se le pueden añadir parámetro para tener una "url" dinámica y pasar parámetro mediante la URL
# En el proyecto no utilizaremos url dinámicas. Además le añadimos los métodos que va a admitir.
@app.route("/", methods=["GET", "POST"])
def app_proyecto():
    form = DeleteForm()
    if form.validate_on_submit():
        current_user_id = current_user.id
        logout_user()
        # Con la siguiente sentencia lo que se hace es una consulta del modelo User, y una vez encontrado por id lo elimina.
        User.query.filter_by(id=current_user_id).delete()
        db.session.commit()
    # A continuación utilizaremos el motor de plantillas Jinja2. En lugar de devolver código HTML desde la función, 
    # se renderiza un archivo HTML mediante la función render_template, a la cual le pasamos por parámetro
    # el nombre del archivo que se encuentra en la carpeta /templates. También le pasamos el formulario como parámetro.
    # el "sistema de plantillas web" es una forma mediante la cual los datos variables pueden insertarse de forma variable.
    # Así nuestra plantillas web contienen marcadores de posición de sintaxis HTML intercalados para variables y expresiones,
    # que son valores reemplazados cuando se renderiza la plantilla. 
    return render_template('index.html', form=form)
""" Jinja2 para los archivos HTML:
{% ... %} Sentencias
{{ ... }} Expresiones, variables para mostrar en la salida de la plantilla
{# ... #} comentarios no incluidos en la salida de la plantilla
"""

# En elste decorador, si en vez de /acceso fuese /acceso/ se convertiría en una URL canónica, que son links
# con el atributo canónico('rel='canonical'), que sirven para indicar a los buscadores web qué deben mostrar.
# En nuestro caso si pusieramos /acceso/ terminaría en un resultado error 404 página no encontrada.
@app.route('/acceso', methods=["GET", "POST"])
def acceso():
    if current_user.is_authenticated:
        # url_for es muy útil para consturir dinámicamente una URL para una función específica. LA función acepta el nombre
        # de una función como primer argumento, y uno o más argumentos de palabra clave,
        # que corresonderían a la parte variable de la URL.
        return redirect(url_for("app_proyecto"))

    form = LoginForm()
    if form.validate_on_submit():
        # request.form es un objeto de tipo diccionario que contiene los datos del formulario enviado a través
        # de una petición POST, en este caso se le especifica que recupere el que tiene por clave "id". 
        dni = request.form["id"]
        user = User.query.filter_by(id=dni).first()

        if user is not None and user.check_password(request.form["password"]):
            login_user(user)
            # redirect es una función que devuelve un objeto de respuesta y redirige al usuario a otra ubucación de destino
            # con el estado especificado: redirect(location, statuscode, response)
            return redirect("/informacion")

    return render_template("acceso.html", form=form)


@app.route('/registros', methods=["GET", "POST"])
def registros():
    # Si el usuario ha accedido que no pueda registrarse:
    if current_user.is_authenticated:
        return redirect(url_for("app_proyecto"))

    form = SignupForm()
    if form.validate_on_submit():
        dni = form.id.data
        nombre = form.name.data
        email = form.email.data
        password = form.password.data
        descripcion = form.descripcion.data
        # en la variable user que es un objeto de tipo User, se crea con los datos del formulario.
        user = User(id=dni, name=nombre, email=email, desc=descripcion)
        user.set_password(password)
        # SQLAlchemy añade el usuario a la Base de Datos y confirma la acción.  
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("app_proyecto"))

    return render_template("registros.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("app_proyecto"))


# Login_required nos indica que necesitas haber iniciado sesión para poder acceder.
@app.route('/informacion', methods=["GET", "POST"])
@login_required
def informacion():
    form = ModifyForm()
    if form.validate_on_submit():
        current_user.desc = form.descripcion.data
        db.session.commit()
    return render_template("informacion.html", form=form)


# Esto son las pruebas que realizamos inicialmente para comprobar que funcionaban los servidores.
"""def hola():
    # return "<h1 style='color:blue'> Este test Funciona! </h1>" para la prueba inicial.
    # return "<h1 style='color:green'> Funciona gunicorn! </h1>"
    return "<h1 style='color:red'> Funciona NGINX! </h1>"""""


if __name__ == "__main__":
    # app.run(host, port, debug, options) host=0.0.0.0 Nos permite servir la aplicación externamente
    # en otro caso solo la servirá en 127.0.0.1 (localhost). El puerto por defecto es 5000. 
    # Debug por defecto es false, por lo que comienza sirviendo en modo "producción".
    app.run(host='0.0.0.0')
