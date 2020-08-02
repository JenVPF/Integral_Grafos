from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, SelectField, StringField
#Guardar, Cargar Archivo, Numero, Lista desplegable, string
from wtforms.validators import Required	
from werkzeug.datastructures import MultiDict

class UploadForm(FlaskForm):
    archivo = FileField('Archivo', validators = [Required("Tienes que subir el archivo")])
    cant_camiones = IntegerField('Cantidad Camiones',validators = [])
    
    submit = SubmitField(' Enviar ')

class DetalleForm(FlaskForm):
    camion = SelectField('Camion', choices = [(0,'--')])
    centro = SelectField('Centro Distribucion', choices = [(0,'--')])
    punto = SelectField('Punto de Ventas', choices = [(0,'--')])
    productos = IntegerField('Cantidad de Productos', validators = [])

    agregar = SubmitField('+')