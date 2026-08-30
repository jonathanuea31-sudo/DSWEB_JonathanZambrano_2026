from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):
    """Formulario para registrar o editar un producto.

    Se reutiliza tanto para el alta de un nuevo producto como para
    una futura edición, ya que solo cambian los valores iniciales
    con los que se instancia (form = ProductoForm(obj=producto)).
    """

    nombre = StringField(
        'Nombre del producto',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=80, message='Debe tener entre 3 y 80 caracteres.')]
    )

    categoria = SelectField(
        'Categoría',
        choices=[
            ('Tecnología', 'Tecnología'),
            ('Mobiliario', 'Mobiliario'),
            ('Suministros', 'Suministros'),
        ],
        validators=[DataRequired(message='Seleccione una categoría.')]
    )

    precio = FloatField(
        'Precio ($)',
        validators=[DataRequired(message='El precio es obligatorio.'),
                    NumberRange(min=0.01, message='El precio debe ser mayor a 0.')]
    )

    stock = IntegerField(
        'Stock disponible',
        validators=[DataRequired(message='El stock es obligatorio.'),
                    NumberRange(min=0, message='El stock no puede ser negativo.')]
    )

    submit = SubmitField('Guardar Producto')
