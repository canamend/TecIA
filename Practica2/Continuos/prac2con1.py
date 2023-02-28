import subprocess
import re
import random
import math

def generateRand():
    r = random.uniform(-25.0, 25.0)
    return r

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



x1, x2 = generateRand(), generateRand()
output = subprocess.run(["my_func4.exe", f"{x1}", f"{x2}"], capture_output=True, shell=True)
result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
mejor = int(float(result))
temp = 200.0
for i in range(100):
    temp = 200/(i+1)
    if(temp<10):
        #Evalúa si se acerca a aun resultado óptimo
        
        if(mejor > 150 and i < 60):
            # Ir refinando resultados cuando resultado disminuya (variar cada vez menos nodos por permutación)
            x1, x2 = generateRand(), generateRand()
        else:
            x1, x2 = generateRand(), generateRand()
    else:
        x1, x2 = generateRand(), generateRand()

    output = subprocess.run(["my_func4.exe", f"{x1}", f"{x2}"], capture_output=True, shell=True)
    result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
    res = int(float(result))

    print(f"Iteración actual: {i} resultado: {res} mejor: {mejor} combinación: {x1}, {x2} temp: {round(temp, 3)}")

    if(metropolis(mejor, res, temp) == True):
        mejor = res
        x1prim, x2prim = x1, x2
    
print(f"La mejor combinación es: {x1prim}, {x2prim} y su puntaje es {mejor}")