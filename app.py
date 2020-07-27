from flask import Flask, render_template, request, redirect, url_for
#Formulario
from werkzeug import secure_filename
#Llamada Funciones
from forms import UploadForm
from func import lecturaArchivo
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

@app.route('/datos')
def datos():
    lec = lecturaArchivo(filename)
    return render_template("datos.html", lec=lec)

if __name__ == '__main__':
    app.run(debug=True)