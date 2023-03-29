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
        return (validSolucion[1], validSolucion[0])

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
    for padre in population:
        listaFit.append( fitness(list(padre), lista)[0] )
    return listaFit

def zeroCount(solucion):
    return solucion.count(0)

def binTournament(listaFitness, numHijos, tamMaxPool):
    for i in range(numHijos):
        print()


n = nGen =0
numHijos = 250
tamMaxPool = 10
lista = readArray("rail507.txt")
population = genPop()
lista.pop(0)

while(nGen < 100):
    listaFitness = genListaFit(population, lista)
    #idHijos = binTournament(listaFitness, numHijos, tamMaxPool)
print(len(lista))
print(len(population))
print(population[777])

