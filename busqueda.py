from nodos import *


from abc import abstractmethod
from abc import ABCMeta


#Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass



#Implementa una búsqueda en Anchura genérica (independiente de Estados y Operadores) controlando repetición de estados.
#Usa lista ABIERTOS (lista) y lista CERRADOS (diccionario usando Estado como clave)
class BusquedaAnchura(Busqueda):
    
    #Implementa la búsqueda en anchura. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoAnchura
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False #prueba
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop(0) #tarea 1
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                #cerrados[actual.cubo.visualizar()] = actual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS 
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        

class BusquedaProfundidadAcotada(Busqueda):
    def __init__(self, cota = 6):
        self.cota = cota
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoProfundidad(inicial, None, None, 0))
        cerrados[inicial.cubo.visualizar()] = inicial
        
        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado

            if actual.esFinal():
                solucion = True
            else:
                if nodoActual.profundidad < self.cota:
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        if hijo.cubo.visualizar() not in cerrados.keys():
                            abiertos.append(
                                NodoProfundidad(
                                    hijo,
                                    nodoActual,
                                    operador,
                                    nodoActual.profundidad + 1
                                )
                            )
                            cerrados[hijo.cubo.visualizar()] = hijo


        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class BusquedaProfundidadIterativa(Busqueda):
    def __init__(self, cota_inicial=0, cota_max=20):
        self.cota_inicial = cota_inicial
        self.cota_max = cota_max

    def buscarSolucion(self, inicial):
        for cota in range(self.cota_inicial, self.cota_max + 1):
            busqueda_acotada = BusquedaProfundidadAcotada(cota)
            solucion = busqueda_acotada.buscarSolucion(inicial)
            if solucion is not None:
                return solucion
        return None
    
    class BusquedaVoraz(Busqueda):

        def heuristica(self, estado):
            mal_colocadas = 0
            for cara in estado.cubo.caras:
                for casilla in cara.casillas:
                    if casilla.color != cara.color:
                        mal_colocadas += 1
            return mal_colocadas

        def buscarSolucion(self, inicial):
            nodoActual = None
            actual, hijo = None, None
            solucion = False
            abiertos = []
            cerrados = dict()

            abiertos.append(NodoVoraz(inicial, None, None, self.heuristica(inicial)))

            while not solucion and len(abiertos) > 0:
                abiertos.sort(key=lambda nodo: nodo.heuristica)
                nodoActual = abiertos.pop(0)
                actual = nodoActual.estado

                if actual.esFinal():
                    solucion = True
                else:
                    cerrados[actual.cubo.visualizar()] = actual

                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)

                        if hijo.cubo.visualizar() not in cerrados:
                            repetido = False
                            for nodo in abiertos:
                                if nodo.estado.cubo.visualizar() == hijo.cubo.visualizar():
                                    repetido = True

                            if not repetido:
                                abiertos.append(NodoVoraz(hijo, nodoActual, operador, self.heuristica(hijo)))

            if solucion:
                lista = []
                nodo = nodoActual
                while nodo.padre != None:
                    lista.insert(0, nodo.operador)
                    nodo = nodo.padre
                return lista
            else:
                return None
            
class BusquedaEstrella(Busqueda):

    def buscarSolucion(self, inicial):
        solucion = False
        abiertos = []
        cerrados = dict()
        nodoActual = None

        nodoInicial = NodoEstrella(inicial, None, None, 0, inicial.heuristica())
        abiertos.append(nodoInicial)

        while not solucion and len(abiertos) > 0:
            abiertos.sort(key=lambda n: n.f)
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado

            if actual.esFinal():
                solucion = True
            else:
                cerrados[actual.cubo.visualizar()] = nodoActual

                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    clave = hijo.cubo.visualizar()

                    g_hijo = nodoActual.g + 1
                    h_hijo = hijo.heuristica()
                    sucesor = NodoEstrella(hijo, nodoActual, operador, g_hijo, h_hijo)

                    nodo_en_abiertos = None
                    for n in abiertos:
                        if n.estado.cubo.visualizar() == clave:
                            nodo_en_abiertos = n
                            break

                    if nodo_en_abiertos is not None:
                        if sucesor.g < nodo_en_abiertos.g:
                            # actualizar nodo en abiertos
                            ...
                    elif clave in cerrados:
                        if sucesor.g < cerrados[clave].g:
                            # reabrir nodo
                            ...
                    else:
                        abiertos.append(sucesor)

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None