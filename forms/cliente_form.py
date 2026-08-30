from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):
    """Formulario para registrar o editar un cliente."""

    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )

    email = StringField(
        'Correo electrónico',
        validators=[DataRequired(message='El correo es obligatorio.'),
                    Email(message='Ingrese un correo electrónico válido.')]
    )

    telefono = StringField(
        'Teléfono',
        validators=[DataRequired(message='El teléfono es obligatorio.'),
                    Length(min=7, max=15, message='Debe tener entre 7 y 15 dígitos.')]
    )

    activo = BooleanField('Cliente activo', default=True)

    submit = SubmitField('Guardar Cliente')
