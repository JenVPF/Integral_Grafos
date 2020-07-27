from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import Required	

class UploadForm(FlaskForm):
    
    archivo = FileField('Archivo', validators = [Required("Tienes que subir el archivo")])
    
    submit = SubmitField(' Subir ')