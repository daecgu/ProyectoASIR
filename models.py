# Importamos las librerías necesarias para poder guardar contraseñas de forma segura.
from werkzeug.security import generate_password_hash, check_password_hash
# Importamos las librerias para poder crear usuarios y gestionar el login.
from flask_login import UserMixin, LoginManager
# Importamos nuestro ORM para realizar los mapeos.
from flask_sqlalchemy import SQLAlchemy

# Para poder realizar la gestion de logins
login_manager = LoginManager()
# Para poder realizar mapeos ORM
db = SQLAlchemy()


class User(UserMixin, db.Model):
    # Indicamos dónde se va a guardar
    __tablename__ = "Usuarios"

    id = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    desc = db.Column(db.String(1024), nullable=False)

    # Generar un Hash para almacenar en la base de datos y no almacenar contraseñas.
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# User_loader nos permitirá cargar el usuario que ha hecho login
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


# debemos pasar por parámetro el ID y esto debe comprobar si existe el usuario.
def get_user():
    return True
