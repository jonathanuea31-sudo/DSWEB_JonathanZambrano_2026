from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProveedorForm(FlaskForm):
    """Formulario para registrar o editar un proveedor."""

    nombre = StringField(
        'Nombre o razón social',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )

    contacto = StringField(
        'Persona de contacto',
        validators=[DataRequired(message='El contacto es obligatorio.'),
                    Length(min=3, max=80, message='Debe tener entre 3 y 80 caracteres.')]
    )

    ciudad = StringField(
        'Ciudad',
        validators=[DataRequired(message='La ciudad es obligatoria.'),
                    Length(min=3, max=60, message='Debe tener entre 3 y 60 caracteres.')]
    )

    calificacion = IntegerField(
        'Calificación (1 a 5)',
        validators=[DataRequired(message='La calificación es obligatoria.'),
                    NumberRange(min=1, max=5, message='La calificación debe estar entre 1 y 5.')]
    )

    submit = SubmitField('Guardar Proveedor')
