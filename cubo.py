
from random import *

seed(76)

#Clase que encapsula una cara del cubo de Rubik.
#Cada cara tiene un color asociado (coincide con su índice en el array caras del objeto Cubo) y
# un array de 9 Casillas distribuidas en "espiral" sobre la cara
class Cara:
    def __init__(self, color):
        self.color=color
        self.casillas = []
        for i in range(0, 9):
            self.casillas.append(Casilla(color, i))


    def equal(self, cara):
        for i,c in enumerate(cara):
            if c.color != self.casillas[i].color:
                return False
        return True




#Clase que encapsula una casilla del curbo de Rubik.
#Mantiene el color de la casilla y su posición correcta final en su respectiva cara (la que corresponde a su color)
class Casilla:
    def __init__(self, color, pos):
        self.color=color
        self.posicionCorrecta=pos



    def equal(self,casilla):
        if self.color != casilla.color or self.posicionCorrecta != casilla.posicionCorrecta: return False
        return True


    
        




#Clase que encapsula un cubo de Rubik.
#Almacena la situación actual del Cubo en un array de 6 objetos Cara. Cada objeto Cara almacena
#la situación de sus casillas en un array de 9 objetos Casilla
#Incluye información (constantes y arrays estáticos) que identifica caras y colores y la vecindad entre caras y casillas.
class Cubo:
    """

    Reparto de las caras
       0
     1 2 3 4
       5
    
    Indices de las casillas en cada cara
           012
           783
           654
     
      012  012  012  012
      783  783  783  783
      654  654  654  654
    
           012
           783    
           654
    
    

    """

    #Constantes para identificar las caras
    UP = 0
    LEFT = 1
    FRONT = 2
    RIGHT = 3
    BACK = 4
    DOWN = 5

    #lista para identificar colores
    ids_colores = [0, 1, 2, 3, 4, 5]

    #lista de etiquetas para identificar los colores
    etq_colores = ["W", "B", "O", "G", "R", "Y"]

    #Indices de la cara vecina Norte de cada una de las caras
    vecinoNorte = [4, 0, 0, 0, 0, 2]

    #Indices de la cara vecina Este de cada una de las caras
    vecinoEste  = [3, 2, 3, 4, 1, 3]

    #Indices de la cara vecina Sur de cada una de las caras
    vecinoSur   = [2, 5, 5, 5, 5, 4]

    #Indices de la cara vecina Oeste de cada una de las caras
    vecinoOeste = [1, 4, 1, 2, 3, 1]

    #Indices de las casillas fronterizas en las caras vecinas Norte, Este, Sur, Oeste 
    #  a mover en el giro normal (sentido del reloj visto de frente)
    idxNorte = [[2, 1, 0],  # casillas fronterizas al Norte para cara 0
                [0, 7, 6],  # idem cara 1
                [6, 5, 4],  # idem cara 2
                [4, 3, 2],  # idem cara 3
                [2, 1, 0],  # idem cara 4
                [6, 5, 4]]; # idem cara 5

    #Indices de las casillas fronterizas en la cara  vecina Este
    #  a mover en el giro normal (sentido del reloj visto de frente) 
    idxEste = [[2, 1, 0],  # casillas fronterizas al Este para cara 0
               [0, 7, 6],  # idem cara 1
               [0, 7, 6],  # idem cara 2
               [0, 7, 6],  # idem cara 3
               [0, 7, 6],  # idem cara 4
               [6, 5, 4]]; # idem cara 5


    #Indices de las casillas fronterizas en la cara vecina Sur
    #  a mover en el giro normal (sentido del reloj visto de frente)
    idxSur = [[2, 1, 0],  # casillas fronterizas al Sur para cara 0
              [0, 7, 6],  # idem cara 1
              [2, 1, 0],  # idem cara 2
              [4, 3, 2],  # idem cara 3
              [6, 5, 4],  # idem cara 4
              [6, 5, 4]]; # idem cara 5





    #Indices de las casillas fronterizas en las cara vecina Oeste 
    # a mover en el giro normal (sentido del reloj visto de frente)
    idxOeste = [[2, 1, 0],  # casillas fronterizas al Oeste para cara 0
                [4, 3, 2],  # idem cara 1
                [4, 3, 2],  # idem cara 2
                [4, 3, 2],  # idem cara 3
                [4, 3, 2],  # idem cara 4
                [6, 5, 4]]; # idem cara 5




    #Movimientos posibles
    U = UP;
    Ui = U + 6;
    L = LEFT;
    Li = L + 6;
    F = FRONT;
    Fi = F + 6;
    R = RIGHT;
    Ri = R + 6;
    B = BACK;
    Bi = B + 6;
    D = DOWN;
    Di = D + 6;

    movimientosPosibles = [U, Ui, L, Li, F, Fi, R, Ri, B, Bi, D, Di]


    #Etiquetas abreviadas que identifican cada uno de los movimientos (U, Ui, L, Li, ...)
    etq_corta = ["U", "L", "F", "R", "B", "D","Ui", "Li", "Fi", "Ri", "Bi", "Di"]



    #Lista con las 6 caras del cubo
    def __init__(self):
        self.caras=[]
        for i in range(0, 6):
            self.caras.append(Cara(i))


    #Clonación de objetos cubo
    def clonar(self):
        c=Cubo()
        for i in range(0,6):
            c.caras[i].color=self.caras[i].color
            for j in range(0,9): 
                c.caras[i].casillas[j].color=self.caras[i].casillas[j].color
        return c

    #Comprueba si las caras del cubo contienen una configuración final
    def esConfiguracionFinal(self):
        for c in self.caras:
            for n in c.casillas:
                if n.color != c.color:
                    return False
        return True

    

    #Realiza una mezcla aleatoria de las caras del cubo aplicando un número aleatorio de movientos al azar 
    def mezclar(self):
        return self.mezclar(randint(0, 30))


    #Realiza una mezcla aleatoria de las caras del cubo aplicando el num. indicado de movimientos al azar
    def mezclar(self,pasos):
        listaMovs=[]
        #print(self.movimientosPosibles)
        for i in range(0, pasos):
            
            idMov = randint(0,len(self.movimientosPosibles)-1)
            self.mover(self.movimientosPosibles[idMov])
            listaMovs.append(self.movimientosPosibles[idMov])
        #print(listaMovs)
        return listaMovs


    #Realiza el moviminnto indicado sobre la correspondiente cara del cubo
    def mover(self,mov):
        if mov < 6:
            self.girarHorario(mov)
        else:
            self.girarAntiHorario(mov-6)


    #Realiza una lista de movimientos sobre las caras del cubo
    def moverListaMovs(sefl,listaMovs):
        for mov in listaMovs:
            self.mover(mov)



    #Giro horario sobre la cara indicada y las casillas fronterizas de las 
    # caras vecinas que correspondan
    def girarHorario(self,idxCara):
        aux1 = None
        aux2 = None
        aux3 = None
        self.girarCaraHorario(self.caras[idxCara])
        for i in range(0,3):
            # Norte -> Este
            aux1 = self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]]
            self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]] = self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]]

            # Este -> Sur
            aux2 = self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]]
            self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]] = aux1

            # Sur -> Oeste
            aux3 = self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]]
            self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]] = aux2

            # Oeste -> Norte
            self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]] = aux3



    #Giro horario sobre la cara indicada y las casillas fronterizas de las 
    # caras vecinas que correspondan
    def girarAntiHorario(self,idxCara):
        aux1 = None
        aux2 = None
        aux3 = None
        self.girarCaraAntiHorario(self.caras[idxCara])
        for i in range(0,3):
            # Norte -> Oeste
            aux1 = self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]]
            self.caras[self.vecinoOeste[idxCara]].casillas[self.idxOeste[idxCara][i]] = self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]]

            # Oeste -> Sur
            aux2 = self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]]
            self.caras[self.vecinoSur[idxCara]].casillas[self.idxSur[idxCara][i]] = aux1

            # Sur -> Este
            aux3 = self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]]
            self.caras[self.vecinoEste[idxCara]].casillas[self.idxEste[idxCara][i]] = aux2

            # Este -> Norte
            self.caras[self.vecinoNorte[idxCara]].casillas[self.idxNorte[idxCara][i]] = aux3;



    #Giro horario sobre las casillas de una cara (no afecta a las caras vecinas)
    def girarCaraHorario(self,cara):
        copia = []
        for c in cara.casillas:
            copia.append(c)

        #La casilla num. 8 no se mueve
        for i in range(0,8):
            cara.casillas[(i+2)%8]=copia[i]


    #Giro antihorario sobre las casillas de una cara (no afecta a las caras vecinas)
    def girarCaraAntiHorario(self,cara):
        copia = []
        for c in cara.casillas:
            copia.append(c)

        #La casilla num. 8 no se mueve
        for i in range(0,8):
            cara.casillas[i]=copia[(i+2)%8]


    #Comparar 2 cubos
    def equals(self,cubo):
        for i in range(0,6):
            if not self.caras[i].equals(cubo.caras[i]):
                return False
        return True


    #Visualizar cubo
    def visualizar(self):
        # Cara 0
        resultado = "    " + self.stringFila1(self.caras[0]) + "\n" +"    " + self.stringFila2(self.caras[0]) + "\n" +"    " + self.stringFila3(self.caras[0]) + "\n\n"

        # Caras 1, 2, 3, 4
        resultado += self.stringFila1(self.caras[1]) + " " + self.stringFila1(self.caras[2]) + " " + self.stringFila1(self.caras[3]) + " " + self.stringFila1(self.caras[4]) + "\n" + self.stringFila2(self.caras[1]) + " " + self.stringFila2(self.caras[2]) + " " +self.stringFila2(self.caras[3]) + " " + self.stringFila2(self.caras[4]) + "\n" +self.stringFila3(self.caras[1]) + " " + self.stringFila3(self.caras[2]) + " " +self.stringFila3(self.caras[3]) + " " + self.stringFila3(self.caras[4]) + "\n\n"

        # Cara 5
        resultado += "    " + self.stringFila1(self.caras[5]) + "\n" + "    " + self.stringFila2(self.caras[5]) + "\n" + "    " + self.stringFila3(self.caras[5]) + "\n\n"
        return resultado

    def  stringFila1(self,cara):
        return self.etq_colores[cara.casillas[0].color] + self.etq_colores[cara.casillas[1].color] + self.etq_colores[cara.casillas[2].color]


    def  stringFila2(self,cara):
        return self.etq_colores[cara.casillas[7].color] + self.etq_colores[cara.casillas[8].color] + self.etq_colores[cara.casillas[3].color]

    def  stringFila3(self,cara):
        return self.etq_colores[cara.casillas[6].color] + self.etq_colores[cara.casillas[5].color] + self.etq_colores[cara.casillas[4].color]



    def visualizarMovimiento(self,tipo):
        return self.etq_corta[tipo]








