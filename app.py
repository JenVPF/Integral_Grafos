from flask import Flask, render_template, request, redirect, url_for
#Formulario
from werkzeug.utils import secure_filename
#Llamada Funciones
from forms import UploadForm, DetalleForm
from func import lecturaArchivo, Parametros, Conexion, ordenarDatos
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
    global ruta
    ruta = [] #clases conexion

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
    global conexiones
    conexiones = Conexion()
    Param = lecturaArchivo("./static/archivos/"+filename) #Arreglo de Clases
    Centros = {} #Dic Centros {N:[x,y]}
    Puntos = {} #Dic Puntos {N:[x,y]}
    aux = Parametros()
    aux1 = Conexion()
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
            for i in ruta:
                aux1 = ruta.pop()
                if(aux1.idCam == camion): #Mismo Camion
                    print('Lista llena y mismo camion que el anterior')
                    if(aux1.idCen == centro): #Mismo centro
                        Pun = aux1.Punto
                        Prod = aux1.Cant
                        Pun.append(punto)
                        Prod.append(productos)
                        aux1.Punto = Pun
                        aux1.Cant = Prod
                    else: #no es el mismo centro anterior
                        message2 = 'Un camion se puede asignar solo a un Centro de distribucion, intente nuevamente'
                ruta.append(aux1)
                if(aux1.idCam != camion):
                    print('lista llena y camion distinto al anterior')
                    conexiones.idCam = camion
                    conexiones.idCen = centro
                    Pun.append(punto)
                    Prod.append(productos)
                    conexiones.Punto = Pun
                    conexiones.Cant = Prod
                    ruta.append(conexiones)
        else: #Vacio 
            print('lista vacia')
            conexiones.idCam = camion
            conexiones.idCen = centro
            Pun.append(punto)
            Prod.append(productos)
            conexiones.Punto = Pun
            conexiones.Cant = Prod
            ruta.append(conexiones)

        #return redirect(url_for('datos'))
    if request.method == 'POST' and request.form.get('enviar', True) == 'Enviar' :
        return redirect('rutas')

    return render_template("datos.html", form=form, message=message, message2=message2)

@app.route('/rutas', methods = ['GET', 'POST'])
def rutas():
    aux = Conexion()
    print(ruta)
    for i in ruta: 
        aux = i 
        aux.mostrar()
    """for i in ruta:
        aux = ruta.pop()
        print('###########')
        aux.mostrar()
        aux.Punto = ordenarDatos(aux.Punto)
        aux.Cant = ordenarDatos(aux.Cant)
        print('###########')
        aux.mostrar()
        ruta.append(aux)"""
    
    return render_template("rutas.html")

if __name__ == '__main__':
    app.run(debug=True,port=3000)