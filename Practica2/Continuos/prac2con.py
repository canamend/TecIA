import subprocess
import re
import random
import math

def generateRand():
    r = random.uniform(-25.0, 25.0)
    return r

def vecindario(rango, numero):
    limInferior = numero - rango
    limSuperior = numero + rango

    if(limSuperior > 25.0):
        r = random.uniform(limInferior, 25.0)
    elif(limInferior < -25.0):
        r = random.uniform(-25.0, limSuperior)
    else:
        r = random.uniform(limInferior, limSuperior)
    return r

def metropolis(x, xP, temp):
    k = 10
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



x1, x2 = generateRand(), generateRand()
output = subprocess.run(["my_func4.exe", f"{x1}", f"{x2}"], capture_output=True, shell=True)
result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
mejor = float(result)
x1prim, x2prim = x1, x2
temp = 100.0
for i in range(100):
    temp = 100/(i+1)
    if(temp<10 and temp > 5):
        #El tamaño del vecindario es de 10
        x1, x2 = vecindario(5, x1prim), vecindario(5, x2prim)
    elif(temp<=5 and temp > 2.5):
        #Varia en 4 el tamaño del vecindario
        x1, x2 = vecindario(2, x1prim), vecindario(2, x2prim)
    elif(temp<=2.5 and temp > 1.5):
        #El tamaño del vecindario sigue siendo de 4 pero solo se modifica uno de los dos valores
        if( i%2 == 0):
            x1 = vecindario(2, x1prim)
        else:
            x2 =  vecindario(2, x2prim)
    elif(temp <= 1.5):
        #El tamaño de vecindario se reduce a 2 y se continua aplicando a un solo valor
        if( i%2 == 0):
            x1 = vecindario(1, x1prim)
        else:
            x2 =  vecindario(1, x2prim)
    elif(temp <= 1.3):
        #El tamaño del vecindario se reduce a 1
        if( i%2 == 0):
            x1 = vecindario(.5, x1prim)
        else:
            x2 =  vecindario(.5, x2prim)
    else:
        #Se generan aleatorios en el rango [-25, 25]
        x1, x2 = generateRand(), generateRand()

    output = subprocess.run(["my_func4.exe", f"{x1}", f"{x2}"], capture_output=True, shell=True)
    result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
    res = float(result)

    print(f"I actual: {i+1} resultado: {round(res,3)} mejor: {round(mejor,3)} combinación: {x1}, {x2} temp: {round(temp, 3)}")

    if(metropolis(mejor, res, temp) == True):
        mejor = res
        x1prim, x2prim = x1, x2
    
print(f"La mejor combinación es: {x1prim}, {x2prim} y su puntaje es {mejor}")