import sys
from cubo import *
from problemaRubik import *
from busqueda import *



cubo = Cubo()

print("CUBO INICIAL SIN MEZCLAR:\n" + cubo.visualizar())


#Mover frontal face
cubo.mover(cubo.F)

print("CUBO resultado del movimiento F:\n" + cubo.visualizar())

movs=int(sys.argv[1])

movsMezcla = cubo.mezclar(movs)

print("MOVIMIENTOS ALEATORIOS:",movs)
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m) + " ")
print()

print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())





#Descomentar una vez se implemente la búsqueda en anchura
#Creación de un problema
#problema = Problema(EstadoRubik(cubo), BusquedaAnchura())
#problema = Problema(EstadoRubik(cubo), BusquedaProfundidadAcotada(6)) 
#problema = Problema(EstadoRubik(cubo), BusquedaEstrella())
problema = Problema(EstadoRubik(cubo), BusquedaIDAEstrella())
opsSolucion = problema.obtenerSolucion()
for o in opsSolucion:
    print(cubo.visualizarMovimiento(o.getEtiqueta()))
    cubo.mover(o.movimiento)



print("SOLUCION:")
opsSolucion = problema.obtenerSolucion()

if opsSolucion != None:
    for o in opsSolucion:
        print(cubo.visualizarMovimiento(o.getEtiqueta()) + " ")
        cubo.mover(o.movimiento)
    print()
    print("CUBO FINAL:\n" + cubo.visualizar())
else:
    print("no se ha encontrado solución")



#problema = Problema(EstadoRubik(cubo), BusquedaAEstrellaPonderada(1.5))

