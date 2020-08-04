import networkx as nx  
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd 
from scipy.spatial import distance

def lecturaArchivo(ar):
    archivo = pd.read_csv(ar, sep=';', names=["T", "N", "X,Y"])
    archivo['X,Y']=archivo['X,Y'].str.split(',')
    print(archivo)
    return archivo

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

def ordenarCentros(dic):
  dato = []
  Centros = {}
  for key in dic:
    dato = dic[key]
    Centros[key] = dato[0]
  return Centros

def ordenarPuntos(dic):
  dato = dic.values()
  dato = list(dato)
  Puntos = {}
  for key in dato:
    key2 = key[0]
    key3 = key[1]
    for i in range(0,len(key2)):
      Puntos[key2[i]]= key3[i]
  return Puntos

def distancia_de_lista(venta_original):##Entra una lista en forma [('nodo1',x,y),('nodo2',x,y)]
    lista = []
    for i in venta_original:  #Recorre la lista
        for j in venta_original:  #Recorre la lista
            if (i[0] != j[0]):  # Identifica que sean distintos nodos
              axis = (i[1], i[2])   # X, Y de nodo1
              axis_2 = (j[1], j[2])  # X, Y de nodo2
              distancia = round(distance.euclidean(axis,axis_2),5) #Calcula la distancia del nodo1 al nodo2
              lista.append( ( i[0], j[0], distancia ) ) #guarda en la lista en forma [(nodo1, nodo2, distancia)]
    return lista # Retorna [(nodo1, nodo2, distancia), (nodo2, nodo1, distancia)]

def CDconCoordenadasdePV(centro_cordenda,venta_cordenda,CDPV): # centro_cordenda y venta_cordenda son listas [('nodo1',x,y),('nodo2',x,y)] y CDPV = {'1': ['79', '22', '14',... 
  GrafoCDPV = {} ##Crea un diccionario con llaves de Centros de Distribucion y contenido de todas las coordenadas de la cosa :)
  listita = []
  centro_cordenda.extend(venta_cordenda) # Se juntan ambas listas, borrar en caso de que haya una lista con todas las coordenadas 
  for i in CDPV:
    for j in centro_cordenda:
      if j[0]==i:
        listita.append(j)
      for d in CDPV[i]:
        if j[0] == d:
          listita.append(j)
    listita.append(('0', 1000,1000)) #fin de cada CD (donde se guardan los camiones) 
    GrafoCDPV[i] = listita
    listita=[]
  return GrafoCDPV

def CaminoDeNodos(CDconCoordenadasdePV_): # {'1': [('1', 0, 0), ('79', 62, 50), ('22', 23, 77),
  DicGrafos = {}
  CaminoDeNodos_ = {}
  for CD in CDconCoordenadasdePV_:
    G = nx.Graph()
    G.add_weighted_edges_from(distancia_de_lista(CDconCoordenadasdePV_[CD]))
    G.remove_edge('0',CD)
    DicGrafos[CD] = G
    mst=nx.minimum_spanning_tree(G)
    nodelist=list(mst) # make a list of the nodes
    CaminoDeNodos_[CD] = nodelist
  return CaminoDeNodos_,DicGrafos  # Dic con el camino por Grafo 


def HojasDeRuta (CaminoDeNodos,PVarticulos,CDconCoordenadasdePV):
  SumaDelCamion = 0
  MaximoDelCamion = 1000
  RutaCamion = {}
  lista_caminos = []
  Camion = 0

  for CD in CaminoDeNodos:
    RutaCamion[CD]={}
    for x in range(0,len(CaminoDeNodos[CD])-1):
      if CaminoDeNodos[CD][x] == CD:
        for P in PVarticulos:
          if P == CaminoDeNodos[CD][x+1]:
            NodoSigui = CaminoDeNodos[CD][x+1]
            lista_caminos.append(CaminoDeNodos[CD][x])
            SumaDelCamion = SumaDelCamion + int(PVarticulos[P])

      if CaminoDeNodos[CD][x] == NodoSigui:
        for P in PVarticulos:
          if MaximoDelCamion <= SumaDelCamion:
            Camion = Camion + 1
            lista_caminos.append('0')
            if lista_caminos[0] != CD: 
              lista_caminos.insert(0,CD)
            RutaCamion[CD][Camion] = lista_caminos
            lista_caminos = []
            SumaDelCamion = 0 

          if P == CaminoDeNodos[CD][x+1]:
            NodoSigui = CaminoDeNodos[CD][x+1]
            lista_caminos.append(CaminoDeNodos[CD][x])
            CaminoDeNodos[CD].remove(CaminoDeNodos[CD][x])
            SumaDelCamion = SumaDelCamion + int(PVarticulos[P])


          if CaminoDeNodos[CD][x+1] == '0':
            Camion = Camion + 1
            lista_caminos.insert(0,CD)
            lista_caminos.append(CaminoDeNodos[CD][x])
            lista_caminos.append('0')
            RutaCamion[CD][Camion] = lista_caminos
            return RutaCamion
            

def cambiar_formato(Dic_PV): # {1: ['20', '-19'], 2: ['86', '45'], 3: ['-27', '32'], 4: ['-74', '60']}
  lista = []
  for i in Dic_PV:
    lista.append((str(i),int(Dic_PV[i][0]),int(Dic_PV[i][1])))
  return lista  # [(1, '20', '-19'), (2, '86', '45'), (3, '-27', '32'), (4, '-74', '60')]