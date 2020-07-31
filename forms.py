from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, SelectField, StringField
#Guardar, Cargar Archivo, Numero, Lista desplegable, string
from wtforms.validators import Required	

class UploadForm(FlaskForm):
    archivo = FileField('Archivo', validators = [Required("Tienes que subir el archivo")])
    
    submit = SubmitField(' Subir ')

class DetalleForm(FlaskForm):
    camion = StringField('Camion', validators = [])
    centro = SelectField('Centro Distribucion', choices = [(0,'--')])
    punto = SelectField('Punto de Ventas', choices = [(0,'--')])
    productos = IntegerField('Cantidad de Productos', validators = [])

    submit = SubmitField('Subir')