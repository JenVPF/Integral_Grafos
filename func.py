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

