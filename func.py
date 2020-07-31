class Parametros:
    def init(self, T, N, X, Y):
        self.T = T
        self.N = N
        self.X = X
        self.Y = Y

def lecturaArchivo(ar):
    archivo = open(ar)
    Rutas = []
    Datos = Parametros()
    for linea in archivo:
        dato = linea.split(';') #Separo la linea por los ; y lo guardo en un arreglo
        Datos.T = dato[0] #Guardo los datos del arreglo en la clase
        Datos.N = dato[1]
        C = dato[2].split(',') #Separo las coordenadas por la , 
        Datos.X=int(C[0]) #Guardo coordenada X 
        Datos.Y=int(C[1]) #Guardo coordenada Y
        Rutas.append(Datos)

    archivo.close()
    return Rutas