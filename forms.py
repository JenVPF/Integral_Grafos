from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, SelectField, StringField
#Guardar, Cargar Archivo, Numero, Lista desplegable, string
from wtforms.validators import Required	
from werkzeug.datastructures import MultiDict

class UploadForm(FlaskForm):
    archivo = FileField('Archivo', validators = [Required("Tienes que subir el archivo")])
    
    submit = SubmitField(' Enviar ')

class DetalleForm(FlaskForm):
    centro = SelectField('Centro Distribucion', choices = [(0,'--')])
    punto = StringField('Punto de Ventas', validators = [Required("No puede dejar el campo vacio")])
    productos = StringField('Cantidad de Productos', validators = [Required("No puede dejar el campo vacio")])

    agregar = SubmitField('+')

