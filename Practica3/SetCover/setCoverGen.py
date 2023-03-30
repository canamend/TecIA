import re
import random
import numpy as np
# def fitness():
    
#Se genera un arreglo de arreglos, donde cada instancia es un arreglo que contiene todos los números de cada línea del archivo
def readArray(archivo: str):
    f = open(archivo, 'r')
    lista = []
    for line in f:
        lista.append((re.sub(r'[^0-9]', ' ', line)).strip().split())
    return lista

def genPop():
    pob = [] 
    binArray = []
    n = nPop = 0
    while(nPop < 1000):
        binArray = np.random.randint(0,2,63009)
        pob.append(binArray)
        nPop += 1
    return pob

def fitness(solucion, lista):
    i = j = 0
    #lleva el registro de valores de 1 al 507
    con = 1
    fitness = solucion.count(1)
    valid = isValid(solucion, lista)
    if(valid[0] == True):
    #Si no es una solución valida definir un módulo que la convierta en una solución válida
        return (fitness, solucion)
    else:
        ban = random.randint(0,1)
        if(ban == 1):
            aux = True
        else:
            aux = False
        validSolucion = turnValid(solucion, aux, valid[1], lista, fitness)
        return (validSolucion[1], validSolucion[0]) #Retorna el valor de fitness pos[1] y el arreglo de 0s y 1s pos[0]

def isValid(solucion, lista):
    i = 0
    numeros = []
    ban = False
    while(i < len(solucion) and ban == False):
        if(solucion[i] == 1):
            for element in lista[i]:
                if(element not in numeros):
                    numeros.append(element)
                    if(len(numeros) >= 507):
                        ban = True
        i += 1
    if(len(numeros) >= 507):
        return (True, numeros)
    else: 
        return (False, numeros)
    
def turnValid(solucion, ban, numeros, lista, fitness):
    banAux = False
    if(ban == True):
        i = 0
        while(i < len(solucion) and banAux == False):
            if(solucion[i] == 0):
                for element in lista[i]:
                    if(element not in numeros):
                        numeros.append(element)
                        solucion[i] = 1
                        fitness += 1
                        if(len(numeros) >= 507):
                            banAux = True
            i += 1
        if(len(numeros) >= 507):
            return (solucion, fitness)
        else:
            return (solucion, fitness)
    else:
        i = len(solucion) - 1
        while(i >= 0 and banAux == False):
            if(solucion[i] == 0):
                for element in lista[i]:
                    if(element not in numeros):
                        numeros.append(element)
                        solucion[i] = 1
                        fitness += 1
                        if(len(numeros) >= 507):
                            banAux = True
            i -= 1
        if(len(numeros) >= 507):
            return (solucion, fitness)
        else:
            return (solucion, fitness)
        
def genListaFit(population, lista):
    listaFit = []
    arreglosBin = []
    i = 0
    for padre in population:
        elemento = fitness(list(padre), lista)
        listaFit.append( elemento[1] )
        arreglosBin.append( elemento[0] )
        i += 1
    return [listaFit, arreglosBin]

def zeroCount(solucion):
    return solucion.count(0)

def genPadres(listaFitness, numHijos, tamMaxPool):
    padres = []
    for i in range(numHijos):
        ban = ban1 = False
        while(ban == False or ban1 == False):
            if(ban == False):
                n1 = random.randint(2, tamMaxPool)
                if(n1 % 2 == 0):
                    ban = True
            if(ban1 == False):
                n2 = random.randint(2, tamMaxPool)
                if(n2 % 2 == 0):
                    ban1 = True

        pool1 = getElements(n1, listaFitness)
        pool2 = getElements(n2, listaFitness)

        winner = binTournament(pool1, pool2)
        padres.append(winner)
    return padres

def getElements(poolSize, listaFitness):
    pool = []
    positions = []
    i = 0
    while(i < poolSize):
        r = random.randint(0, len(listaFitness)-1)
        pool.append(listaFitness[r])
        positions.append(r)
        i += 1
    return [positions, pool]

def binTournament(pool1, pool2):
    min1, min2 = min(pool1[1]), min(pool2[1])
    pos1, pos2 = pool1[0][pool1[1].index(min1)], pool2[0][pool2[1].index(min2)]
    if(min1 < min2):
        return [pos1, min1]
    else:
        return [pos2, min2]

def getHijos(idPadres, listaFitness, crossoverPoint):
    hijos =[]
    hijosTuple = []
    con = len(idPadres) - 1
    while(con > 0):
        hijosTuple.append(crossover( listaFitness[0][ idPadres[con] ], listaFitness[0][ idPadres[con-1] ], crossoverPoint))
        con -= 2
    for tupla in hijosTuple:
        for elemento in tupla:
            if(len(elemento)>63009):
                elemento.pop()
            hijos.append(elemento)
    return genListaFit(hijos, lista)


def crossover(elemento1, elemento2, crossoverPoint):
    child1 = child2 = []
    i = 0
    tam = len(elemento1)
    while(len(child1) < 63009 and len(child2) < 63009 ):
        if(i < crossoverPoint):
            child1.append(elemento2[i])
            child2.append(elemento1[i])
        else:
            if(i < tam - crossoverPoint):
                child1.append(elemento1[i])
                child2.append(elemento2[i])
            else:
                child1.append(elemento2[i])
                child2.append(elemento1[i])
        i += 1
    return [child1, child2]

def mutacion(hijos):
    umbral = .30
    for hijo in hijos:
        if(random.random() < umbral):
            r = random.randint(10, 100)
            for i in range(r):
                ban = False
                while(ban == False):
                    pos = random.randint(0, 63009)
                    if(hijo[pos] == 1):
                        hijo[pos] == 0
                        ban = True       
    return hijos

def replacement(poblacion, hijos):
    i = 0
    while(i<len(hijos)):
        index = poblacion[1].index( max(poblacion[1] ))
        poblacion[0][index], poblacion[1][index] = hijos[0][i], hijos[1][i]
        i+=1
    print(f"El mejor valor de esta generación es: {min(poblacion[1])}")
    return poblacion[0]


n = nGen = 0
numHijos = 250
tamMaxPool = 20
crossoverPoint = 21003
lista = readArray("rail507.txt")
population = genPop()
lista.pop(0)

while(nGen < 100):
    listaFitness = genListaFit(population, lista)
    listOnlyFitVal = listaFitness[1] #Aqui se evita enviar el arreglo de 1s y 0s
    idPadres = genPadres(listOnlyFitVal, numHijos, tamMaxPool)
    idPadres = np.array(idPadres)
    listaFitnessHijos = getHijos(idPadres[:,0], listaFitness, crossoverPoint)
    listaFitnessHijos = genListaFit(mutacion(listaFitnessHijos[0]), lista)
    population = replacement(listaFitness, listaFitnessHijos)
    nGen += 1

