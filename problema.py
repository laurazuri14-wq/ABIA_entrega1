#Interfaz genérico para los estados del espacio de estados
from abc import abstractmethod
from abc import ABCMeta




class Estado(metaclass=ABCMeta):
    #Devuelve el Vector con la lista de Operadores aplicables sobre este Estado
    @abstractmethod
    def operadoresAplicables(self):
        pass

    #Indica si este es un estado final (solución)
    @abstractmethod
    def esFinal(self):
        pass

    @abstractmethod
    #Genera un nuevo Estado resultante de aplicar el Operador indicado
    def aplicarOperador(self,operador):
        pass




#Interfaz para encapsular operadores
class Operador(metaclass=ABCMeta):
    @abstractmethod
    def getEtiqueta(self):
        pass

    @abstractmethod
    def getCoste(self):
        pass




# Clase genérica (indepeniente de estados y algoritmos concretos) que representa un problema de búsqueda en espacio de estados.
# Está caracterizado por un Estado inicial y un método de Busqueda
class Problema:
    def __init__(self,inicial,buscador):
        self.inicial=inicial
        self.buscador=buscador



    #Aplica el método de Busqueda de este Problema concreto para resolverlo. 
    #Devuelve la lista de Operadores que permiten alcanzar un Estado final desde el Estado inicial del Problema
    def obtenerSolucion(self):
        return self.buscador.buscarSolucion(self.inicial)

