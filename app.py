from flask import Flask, render_template, request, redirect, url_for
#Formulario
from werkzeug.utils import secure_filename
#Llamada Funciones
from forms import UploadForm, DetalleForm
from func import lecturaArchivo, Parametros
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about', methods = ['GET', 'POST'])
def about():
    form = UploadForm()
    global filename
    if request.method == 'POST' and form.validate_on_submit():
        arch= form.archivo.data
        filename = secure_filename(arch.filename) #Nombre del Archivo 
        arch.save(app.root_path+"./static/archivos/"+filename) #Donde se guarda
        return redirect(url_for('datos'))
    return render_template("about.html", form=form)

@app.route('/datos', methods = ['GET', 'POST'])
def datos():
    form = DetalleForm()
    Param = lecturaArchivo(filename) #Arreglo de Clases
    
    #crea dict tipo {Centro:{PtoVenta:Distancia}}
    #Variables
    Centros = {} #Dic Centros {N:[x,y]}
    Puntos = {} #Dic Puntos {N:[x,y]}
    aux = Parametros()
    message = ''

    print('Arreglo de clases: ', Param)

    for i in range(0,len(Param)):
        aux = Param[i]
        k = aux.N
        if aux.T == 'C':
            Centros[k] = [aux.X,aux.Y]
        else:
            Puntos[k] = [aux.X,aux.Y]
    
    form.centro.choices = [(key, 'C'+str(key)) for key in Centros.keys()]
    form.punto.choices = [(key, 'P'+str(key)) for key in Puntos.keys()]

    #if request.method == 'POST':
        #[(i,'q'+str(i-1)) for i in range(len(transitions1)+1)]
        #trans.origen1.choices[0] = (0,'-')

    if request.method == 'POST' and form.validate_on_submit():
        camion = form.camion.data
        centro = form.centro.data
        punto = form.punto.data
        productos = form.productos.data
        message = 'El camion '+str(camion)+' esta asignado a el Centro de distribucion '+str(centro)+' y va al Punto de venta '+str(punto)+' llevando '+str(productos)+' productos'
        
    return render_template("datos.html", form=form, message=message)

if __name__ == '__main__':
    app.run(debug=True)