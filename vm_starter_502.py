
# -*- coding: utf-8 -*-

try:
    with open('salida.txt', 'r') as archivo:
        test = archivo.read()
    print("Archivo 'salida.txt' leído correctamente.")
except FileNotFoundError:
    print("Error: El archivo 'salida.txt' no fue encontrado.")
    exit()

# info sobre los indices de cada region para simular la memoria
regions = { "global_int" : [1000] ,
"global_float" : [2000] ,
"global_str" : [3000] ,
"global_void" : [4000] ,
"local_int" : [7000] ,
"local_float" : [8000] ,
"local_str" : [9000] ,
"temp_int" : [12000] ,
"temp_float" : [13000] ,
"temp_bool" : [14000] ,
"cte_int" : [17000] ,
"cte_float" : [18000] ,
"cte_str" : [19000] }
class Cuadruplo:
    def __init__(self, lista):
        if len(lista) != 5:
            raise ValueError(f"Cuádruplo inválido: {lista}")
        self.operador = lista[1]
        self.argIzq = int(lista[2]) if lista[2].isdigit() or (lista[2][0] == '-' and lista[2][1:].isdigit()) else -1
        self.argDer = int(lista[3]) if lista[3].isdigit() or (lista[3][0] == '-' and lista[3][1:].isdigit()) else -1
        self.destino = int(lista[4]) if lista[4].isdigit() or (lista[4][0] == '-' and lista[4][1:].isdigit()) else -1


test_split = test.split('\n')

memo = {}
cuads = [Cuadruplo([-1, 'NOP', '-1', '-1', '-1'])]
section = 0

for l in test_split:
    linea = l.split()
    if l.strip() == '':
      section += 1
    elif section == 0 and len(linea) == 2:
        dir = int(linea[1])
        if dir < 18000:
            memo[dir] = int(linea[0])
        elif dir < 19000:
            memo[dir] = float(linea[0])
        else:
            memo[dir] = linea[0]
    if len(linea) == 5:
      #Seccion de los cuadruplos
      cuads.append(Cuadruplo(linea))

    


# simulación
indx = 1
while indx < len(cuads):
    q = cuads[indx]
    if q.operador == 'gotomain':
        indx = q.destino
    elif q.operador == '=':
        # 2 = 17000 -1 1000
        # memo[1000] = memo[1700]
        memo[q.destino] = memo[q.argIzq]
        indx += 1
    elif q.operador == '/':
        memo[q.destino] = memo[q.argIzq] / memo[q.argDer]
        indx += 1
    elif q.operador == '*':
        memo[q.destino] = memo[q.argIzq] * memo[q.argDer]
        indx += 1
    elif q.operador == '+':
        memo[q.destino] = memo[q.argIzq] + memo[q.argDer]
        indx += 1
    elif q.operador == '-':
        memo[q.destino] = memo[q.argIzq] - memo[q.argDer]
        indx += 1
    elif q.operador == '!=':
        memo[q.destino] = int(memo[q.argIzq] != memo[q.argDer])
        indx += 1
    elif q.operador == '==':
        memo[q.destino] = int(memo[q.argIzq] == memo[q.argDer])
        indx += 1
    elif q.operador == '>=':
        memo[q.destino] = int(memo[q.argIzq] >= memo[q.argDer])
        indx += 1
    elif q.operador == '<=':
        memo[q.destino] = int(memo[q.argIzq] <= memo[q.argDer])
        indx += 1
    elif q.operador == 'Print':
        print(memo.get(q.argIzq, f"(no definido: {q.argIzq})"), end=" ")
        indx += 1
    elif q.operador == 'Println':
        print()
        indx += 1
    elif q.operador == 'GOTOF':
        if not memo[q.argIzq]:
            indx = q.destino
        else:
            indx += 1