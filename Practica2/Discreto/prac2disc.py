import subprocess
import re
import random
import math

##MEJOR RESULTADO 137
def opc1(lista: list, pos:int):
        lista[pos], lista[pos+1] = lista[pos+1], lista[pos]
        return lista    

############################## CAMBIO DE EXTREMOS ########################################
def opc2(lista):
        lista[0], lista[19], lista[1], lista[18] = lista[19], lista[0], lista[18], lista[1]
        return lista
############################## CAMBIO DE CENTRO/EXTERNO ########################################
def opc3(lista):
        lista[2], lista[3], lista[16], lista[17] = lista[17], lista[16], lista[3], lista[2]
        return lista

############################### MEZCLA DE PRIMER Y TERCER CUARTO ##########################
def opc4(lista):
        lista[0], lista[1], lista[14], lista[15] = lista[14], lista[15], lista[0], lista[1]
        return lista

############################### MEZCLA SEGUNDO Y CUARTO CUARTO ############################
def opc5(lista):
        lista[2], lista[3], lista[16], lista[17] = lista[16], lista[17], lista[2], lista[3]
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

def error():
	print('error')

def switch_pair(opc, lista, pos=0):
    match opc:
        case 0:
                return opc1(lista, pos)
        case 1:
                aux = random.randint(0,1)
                if(aux == 0):
                    return swapHalf(lista, True)
                else:
                    return swapHalf(lista, False)
        case 2:
                return generateRand()
        case 3:
                return opc2(lista)
        case 4:
                return opc3(lista)
        case 5:
                return opc4(lista)
        case 6:
                return opc5(lista)
        case 7:
                return opc6(lista)
        case 8:
                return opc7(lista)
        case default:
            return "something"

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
    k = 1
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

def swapHalf(lista, flag):
    #Cambia la primera mitad
    if (flag == True):
        used = []
        con = 0
        while len(used) < 4:
            r = random.randint(0,3)
            if(r not in used):
                lista[con], lista[r] = lista[r], lista[con]
                used.append(r)
                con += 1
    #Cambia la segunda mitad
    else:
        used = []
        con = 4
        while len(used) < 4:
            r = random.randint(4,7)
            if(r not in used):
                lista[con], lista[r] = lista[r], lista[con]
                used.append(r)
                con += 1
    return lista


x = generateRand()
generateFile(x)
temp = 500.0
output = subprocess.run(["my_graph1.exe"], capture_output=True, shell=True)
result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
mejor = int(result)
comb = x
for i in range(1000):
    temp = 500/(i+1)
    if(temp<2):
        #Evalúa si se acerca a aun resultado óptimo
        if(mejor > 150 and i < 600):
            # Ir refinando resultados cuando resultado disminuya (variar cada vez menos nodos por permutación)
            r = random.randint(3,8)
            x = switch_pair(r, comb)
        elif(mejor > 50 and i < 930):
            if(i % 2 == 0):
                x = switch_pair(7, comb)
            else:
                x = switch_pair(8, comb)
        elif(mejor > 5):
            #tomamos la función asociada a la variable y la invocamos
            r = random.randint(0,8)
            x = switch_pair(0, comb, r)
        else:
            print("Se logró")
            #tomamos la función asociada a la variable y la invocamos
            #swap_pairs.get(opc, error)()
    else:
        x = generateRand()

    generateFile(x)

    output = subprocess.run(["my_graph1.exe"], capture_output=True, shell=True)
    result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
    res = int(result)

    print(f"Iteración actual: {i} resultado: {res} mejor: {mejor} combinación: {x} temp: {round(temp, 3)}")

    if(metropolis(mejor, res, temp) == True):
        mejor = res
        comb = x
    
print(f"La mejor combinación es: {comb} y su puntaje es {mejor}")