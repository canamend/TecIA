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
    while(nPop < 10):
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
            # print("AHORA ES VÁLIDA")
            # print(numeros)
            return (solucion, fitness)
        else:
            print("Fue imposible hacerla válida")
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
            # print("AHORA ES VÁLIDA")
            # print(numeros)
            return (solucion, fitness)
        else:
            print("Fue imposible hacerla válida")
            return (solucion, fitness)
        
def genListaFit(population, lista):
    listaFit = []
    arreglosBin = []
    i = 0
    for padre in population:
        elemento = fitness(list(padre), lista)
        listaFit.append( elemento[1] )
        arreglosBin.append( elemento[0] )
        print(f"Se crea el elemento numero {i} del arreglo de fitness")
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
    # print(f"Los candidatos son:\nPrimer pool: {pool1}\nSegundo pool: {pool2}")
    print()

n = nGen =0
numHijos = 250
tamMaxPool = 20
lista = readArray("rail507.txt")
population = genPop()
lista.pop(0)

while(nGen < 100):
    listaFitness = genListaFit(population, lista)
    listOnlyFitVal = listaFitness[0] #Aqui se evita enviar el arreglo de 1s y 0s
    print(type(listOnlyFitVal))
    print(listOnlyFitVal)
    print("Se ha creado la lista de fitness")
    idPadres = genPadres(listOnlyFitVal, numHijos, tamMaxPool)
    nGen += 1
print(len(lista))
print(len(population))
print(population[777])

