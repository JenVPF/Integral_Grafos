from flask import Flask, render_template, request, redirect, url_for
#Formulario
from werkzeug.utils import secure_filename
#Llamada Funciones
from forms import UploadForm, DetalleForm
from func import lecturaArchivo, validacionString, validarPuntos, distancia_de_lista, CDconCoordenadasdePV, DistanciasEntreNodos
from config import Config
import pandas as pd
app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about', methods = ['GET', 'POST'])
def about():
    #Formulario
    form = UploadForm()
    #Variables
    global filename 
    global Asignacion
    global TablaI
    Asignacion = {}

    if request.method == 'POST' and form.validate_on_submit():
        arch= form.archivo.data
        filename = secure_filename(arch.filename) #Nombre del Archivo 
        arch.save(app.root_path+"./static/archivos/"+filename) #Donde se guarda
        TablaI = lecturaArchivo("./static/archivos/"+filename) #Tabla Inicial desde el TXT
        return redirect(url_for('datos'))

    return render_template("about.html", form=form)

@app.route('/datos', methods = ['GET', 'POST'])
def datos():
    #Formulario
    form = DetalleForm()
    #Variables
    Centros = {} #Dic Centros {N:[x,y]}
    Puntos = {} #Dic Puntos {N:[x,y]}
    Pun = [] #Arreglo de con IdPuntos
    Prod = [] #Arreglo con CantProductos
    datos = []
    #Mensajes
    message = ''
    message2 = ''
    message3 = ''
    message4 = ''
    
    #Llenando los diccionarios Centros y Puntos
    for n in range(0,len(TablaI.index)): #Index es para el largo de las filas
        if(TablaI["T"][n]== 'C'):
            Centros[TablaI["N"][n]]= TablaI["X,Y"][n]
        else:
            Puntos[TablaI["N"][n]]= TablaI["X,Y"][n]

    #Opciones desplegables formulario
    form.centro.choices = [(key, 'C'+str(key)) for key in Centros.keys()]
    form.punto.choices = [(key, 'P'+str(key)) for key in Puntos.keys()]

    #TABLAS CENTROS Y PUNTOS 
    #REVISAR
    C = pd.DataFrame( (key, Centros[key]) for key in Centros.keys() )
    C.columns = ["N", "X,Y"]
    P = pd.DataFrame( (key, Puntos[key]) for key in Puntos.keys() )
    P.columns = ["N", "X,Y"]

    if request.method == 'POST' and form.validate_on_submit():

        centro = form.centro.data #Id_Centro int 
        punto = form.punto.data #Id_Punto string
        productos = form.productos.data #Cant_Productos string

        if(validacionString(punto)==True and validacionString(productos)==True): #Valido que los Puntos y Productos se ingresaron correctamente
            print(chr(27)+"[;34m"+"String Validados")
            Pun = punto.split(',')
            Prod = productos.split(',')
            if(len(Pun)==len(Prod)):
                print(chr(27)+"[;34m"+"Validacion Largo Puntos y Productos")
                if(validarPuntos(P,Pun)==True):
                    print(chr(27)+"[;34m"+"Validacion Puntos")
                    print('')
                    print(chr(27)+"[;34m"+'Puntos: ', Pun)
                    print(chr(27)+"[;34m"+'Productos: ', Prod)
                    datos.append(Pun) #Puntos Guardados
                    datos.append(Prod)
                    Asignacion[centro] = datos
                    #Asignacion = { idCentro : [ [Puntos] , [Productos] ] }
                else:
                    message3='Un Punto de venta ingresado no es valido'
            else:
                message4 = 'Ingrese la misma cantidad de Puntos de venta y Productos'
            message = 'El Centro de distribucion '+str(centro)+' y va a los Puntos de venta '+str(punto)+' llevando '+str(productos)+' productos respectivamente'
        else: 
            message2 = 'Ingrese un formato valido'
        #return redirect(url_for('datos'))
    if request.method == 'POST' and request.form.get('enviar', True) == 'Enviar' :
        return redirect('rutas')

    return render_template("datos.html", form=form, message=message, message2=message2,message3=message3,message4=message4,T1=[C.to_html(classes='data', header="true")], T2=[P.to_html(classes='data', header="true")])

@app.route('/rutas', methods = ['GET', 'POST'])
def rutas():
    #Asignacion = { idCentro : [ [Puntos] , [Productos] ] }
    #Centro = { id : [PuntoA,PunetoB,PuntoC] }
    #Puntos = { id : cant , id2 : cant }
    print('')
    print(chr(27)+"[;34m"+"Valores Asignados: ",Asignacion)
    centros = {}
    puntos = {}
    return render_template("rutas.html", Asignacion=Asignacion)

if __name__ == '__main__':
    app.run(debug=True,port=3000)