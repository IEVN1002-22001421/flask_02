from flask import Flask, render_template, request, make_response
import json
from datetime import datetime
import forms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    confirmacion = ""
    detalle = []
    total_pedido_actual = 0
    
    data_str = request.cookies.get("pedido_actual")
    if data_str:
        detalle = json.loads(data_str)
        for pizza in detalle:
            total_pedido_actual += pizza['subtotal']
    
    ventas_str = request.cookies.get("ventas", "[]")
    ventas = json.loads(ventas_str)

    form = forms.PedidoForm(request.form)
    
    if request.method == 'POST':
        if 'btn_agregar' in request.form:
            tamanio = request.form.get('tamanio')
            ingredientes = request.form.get('ingredientes')
            num_pizzas = int(request.form.get('num_pizzas', 1))
            
            precios = {'chica': 60, 'mediana': 80, 'grande': 120}
            subtotal = precios.get(tamanio, 0) * num_pizzas
            
            nueva_pizza = {
                'tamanio': tamanio,
                'ingredientes': ingredientes,
                'num_pizzas': num_pizzas,
                'subtotal': subtotal
            }
            
            detalle.append(nueva_pizza)
            
            total_pedido_actual = sum(pizza['subtotal'] for pizza in detalle)
            
            response = make_response(render_template('pizzeria.html', form=form, 
                                                   detalle=detalle, 
                                                   total_pedido_actual=total_pedido_actual,
                                                   ventas=ventas))
            response.set_cookie('pedido_actual', json.dumps(detalle))
            return response
            
        elif 'btn_quitar' in request.form:
            if detalle:
                detalle.pop()
                total_actualizado = sum(pizza['subtotal'] for pizza in detalle)
                
                response = make_response(render_template('pizzeria.html', form=form, 
                                                       detalle=detalle, 
                                                       total_pedido_actual=total_actualizado,
                                                       ventas=ventas))
                if detalle:
                    response.set_cookie('pedido_actual', json.dumps(detalle))
                else:
                    response.set_cookie('pedido_actual', '', expires=0)
                return response
                
        elif 'btn_terminar' in request.form:
            nombre = request.form.get('nombre', '')
            direccion = request.form.get('direccion', '')
            telefono = request.form.get('telefono', '')
            fecha = datetime.now().strftime("%d-%m-%Y")
            
            if not nombre:
                confirmacion = "Error: Debe ingresar el nombre del cliente"
            elif total_pedido_actual <= 0:
                confirmacion = "Error: El pedido está vacío o no tiene costo."
            else:
                nueva_venta = {
                    'nombre': nombre,
                    'direccion': direccion,
                    'telefono': telefono,
                    'fecha': fecha,
                    'total': total_pedido_actual
                }
                ventas.append(nueva_venta)
                
                confirmacion = f"Pedido terminado para {nombre}. Total: ${total_pedido_actual:.2f}"
                
                response = make_response(render_template('pizzeria.html', form=form, 
                                                       detalle=[], 
                                                       total_pedido_actual=0,
                                                       confirmacion=confirmacion,
                                                       ventas=ventas))
                response.set_cookie('pedido_actual', '', expires=0)
                response.set_cookie('ventas', json.dumps(ventas))
                return response
            
            return render_template('pizzeria.html', form=form, 
                                   detalle=detalle, 
                                   total_pedido_actual=total_pedido_actual,
                                   confirmacion=confirmacion,
                                   ventas=ventas)
    
    return render_template('pizzeria.html', form=form, 
                          detalle=detalle, 
                          total_pedido_actual=total_pedido_actual,
                          ventas=ventas)

@app.route('/ventas_totales')
def ventas_totales():
    ventas_str = request.cookies.get("ventas", "[]")
    ventas = json.loads(ventas_str)
    return render_template('ventas_totales.html', ventas=ventas)

@app.route('/index_original')
def index_original():
    titulo = "pagina de Inicio"
    listado = ['Python', 'Flask', 'pa']
    return render_template('index.html', titulo=titulo, listado=listado)

@app.route('/calculos', methods=['GET', 'POST'])
def calculos():
    if request.method == 'POST':
        numero1 = request.form['numero1']
        numero2 = request.form['numero2']
        suma = int(numero1) + int(numero2)
        return render_template('calculos.html', suma=suma, numero1=numero1, numero2=numero2)
    return render_template('calculos.html')

@app.route('/distancia')
def distancia():
    return render_template('distancia.html')

@app.route('/numero/<int:num>')
def mostrar_numero(num):
    return f"el numero es, {num}"

@app.route('/suma/<int:num1>/<int:num2>')
def suma_numeros(num1, num2):
    return f"el numero es, {num1 + num2}"

@app.route('/user/<int:id>/<string:username>')
def mostrar_usuario(id, username):
    return "ID: {} Nombre: {}".format(id,username)

@app.route('/suma/<float:n1>/<float:n2>')
def suma_floats(n1, n2):
    return "el numero es, {}".format(n1 + n2)

@app.route('/default')
@app.route('/default/<string:dft>')
def valor_default(dft="sss"):
    return f"el valor de dft es: " + dft

@app.route("/Alumnos", methods=['GET','POST'])
def alumnos():
    mat=0
    nom=""
    ape=""
    email=""
    alumno_class=forms.userform(request.form)
    if request.method == 'POST' and alumno_class.validate():
        mat=alumno_class.matricula.data
        nom=alumno_class.nombre.data
        ape=alumno_class.apellido.data
        email=alumno_class.coreo.data
        return render_template('Alumnos.html', form=alumno_class,
        mat=mat, nom=nom, ape=ape, email=email)
    return render_template('Alumnos.html', form=alumno_class)

@app.route('/prueba')
def pagina_prueba():
    return """
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>HTML 5 Boilerplate</title>
    <link rel="stylesheet" href="style.css">
    </head>
    <body>
    <script src="index.js"></script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)