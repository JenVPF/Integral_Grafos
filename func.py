class Parametros:
    def init(self, T, N, X, Y):
        self.T = T #C o P
        self.N = N #Id int
        self.X = X #coordenada x int
        self.Y = Y #coordenada y int
    def mostrar(self):
        print(self.T)
        print(self.N)
        print(self.X)
        print(self.Y)

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
    archivo = open(ar)
    Rutas = []
    for linea in archivo:
        dato = linea.split(';') #Separo la linea por los ; y lo guardo en un arreglo
        R = Almacenar(dato)
        Rutas.append(R)
    archivo.close()
    return Rutas

def Almacenar(linea):
    Datos = Parametros()
    Datos.T = linea[0] #Guardo los datos del arreglo en la clase
    Datos.N = linea[1]
    C = linea[2].split(',') #Separo las coordenadas por la , 
    Datos.X=int(C[0]) #Guardo coordenada X 
    Datos.Y=int(C[1]) #Guardo coordenada Y
    return Datos

def ordenarDatos(datos): #datos es la lista
    aux = set(datos)
    aux1 = []
    for i in aux:
        aux1.append(i)
    aux1 = sorted(aux1)
    return aux1

