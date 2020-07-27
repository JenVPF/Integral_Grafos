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
    if request.method == 'POST' and form.validate_on_submit():
        arch= form.archivo.data #Set?
        filename = secure_filename(arch.filename)
        arch.save(app.root_path+"/archivo/"+filename)
        return render_template("datos.html")
    return render_template("about.html", form=form)

@app.route('/datos')
def datos():
    return render_template("datos.html")

if __name__ == '__main__':
    app.run(debug=True)