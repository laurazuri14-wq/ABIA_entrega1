from nodos import *


from abc import abstractmethod
from abc import ABCMeta
print("ESTOY EN EL BUSQUEDA CORRECTO")


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
        
        self.nodos_explorados = 0
        self.tam_abiertos_max = 0
        self.suma_abiertos = 0
        self.iteraciones = 0

        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            self.nodos_explorados += 1
            self.suma_abiertos += len(abiertos)
            self.iteraciones += 1

            if len(abiertos) > self.tam_abiertos_max:
                self.tam_abiertos_max = len(abiertos)

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

        if self.iteraciones > 0:
            self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
        else:
            self.tam_abiertos_medio = 0

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:   # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        

class BusquedaProfundidadAcotada(Busqueda):
    def __init__(self, cota=6):
        self.cota = cota

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()

        self.nodos_explorados = 0
        self.tam_abiertos_max = 0
        self.suma_abiertos = 0
        self.iteraciones = 0

        abiertos.append(NodoProfundidad(inicial, None, None, 0))
        cerrados[inicial.cubo.visualizar()] = inicial

        while not solucion and len(abiertos) > 0:
            self.nodos_explorados += 1
            self.suma_abiertos += len(abiertos)
            self.iteraciones += 1

            if len(abiertos) > self.tam_abiertos_max:
                self.tam_abiertos_max = len(abiertos)

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

        if self.iteraciones > 0:
            self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
        else:
            self.tam_abiertos_medio = 0

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

        self.nodos_explorados = 0
        self.tam_abiertos_max = 0
        self.suma_abiertos = 0
        self.iteraciones = 0

        for cota in range(self.cota_inicial, self.cota_max + 1):

            buscador = BusquedaProfundidadAcotada(cota)
            solucion = buscador.buscarSolucion(inicial)

            # 🔹 MÉTRICAS
            self.nodos_explorados += buscador.nodos_explorados
            self.suma_abiertos += buscador.suma_abiertos
            self.iteraciones += buscador.iteraciones

            if buscador.tam_abiertos_max > self.tam_abiertos_max:
                self.tam_abiertos_max = buscador.tam_abiertos_max

            if solucion != None:
                if self.iteraciones > 0:
                    self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
                else:
                    self.tam_abiertos_medio = 0

                return solucion

        if self.iteraciones > 0:
            self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
        else:
            self.tam_abiertos_medio = 0

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

        self.nodos_explorados = 0
        self.tam_abiertos_max = 0
        self.suma_abiertos = 0
        self.iteraciones = 0

        abiertos.append(NodoVoraz(inicial, None, None, self.heuristica(inicial)))

        while not solucion and len(abiertos) > 0:
            self.nodos_explorados += 1
            self.suma_abiertos += len(abiertos)
            self.iteraciones += 1

            if len(abiertos) > self.tam_abiertos_max:
                self.tam_abiertos_max = len(abiertos)

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
                                break

                        if not repetido:
                            abiertos.append(
                                NodoVoraz(hijo, nodoActual, operador, self.heuristica(hijo))
                            )

        if self.iteraciones > 0:
            self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
        else:
            self.tam_abiertos_medio = 0

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

        # métricas
        self.nodos_explorados = 0
        self.tam_abiertos_max = 0
        self.suma_abiertos = 0
        self.iteraciones = 0

        nodoInicial = NodoEstrella(inicial, None, None, 0, inicial.heuristica())
        abiertos.append(nodoInicial)

        while not solucion and len(abiertos) > 0:

            # métricas
            self.nodos_explorados += 1
            self.suma_abiertos += len(abiertos)
            self.iteraciones += 1

            if len(abiertos) > self.tam_abiertos_max:
                self.tam_abiertos_max = len(abiertos)

            # ordenar por f (más pequeño primero)
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

                    # comprobar si está en abiertos
                    repetido = False
                    for n in abiertos:
                        if n.estado.cubo.visualizar() == clave:
                            repetido = True
                            break

                    # si no está ni en abiertos ni en cerrados → añadir
                    if not repetido and clave not in cerrados:
                        abiertos.append(sucesor)

        # calcular media
        if self.iteraciones > 0:
            self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
        else:
            self.tam_abiertos_medio = 0

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None


class BusquedaIDAEstrella(Busqueda):

    def buscarSolucion(self, inicial):
        cota = inicial.heuristica()

        # métricas
        self.nodos_explorados = 0
        self.tam_abiertos_max = 0
        self.suma_abiertos = 0
        self.iteraciones = 0

        while True:
            resultado = self._dfs(inicial, 0, cota, 1)

            if isinstance(resultado, list):
                if self.iteraciones > 0:
                    self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
                else:
                    self.tam_abiertos_medio = 0
                return resultado

            if resultado == float('inf'):
                if self.iteraciones > 0:
                    self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
                else:
                    self.tam_abiertos_medio = 0
                return None

            cota = resultado

    def _dfs(self, estado, g, cota, tam_abiertos):
        # métricas
        self.nodos_explorados += 1
        self.suma_abiertos += tam_abiertos
        self.iteraciones += 1

        if tam_abiertos > self.tam_abiertos_max:
            self.tam_abiertos_max = tam_abiertos

        f = g + estado.heuristica()

        if f > cota:
            return f

        if estado.esFinal():
            return []

        minimo = float('inf')

        for operador in estado.operadoresAplicables():
            hijo = estado.aplicarOperador(operador)

            resultado = self._dfs(hijo, g + 1, cota, tam_abiertos + 1)

            if isinstance(resultado, list):
                return [operador] + resultado

            if resultado < minimo:
                minimo = resultado

        return minimo
  
class BusquedaAEstrellaPonderada(Busqueda):

    def __init__(self, w=1.5):
        self.w = w

    def buscarSolucion(self, inicial):
        solucion = False
        abiertos = []
        cerrados = dict()
        nodoActual = None

        # métricas
        self.nodos_explorados = 0
        self.tam_abiertos_max = 0
        self.suma_abiertos = 0
        self.iteraciones = 0

        nodoInicial = NodoEstrella(
            inicial,
            None,
            None,
            0,
            inicial.heuristica()
        )

        nodoInicial.f = nodoInicial.g + self.w * nodoInicial.h
        abiertos.append(nodoInicial)

        while not solucion and len(abiertos) > 0:

            # métricas
            self.nodos_explorados += 1
            self.suma_abiertos += len(abiertos)
            self.iteraciones += 1

            if len(abiertos) > self.tam_abiertos_max:
                self.tam_abiertos_max = len(abiertos)

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

                    sucesor = NodoEstrella(
                        hijo,
                        nodoActual,
                        operador,
                        g_hijo,
                        h_hijo
                    )

                    sucesor.f = g_hijo + self.w * h_hijo

                    # evitar repetidos (versión simple)
                    repetido = False
                    for n in abiertos:
                        if n.estado.cubo.visualizar() == clave:
                            repetido = True
                            break

                    if not repetido and clave not in cerrados:
                        abiertos.append(sucesor)

        # calcular media
        if self.iteraciones > 0:
            self.tam_abiertos_medio = self.suma_abiertos / self.iteraciones
        else:
            self.tam_abiertos_medio = 0

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        