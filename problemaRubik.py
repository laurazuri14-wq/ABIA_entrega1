


from problema import *
from cubo import *


# Objeto que implementa la interfaz Estado para un cubo Rubik concreto.
# La mayor parte de los métodos definidos en el interfaz Estado se delegan en el objeto Cubo.

class EstadoRubik(Estado):

    def __init__(self, cubo):
        
        self.listaOperadoresAplicables=[]
        for m in Cubo.movimientosPosibles:
            self.listaOperadoresAplicables.append(OperadorRubik(m))

        self.cubo=cubo


    def operadoresAplicables(self):
        return self.listaOperadoresAplicables


    def esFinal(self):
        return self.cubo.esConfiguracionFinal()

    def aplicarOperador(self,o):
        nuevo=self.cubo.clonar()
        nuevo.mover(o.movimiento)
        return EstadoRubik(nuevo)


    def equals(self,e):
        return self.cubo.equals(e.cubo)


# Implementa el interfaz Operador encapsulando un movimiento (giro) Rubik
class OperadorRubik(Operador):
    def __init__(self, mov):
        self.movimiento=mov

    def getEtiqueta(self):
        return self.movimiento

    #El coste de los giros es siempre 1 (para la búsqueda todos son idénticos)
    def getCoste(self):
        return 1
