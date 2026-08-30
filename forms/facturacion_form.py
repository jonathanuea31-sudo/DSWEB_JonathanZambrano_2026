from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):
    """Formulario para registrar o editar una factura."""

    numero = StringField(
        'Número de factura',
        validators=[DataRequired(message='El número de factura es obligatorio.'),
                    Length(min=4, max=20, message='Debe tener entre 4 y 20 caracteres.')]
    )

    cliente = StringField(
        'Nombre del cliente',
        validators=[DataRequired(message='El cliente es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )

    total = FloatField(
        'Total ($)',
        validators=[DataRequired(message='El total es obligatorio.'),
                    NumberRange(min=0.01, message='El total debe ser mayor a 0.')]
    )

    estado = SelectField(
        'Estado',
        choices=[('Pagada', 'Pagada'), ('Pendiente', 'Pendiente')],
        validators=[DataRequired(message='Seleccione un estado.')]
    )

    submit = SubmitField('Guardar Factura')
