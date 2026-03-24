import sys
from cubo import *
from problemaRubik import *
from busqueda import *
import time
import random
random.seed(67)



cubo = Cubo()

print("CUBO INICIAL SIN MEZCLAR:\n" + cubo.visualizar())


#Mover frontal face
cubo.mover(cubo.F)

print("CUBO resultado del movimiento F:\n" + cubo.visualizar())

cubo = Cubo()   # reiniciar antes de mezclar(busqueda IDA)

#  AQUÍ VA EL CAMBIO
movsMezcla = [cubo.Ui, cubo.Ui, cubo.R]

for m in movsMezcla:
    cubo.mover(m)

# esto se queda igual
print("MOVIMIENTOS DE MEZCLA:")
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m))

print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())

"""
movs=int(sys.argv[1])

movsMezcla = cubo.mezclar(movs)

print("MOVIMIENTOS ALEATORIOS:",movs)
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m) + " ")
print()

print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())
"""





#Descomentar una vez se implemente la búsqueda en anchura
#Creación de un problema
#problema = Problema(EstadoRubik(cubo), BusquedaAnchura())
#problema = Problema(EstadoRubik(cubo), BusquedaProfundidadAcotada(6))
#problema = Problema(EstadoRubik(cubo), BusquedaProfundidadIterativa())
#problema = Problema(EstadoRubik(cubo), BusquedaVoraz())
#problema = Problema(EstadoRubik(cubo), BusquedaEstrella())
#problema = Problema(EstadoRubik(cubo), BusquedaIDAEstrella())
problema = Problema(EstadoRubik(cubo), BusquedaAEstrellaPonderada())



print("SOLUCION:")
inicio = time.time()

opsSolucion = problema.obtenerSolucion()

fin = time.time()

tiempo = fin - inicio
print("TIEMPO DE BUSQUEDA:", tiempo, "segundos")

if opsSolucion != None:
    for o in opsSolucion:
        print(cubo.visualizarMovimiento(o.getEtiqueta()) + " ")
        cubo.mover(o.movimiento)
    print()
    print("CUBO FINAL:\n" + cubo.visualizar())
else:
    print("no se ha encontrado solución")




