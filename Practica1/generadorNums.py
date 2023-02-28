import subprocess
import re

mayor = 0.0
for i in range(10):
    for j in range(0, 100,5):
        output = subprocess.run(["my_func.exe", f"{i}.{j}"], capture_output=True, shell=True)
        result = re.sub(r'[^0-9.]', '', output.stdout.decode('utf-8'))
        res = float(result)
        if(mayor<res and res!= 15.0):
            mayor = res
        print(f"x={i}.{j} y={res} el mayor hasta ahora es:{mayor} intento no. {j+i*10}")
        j+=5