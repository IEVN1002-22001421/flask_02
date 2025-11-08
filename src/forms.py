from wtforms import Form, IntegerField, SubmitField, StringField, RadioField
from wtforms import validators

class userform(Form):
    matricula = IntegerField("Matricula", [
        validators.DataRequired(message="El campo es requerido")
    ])

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])

    apellido = StringField("Apellido", [
        validators.DataRequired(message="El campo es requerido")
    ])

    coreo = StringField("Correo", [
        validators.DataRequired(message="El campo es requerido")
    ])

class PedidoForm(Form):
    nombre = StringField("Nombre")
    direccion = StringField("Direccion") 
    telefono = StringField("Telefono")
    
    tamanio = RadioField("Tamaño Pizza", choices=[
        ('chica', 'Chica $60'),
        ('mediana', 'Mediana $80'), 
        ('grande', 'Grande $120')
    ], default='chica')
    
    ingredientes = RadioField("Ingredientes", choices=[
        ('jamon', 'Jamón 10$'),
        ('piña', 'Piña 10$'),
        ('champiñones', 'Champiñones 10$'),
        
    ], default='jamon')
    
    num_pizzas = IntegerField("NumPizzas", default=1)
    
    btn_agregar = SubmitField("Agregar")
    btn_quitar = SubmitField("Quitar")
    btn_terminar = SubmitField("Terminar")