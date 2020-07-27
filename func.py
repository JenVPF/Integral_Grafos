def lecturaArchivo(ar):
    archivo = open(ar)

    lectura = archivo.read()

    archivo.close()

    print(lectura)