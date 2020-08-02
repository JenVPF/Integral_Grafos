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
    global conexiones
    conexiones = Conexion()
    global ruta
    ruta = []

    if request.method == 'POST' and form.validate_on_submit():
        arch= form.archivo.data
        filename = secure_filename(arch.filename) #Nombre del Archivo 
        arch.save(app.root_path+"./static/archivos/"+filename) #Donde se guarda
        num_camiones = form.cant_camiones.data
        return redirect(url_for('datos'))
    return render_template("about.html", form=form)

@app.route('/datos', methods = ['GET', 'POST'])
def datos():
    #Formulario
    form = DetalleForm()
    #Variables
    Param = lecturaArchivo("./static/archivos/"+filename) #Arreglo de Clases
    Centros = {} #Dic Centros {N:[x,y]}
    Puntos = {} #Dic Puntos {N:[x,y]}
    aux = Parametros()
    aux1 = Parametros()
    aux2 = Conexion()
    message = ''
    message2 = ''
    Pun = []
    Prod = []

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

        camion = form.camion.data #Id_Camion
        centro = form.centro.data #Id_Centro
        punto = form.punto.data #Id_Punto
        productos = form.productos.data #Cant_Productos
        
        message = 'El camion '+str(camion)+' esta asignado a el Centro de distribucion '+str(centro)+' y va al Punto de venta '+str(punto)+' llevando '+str(productos)+' productos'
        
        if ruta: #No vacio, buscar el dato guardado
            #Opcion no esta vacio pero el dato es nuevo
            for k in range(0, len(ruta)):
                aux2 = ruta[k]
                if(aux2.idCam == camion): #Si estamos en el mismo camion
                    aux = aux2.idCen #Centro al que esta asignado ese camion 
                    if(aux.N == centro): #Si es el mismo centro que el camion 
                        for j in range(0,len(Param)): #Busco el nueo Punto que se añadio 
                            aux1 = Param[j]
                            Pun = aux2.Punto #Saco el arreglo guardado
                            Prod = aux2.Cant
                            if punto==aux1.N:
                                Pun.append(aux1) #Añado el Punto a la lista
                                Prod.append(productos) #Añado el producto a la lista 
                                aux2.Cant = Prod
                                aux2.Punto = Pun
                        ruta.append(aux2)
                    else: #Si no es el mismo centro que el camion 
                        message2 = 'Un camion se puede asignar solo a un Centro de distribucion, intente nuevamente'
        else: #Vacio 
            conexiones.idCam = camion #Añade IdCamion a la clase 
            Prod.append(productos) #Añado el producto a la lista
            conexiones.Cant = Prod #Añado la lista a la Clase
            for k in range(0,len(Param)):
                aux = Param[k]
                if centro==aux.N:
                    conexiones.idCen = aux #Añado el Centro a la Clase
                if punto==aux.N:
                    Pun.append(aux) #Añado el Punto a la lista
                    conexiones.Punto = Pun #Añado la lista a la Clase
            ruta.append(conexiones)
    
    if request.method == 'POST' and request.form.get('enviar', True) == 'Enviar' :
        return redirect('rutas')

    return render_template("datos.html", form=form, message=message, message2=message2)

@app.route('/rutas', methods = ['GET', 'POST'])
def rutas():
    aux = Conexion()
    print(ruta)
    return render_template("rutas.html")

if __name__ == '__main__':
    app.run(debug=True,port=3000)