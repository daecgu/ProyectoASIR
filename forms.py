# Este será nuestro archivo para validación de formularios.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea


class SignupForm(FlaskForm):
    id = StringField('DNI', validators=[DataRequired(), Length(9)])
    name = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=256)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(max=50)])
    descripcion = StringField('Información', validators=[DataRequired(), Length(max=1024)], widget=TextArea())

    submit = SubmitField('Registrate')


class LoginForm(FlaskForm):
    id = StringField('DNI', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Accede')
