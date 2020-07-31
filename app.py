from flask import Flask, render_template, request, redirect, url_for
#Formulario
from werkzeug import secure_filename
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
        arch.save(app.root_path+"./"+filename) #Donde se guarda
        return redirect(url_for('datos'))
    return render_template("about.html", form=form)

@app.route('/datos', methods = ['GET', 'POST'])
def datos():
    form = DetalleForm()
    Param = lecturaArchivo(filename) #Arreglo de Clases

    #Variables
    List_C = []
    List_P = []
    aux = Parametros()

    for i in range(0,len(Param)):
        aux = Param[i]
        if aux.T == 'C': 
            List_C.append(aux)
        else: 
            List_P.append(aux)
    

    if request.method == 'GET' and form.validate_on_submit():
        camion = form.camion.data
        centro = form.centro.data
        punto = form.punto.data
        productos = form.productos.data
    return render_template("datos.html", Param=Param, form=form)

if __name__ == '__main__':
    app.run(debug=True)