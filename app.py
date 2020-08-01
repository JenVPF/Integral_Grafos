from flask import Flask, render_template, request, redirect, url_for
#Formulario
from werkzeug.utils import secure_filename
#Llamada Funciones
from forms import UploadForm, DetalleForm
from func import lecturaArchivo, Parametros, Conexion
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about', methods = ['GET', 'POST'])
def about():
    #Variables
    form = UploadForm()
    global filename
    global num_camiones

    if request.method == 'POST' and form.validate_on_submit():
        arch= form.archivo.data
        filename = secure_filename(arch.filename) #Nombre del Archivo 
        arch.save(app.root_path+"./static/archivos/"+filename) #Donde se guarda
        num_camiones = form.cant_camiones.data
        return redirect(url_for('datos'))
    return render_template("about.html", form=form)

@app.route('/datos', methods = ['GET', 'POST'])
def datos():
    #Variables
    form = DetalleForm()
    Param = lecturaArchivo("./static/archivos/"+filename) #Arreglo de Clases
    Centros = {} #Dic Centros {N:[x,y]}
    Puntos = {} #Dic Puntos {N:[x,y]}
    aux = Parametros()
    message = ''
    global conexiones
    conexiones = Conexion()

    for i in range(0,len(Param)):
        aux = Param[i]
        k = aux.N
        if aux.T == 'C':
            Centros[k] = [aux.X,aux.Y]
        else:
            Puntos[k] = [aux.X,aux.Y]
    #print('Arreglo de clases: ', Param)
    form.camion.choices = [(key+1, str(key+1)) for key in range(num_camiones)]
    form.centro.choices = [(key, 'C'+str(key)) for key in Centros.keys()]
    form.punto.choices = [(key, 'P'+str(key)) for key in Puntos.keys()]

    if request.method == 'POST' and form.validate_on_submit():
        ruta = []
        camion = form.camion.data #Id_Camion
        centro = form.centro.data #Id_Centro
        punto = form.punto.data #Id_Punto
        productos = form.productos.data #Cant_Productos
        
        message = 'El camion '+str(camion)+' esta asignado a el Centro de distribucion '+str(centro)+' y va al Punto de venta '+str(punto)+' llevando '+str(productos)+' productos'
        
        for k in range(0,len(Param)):
            aux = Param[k]
            if centro==aux.N:
                ruta.append(aux)
            if punto==aux.N:
                ruta.append(aux)
        
        ruta.append(productos)
        conexiones[camion]=ruta
    
    if request.method == 'POST' and request.form.get('enviar', True) == 'Enviar' :
        return redirect('rutas')
    

    return render_template("datos.html", form=form, message=message)

@app.route('/rutas', methods = ['GET', 'POST'])
def rutas():
    print(conexiones)
    return render_template("rutas.html")

if __name__ == '__main__':
    app.run(debug=True)