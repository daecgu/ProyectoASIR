# Este será nuestro archivo para validación de formularios.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    id = StringField('id', validators=[DataRequired(), Length(9)])
    name = StringField('nombre', validators=[DataRequired(), Length(max=50)])
    email = StringField('emails', validators=[DataRequired(), Email(), Length(max=256)])
    password = PasswordField('password', validators=[DataRequired(), Length(max=50)])
    descripcion = StringField('descripcion', validators=[DataRequired(), Length(max=1024)])

    submit = SubmitField('envio_formulario')
