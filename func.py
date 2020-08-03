import pandas as pd 

class Conexion:
    def init(self, idCam, idCen, Punto, Cant, Dis):
        self.idCam = idCam #int
        self.idCen = idCen 
        self.Punto = Punto 
        self.Cant = Cant 
        self.Dis = Dis
    def mostrar(self):
        print('Camion: ', self.idCam)
        print('Centro:', self.idCen)
        print('Punto: ', self.Punto)
        print('Cantidad: ', self.Cant)

def lecturaArchivo(ar):
    archivo = pd.read_csv(ar, sep=';', names=["T", "N", "X,Y"])
    archivo['X,Y']=archivo['X,Y'].str.split(',')
    print(archivo)
    print('')

    return archivo

def ordenarDatos(datos): #datos es la lista
    aux = set(datos)
    aux1 = []
    for i in aux:
        aux1.append(i)
    aux1 = sorted(aux1)
    return aux1

def validacionString(cadena): 
  if cadena.find(',') == -1: #Si no encuentra la ,
    return False
  else:
    for i in cadena: 
      if (i >= chr(32) and i <= chr(43)): 
        return False 
      elif (i >= chr(45) and i <= chr(47)):
        return False 
      elif (i >= chr(58) and i <= chr(254)):
        return False 
      else: 
        return True 

def validarPuntos(P,Pun):
    aux = []
    for n in range(0,len(P.index)): #Index es para el largo de las filas
        for m in Pun:
            if(int(P["N"][n]) == int(m)): #Verifico que los puntos ingresados sean validos
                aux.append(m)
    if(len(aux)==len(Pun)):
        return True
    else: 
        return False
