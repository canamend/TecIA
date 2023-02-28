import subprocess
import re
import random
import math

def generateRand():
    tsp = []
    while len(tsp) < 20:
        r = random.randint(0,19)
        if(r not in tsp):
            tsp.append(r)
    return tsp

def generateFile(lista):
    with open('solution.txt', 'w') as f:
        for element in lista:
            f.write(f"{str(element)}\n")

def metropolis(x, xP, temp):
    k = 100
    e = xP - x
    if(e > 0):
        rand = random.uniform(0,1)
        if( math.exp((-1*k*e)/temp) > rand):
            return True #RETORNA RANGO ENTRE 0 Y 1, SE COMPARA CON RANDOM [ EN RANGO ENTRE 0 Y 1 ] (SI EL RANDOM ES MENOR AL VALOR DEL EXPONENCIAL, BRINCA YA QUE ENTRA DENTRO DEL RANGO QUE SE VA DECREMENTANDO)
        else:
            return False
    else: 
        #Si es negativo, salta, ya que se busca un número más pequeño
        return True
    
## Cambio de pares
def opc1(lista: list, pos:int):
        lista[pos], lista[pos+1] = lista[pos+1], lista[pos]
        return lista    

############################## CAMBIO DE EXTREMOS ########################################
def opc2(lista):
        for i in range(5):
            lista[i], lista[19-i] = lista[19-i], lista[i]
        return lista
############################## CAMBIO DE CENTRO ########################################
def opc3(lista):
        for i in range(5):
            lista[5+i], lista[14-i] = lista[14-i], lista[5+i]
        return lista

############################### MEZCLA DE PRIMER Y TERCER CUARTO ##########################
def opc4(lista):
        for i in range(5):
            lista[i], lista[14-i] = lista[14-i], lista[i]
        return lista

############################### MEZCLA SEGUNDO Y CUARTO CUARTO ############################
def opc5(lista):
        for i in range(5):
            lista[5+i], lista[19-i] = lista[19-i], lista[5+i]
        return lista

############################### MEZCLA PRIMERA MITAD ############################
def opc6(lista):
    used = []
    con = 0
    while len(used) < 10:
        r = random.randint(0,9)
        if(r not in used):
            lista[con], lista[r] = lista[r], lista[con]
            used.append(r)
            con += 1
    return lista

############################### MEZCLA SEGUNDA MITAD ############################
def opc7(lista):
    used = []
    con = 5
    while len(used) < 10:
        r = random.randint(10,19)
        if(r not in used):
            lista[con], lista[r] = lista[r], lista[con]
            used.append(r)
            con += 1
    return lista

def opc8(lista, numRand):
    rand = []
    while len(rand) < numRand:
        r = random.randint(0,19)
        if(r not in rand):
            rand.append(r)
    lim = int(numRand/2)
    for i in range(lim):
        lista[rand[i]], lista[ rand[(numRand-1)-i] ] = lista[rand[(numRand-1)-i]], lista[rand[i]]
    return lista

        
        
        
def error():
	print('error')

def switch_pair(opc, lista, pos=0, numRand = 8):
    match opc:
        case 0:
                return opc1(lista, pos)
        case 1:
                return generateRand()
        case 2:
                return opc2(lista)
        case 3:
                return opc3(lista)
        case 4:
                return opc4(lista)
        case 5:
                return opc5(lista)
        case 6:
                return opc6(lista)
        case 7:
                return opc7(lista)
        case 8:
                return opc8(lista, numRand)
        case default:
            return "something"


x = generateRand()
generateFile(x)
temp = 500.0
output = subprocess.run(["my_graph1.exe"], capture_output=True, shell=True)
result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
mejor = int(result)
comb = x
for i in range(1000):
    temp = 500/(i+1)
    if(temp<1):
        #Evalúa si se acerca a aun resultado óptimo
        if(temp>0.67):
            # Ir refinando resultados cuando resultado disminuya (variar cada vez menos nodos por permutación)
            if(i%2 == 0):
                r = random.randint(1,7)
                x = switch_pair(r, comb)
            else:
                x = switch_pair(8, comb, 8)
        elif(temp>0.51):
            r = random.randint(0,2)
            match r:
                case 0:
                        x = switch_pair(6, comb)
                case 1:
                        x = switch_pair(7, comb)
                case 2:
                    x = switch_pair(8, comb, 4)
        elif(mejor > 5):
            #tomamos la función asociada a la variable y la invocamos
            r = random.randint(0,18)
            x = switch_pair(0, comb, r)
        else:
            print("Se logró")
    else:
        x = generateRand()

    generateFile(x)

    output = subprocess.run(["my_graph1.exe"], capture_output=True, shell=True)
    result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
    res = int(result)

    print(f"{i} R: {res} mejor: {mejor} Comb: {x} temp: {round(temp, 3)}")

    if(metropolis(mejor, res, temp) == True):
        mejor = res
        comb = x
    
print(f"La mejor combinación es: {comb} y su puntaje es {mejor}")