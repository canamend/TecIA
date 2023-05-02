import random

def generateRand():
    tsp = []
    while len(tsp) < 10:
        r = random.randint(0,9)
        if(r not in tsp):
            tsp.append(r)
    return tsp

def merge1(lista1, lista2):
    merge = []
    b = False
    for i in range(10):
        if(lista1[i] == lista2[i]):
            merge.append(lista1[i])
        elif(lista1[i] not in merge and b == False):
            merge.append(lista1[i])
            b = True
        elif(lista2[i] not in merge and b == True):
            merge.append(lista2[i])
            b = False

    for i in range(10):
        if(i not in merge):
            merge.append(i)

    return merge

lista1, lista2 = generateRand(), generateRand()
merge = merge1(lista1, lista2)
print(f"Lista 1: {lista1}\nLista 2: {lista2}\nLista n: {merge}")        
        

