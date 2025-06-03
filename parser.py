from ply_lexer import MyLexer
import ply.yacc as yacc

class Estructura:
    stack_operandos = []
    cubo = {}
    counter_temporales = 0
    cuadruples = []
    saltos = []
    destino = []
    linea = 0
    linea_ciclo = 0
    detector_ciclo = False
    var_names = {}
    dir_func = {}
    tab_vars = {}
    global_int = 0
    global_float = 0
    global_void = 0
    local_int = 0
    local_float = 0
    local_str = 0
    temp_int = 0
    temp_float = 0
    temp_bool = 0
    cte_int	= 0
    cte_float = 0
    cte_str = 0
    isFunc = False
    var_dir = []
    var_tem = []
    variables = []
    len_cte_int = 0
    len_cte_float = 0
    len_cte_str = 0

    len_tem_int = 0
    len_tem_float = 0
    len_tem_bool = 0

    len_loc_int = 0
    len_loc_float = 0
    len_glo_int = 0
    len_glo_float = 0

    
    


    def __init__(self):
        self.stack = []
        self.cubo = {
            #igual
            ('int','int','=') : 'int',
            ('int','float','='): 'error',
            ('float','int','=') : 'float',
            ('float','float','=') : 'float',
            
            #suma
            ('int','int','+'): 'int',
            ('float','int','+'): 'float',
            ('int','float','+'): 'float',
            ('float','float','+'): 'float',
            
            #resta
            ('int','int','-') : 'int',
            ('float','int','-') : 'float',
            ('int','float','-') : 'float',
            ('float','float','-') : 'float',
           
            #divicion
            ('int','int','/') : 'int',
            ('float','int','/') : 'float',
            ('int','float','/') : 'float',
            ('float','float','/') : 'float',
            
            #muti
            ('int','int','*') : 'int',
            ('float','int','*') : 'float',
            ('int','float','*') : 'float',
            ('float','float','*') : 'float',
            
             #mayor que
            ('int','int','>') : 'bool',
            ('float','int','>') : 'bool',
            ('int','float','>') : 'bool',
            ('float','float','>') : 'bool',
            
             #mayor que
            ('int','int','<') : 'bool',
            ('float','int','<') : 'bool',
            ('int','float','<') : 'bool',
            ('float','float','<') : 'bool',
            
             #mayor igual que
            ('int','int','>=') : 'bool',
            ('float','int','>=') : 'bool',
            ('int','float','>=') : 'bool',
            ('float','float','>=') : 'bool',
            
             #menor igual que
            ('int','int','<=') : 'bool',
            ('float','int','<=') : 'bool',
            ('int','float','<=') : 'bool',
            ('float','float','<=') : 'bool',
            
             #distinto 
            ('int','int','!=') : 'bool',
            ('float','int','!=') : 'bool',
            ('int','float','!=') : 'bool',
            ('float','float','!=') : 'bool',
            
             #igual igual
            ('int','int','==') : 'bool',
            ('float','int','==') : 'bool',
            ('int','float','==') : 'bool',
            ('float','float','==') : 'bool',
        }

        self.counter_temporales = 0
        self.cuadruples = [(self.linea,"gotomain",-1,-1,-1)]
        self.linea = 0
        self.linea_ciclo = 0
        self.detector_ciclo = False
        self.var_names = {}
        self.saltos = []
        self.dir_func = {}
       

        
        
        
estructura = Estructura()


m = MyLexer() #crea una instancia del lexer
m.build()      # Construye el lexer 

# Guardamos la tabla de tokens
literals = MyLexer.literals
tokens = MyLexer.tokens + literals

# Listado de casos de prueba
documento = ['ejemplo.ld']
num_caso = 0 # Número de caso 
start = 'program'
# Creamos el parser

def generar_cuadruplo_binario(tipo1, op1, tipo2, op2, operador):
            
            result_type = estructura.cubo[(tipo1, tipo2, operador)]

            if result_type == 'error' or result_type is None:
                raise TypeError(f"Operación inválida: {tipo1} {operador} {tipo2}")
            
            temp = f"t{estructura.counter_temporales}"
            estructura.counter_temporales += 1
            if result_type == 'int':
                estructura.temp_int += 1
                estructura.var_tem.append([temp,12000 + estructura.len_tem_int])
                estructura.len_tem_int +=1
            elif result_type == "float":
                estructura.temp_float += 1
                estructura.var_tem.append([temp,13000 + estructura.len_tem_float])
                estructura.len_tem_float +=1
            else :
                estructura.temp_bool +=1
                estructura.var_tem.append([temp,14000 + estructura.len_tem_bool])
                estructura.len_tem_bool +=1
            estructura.linea +=1
            estructura.cuadruples.append((estructura.linea,operador, op1, op2, temp, result_type))
            estructura.stack_operandos.append((temp, result_type))
            return temp

def agregar_funcion_dir_func(key, tipo, inicio, parametros, variables):
    elementos = []
    estructura.global_void += 1
    for param in parametros:
        elementos.append((param["key"], param["tipo"], "param"))
        if param["tipo"] == "int":
            estructura.local_int += 1
        elif param["tipo"] == "float":
            estructura.local_float += 1
    for var in variables:
        if var["tipo"] == "int" and estructura.isFunc == True:
            estructura.local_int += 1
        elif var["tipo"] == "float" and estructura.isFunc == True:
            estructura.local_float += 1
        elif var["tipo"] == "int" and estructura.isFunc == False:
            estructura.global_int += 1
        elif var["tipo"] == "float" and estructura.isFunc == False:
            estructura.global_float += 1
        elementos.append((var["key"], var["tipo"], "local"))
    estructura.dir_func[key] = {
    'tipo': tipo,
    'inicio': inicio,
    'num_parametros': len(parametros),
    'num_vars': len(variables),
    'variables': elementos
    }

def generar_goto_falso():
    cond, tipo = estructura.stack_operandos.pop()
    if tipo != 'bool':
        raise TypeError("Condición no booleana para IF o WHILE")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea, 'GOTOF', cond, -1, -1))
    estructura.saltos.append(len(estructura.cuadruples) - 1)


def llenar_salto():
    destino = len(estructura.cuadruples)
    salto = estructura.saltos.pop()
    cuad = list(estructura.cuadruples[salto])
    cuad[4] = destino + 1 # índice 4 es el destino del salto
    estructura.cuadruples[salto] = tuple(cuad)

def llenar_salto_else():
    destino = len(estructura.cuadruples)
    salto = estructura.saltos.pop()
    cuad = list(estructura.cuadruples[salto])
    cuad[4] = destino + 1  # índice 4 es el destino del salto
    estructura.cuadruples[salto] = tuple(cuad)

def generar_goto():
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea,'GOTO', -1, -1, -1))
    estructura.saltos.append(len(estructura.cuadruples) - 1)

def hay_ciclo():
    if estructura.detector_ciclo == True: #& op2 != op2.startswith("t"):
        estructura.linea_ciclo += 1
    return

def recolectar_ids(tupla):
    ids = []
    while tupla:
        ids.append(tupla[0])
        tupla = tupla[1]
        print(ids)
    return ids

def unico_constante(constantes):
    valores_vistos = set()
    resultado = []
    for const in constantes:
        valor = const[0]
        if valor not in valores_vistos:
            valores_vistos.add(valor)
            resultado.append(const)
    return resultado

def convert_cuadruplos():
    nuevos_cuadruplos = []

    for cuad in estructura.cuadruples:
        linea = cuad[0]
        op = cuad[1]
        izq = cuad[2]
        der = cuad[3]
        res = cuad[4]
        tipo = cuad[5] if len(cuad) > 5 else None

        # Operaciones que NO necesitan reemplazo
        if op in ("gotomain", "endFun", "gosub", "GOTO"):
            nuevos_cuadruplos.append(cuad)
            continue

        # Reemplazar constantes si están en var_dir
        izq = reemplazar_si_cte(izq)
        der = reemplazar_si_cte(der)
        res = reemplazar_si_cte(res)

        izq = reemplazar_si_tem(izq)
        der = reemplazar_si_tem(der)
        res = reemplazar_si_tem(res)

        izq = reemplazar_si_local_global(izq)
        der = reemplazar_si_local_global(der)
        res = reemplazar_si_local_global(res)

        nuevo_cuad = (linea, op, izq, der, res) if tipo is None else (linea, op, izq, der, res, tipo)
        nuevos_cuadruplos.append(nuevo_cuad)

    estructura.cuadruples = nuevos_cuadruplos

def reemplazar_si_cte(valor):
    for cte in estructura.var_dir:
        if cte[0] == valor:
            return cte[1]
    return valor  # Si no se encuentra, devuelve el mismo valor

def reemplazar_si_tem(valor):
    for cte in estructura.var_tem:
        if cte[0] == valor:
            return cte[1]
    return valor  # Si no se encuentra, devuelve el mismo valor

def reemplazar_si_local_global(nombre_var):
    for funcion in estructura.dir_func.values():
        for cte in funcion['variables']:
            nombre, tipo, scope = cte[:3]

            if nombre == nombre_var:
                # Parámetros o locales → direcciones locales
                if scope == "param" or scope == "local":
                    if tipo == "int":
                        direccion = 7000 + estructura.len_loc_int
                        estructura.len_loc_int += 1
                        return direccion
                    elif tipo == "float":
                        direccion = 8000 + estructura.len_loc_float
                        estructura.len_loc_float += 1
                        return direccion

                # Globales
                elif scope == "global":
                    if tipo == "int":
                        direccion = 1000 + estructura.len_glo_int
                        estructura.len_glo_int += 1
                        return direccion
                    elif tipo == "float":
                        direccion = 2000 + estructura.len_glo_float
                        estructura.len_glo_float += 1
                        return direccion

    # Si no se encuentra la variable, se regresa el mismo valor
    return nombre_var

def exportar_salida(nombre_archivo="salida.txt"):
    with open(nombre_archivo, 'w') as f:
        # 1. Tabla de constantes
        for cte in estructura.var_dir:
            f.write(f"{cte[0]}\t{cte[1]}\n")
        f.write("\n")

        # 2. Contadores
        f.write(f"global_int {estructura.global_int}\n")
        f.write(f"global_float {estructura.global_float}\n")
        f.write(f"global_void {estructura.global_void}\n")
        f.write(f"local_int\t {estructura.local_int}\n")
        f.write(f"local_float {estructura.local_float}\n")
        f.write(f"temp_int\t{estructura.temp_int}\n")
        f.write(f"temp_float {estructura.temp_float}\n")
        f.write(f"temp_bool\t{estructura.temp_bool}\n")
        f.write(f"cte_int\t{estructura.cte_int}\n")
        f.write(f"cte_float\t{estructura.cte_float}\n")
        f.write(f"cte_str\t{estructura.cte_str}\n\n")

        # 3. Cuádruplos
        for i, cuad in enumerate(estructura.cuadruples, start=1):
            linea = cuad[0]
            op = cuad[1]
            izq = cuad[2]
            der = cuad[3]
            res = cuad[4]
            tipo = cuad[5] if len(cuad) > 5 else ""

            f.write(f"\t{linea}\t{op}\t{izq}\t{der}\t{res}\t{tipo}\n")


def p_empty(p):
    'empty :'
    pass

# Type
def p_type_int(p):
    'type : INT'
    p[0] = p[1]

def p_type_float(p):
    'type : FLOAT'
    p[0] = p[1]

# Vars
def p_vars(p):
    'vars : VAR var_ayuda'
    p[0] = [(p[1], p[2])]
    estructura.variables.append(p[2])

def p_var_ayuda(p):
    'var_ayuda : ID var_doble_ayuda ":" type ";" var_ayuda_tail'
    # Procesamos el ID principal
    ids = [p[1]]

    # Procesamos los IDs en la lista (si existen)
    if p[2]:  # p[2] puede ser una tupla de comas
        ids += recolectar_ids(p[2])


    tipo = p[4]
    vars_actuales = [{"key": key, "tipo": tipo} for key in ids]

    if p[6]:
        p[0] = vars_actuales + p[6]
    else:
        p[0] = vars_actuales

def p_var_ayuda_tail(p):
    'var_ayuda_tail : var_ayuda'
    p[0] = p[1]

def p_var_ayuda_tail_empty(p):
    'var_ayuda_tail : empty'
    p[0] = []

def p_var_doble_ayuda(p):
    'var_doble_ayuda : "," ID var_doble_ayuda'
    p[0] = (p[2], p[3])  # Usamos tupla para después desarmar

def p_var_doble_ayuda_empty(p):
    'var_doble_ayuda : empty'
    p[0] = None

# exp
def p_exp_add(p):
    'exp : exp "+" termino'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "+", p[3])


def p_exp_sub(p):
    'exp : exp "-" termino'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "-", p[3])

def p_exp_term(p):
    'exp : termino'
    p[0] = p[1]

# expresión
def p_expression_gt(p):
    'expression : exp ">" exp'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], ">", p[3])
  
 

def p_expression_lt(p):
    'expression : exp "<" exp'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "<", p[3])

 

def p_expression_eq(p):
    'expression : exp EQ exp'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "==", p[3])


def p_expression_ge(p):
    'expression : exp GE exp'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], ">=", p[3])
   

def p_expression_le(p):
    'expression : exp LE exp'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "<=", p[3])
  

def p_expression_ne(p):
    'expression : exp NE exp'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "!=", p[3])
 

def p_expression_exp(p):
    'expression : exp'
    p[0] = p[1]
    
# factor
def p_factor_group(p):
    'factor : "(" expression ")"'
    p[0] = ("(", p[2], ")")

def p_factor_id(p):
    'factor : ID'
    if p[1] not in estructura.var_names:
        estructura.var_names[p[1]] = "int"
    tipo = estructura.var_names[p[1]]
    estructura.stack_operandos.append([p[1],tipo])
    p[0] = p[1]
    
def p_factor_cte(p):
    'factor : cte'
    p[0] = p[1]

def p_factor_pos_id(p):
    'factor : "+" ID'
    p[0] = ("+", p[2])

def p_factor_neg_id(p):
    'factor : "-" ID'
    p[0] = ("-", p[2])

def p_factor_pos_cte(p):
    'factor : "+" cte'
    p[0] = ("+", p[2])

def p_factor_neg_cte(p):
    'factor : "-" cte'
    p[0] = ("-", p[2])


# Print
def p_print_expr(p):
    'print : PRINT "(" expression print_ayuda ")" ";"'
    argumentos = []
    arg, tipo = estructura.stack_operandos.pop()
    argumentos.append(arg)

    # Si hay más argumentos, vienen desde p[4] como lista
    if isinstance(p[4], list):
        argumentos.extend(p[4])

    # Imprimir en orden correcto 
    for arg in reversed(argumentos):
        estructura.linea += 1
        estructura.cuadruples.append((estructura.linea, "Print", arg, -1, -1, "string"))

    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea, "Println", "\ n", -1, -1))
    p[0] = (p[1], "(", p[3], p[4], ")", ";")


def p_print_string(p):
    'print : PRINT "(" CONST_STRING print_ayuda ")" ";"'
    argumentos = [p[3]]
    estructura.cte_str += 1
    m = estructura.len_cte_str
    estructura.var_dir.append([p[3], (19000 + m)])
    estructura.len_cte_str += 1

    if isinstance(p[4], list):
        argumentos.extend(p[4])

    for arg in argumentos:
        estructura.linea += 1
        estructura.cuadruples.append((estructura.linea, "Print", arg, -1, -1, "string"))

    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea, "Println", "\ n", -1, -1))
    p[0] = (p[1], "(", p[3], p[4], ")", ";")


def p_print_ayuda_expr(p):
    'print_ayuda : "," expression print_ayuda'
    arg, tipo = estructura.stack_operandos.pop()
    lista = [arg]
    if isinstance(p[3], list):
        lista += p[3]
    p[0] = lista


def p_print_ayuda_string(p):
    'print_ayuda : "," CONST_STRING print_ayuda'
    lista = [p[2]]
    estructura.cte_str += 1
    if isinstance(p[3], list):
        lista += p[3]
    p[0] = lista


def p_print_ayuda_empty(p):
    'print_ayuda : empty'
    p[0] = []


#Terminp0
def p_termino_mul(p):
    'termino : termino "*" factor'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "*", p[3])

def p_termino_div(p):
    'termino : termino "/" factor'
    op2, tipo2 = estructura.stack_operandos.pop()
    op1, tipo1 = estructura.stack_operandos.pop()
    generar_cuadruplo_binario(tipo1, op1, tipo2, op2, p[2])
    p[0] = (p[1], "/", p[3])

def p_termino_factor(p):
    'termino : factor'
    p[0] = p[1]


# Cycle
def p_cycle(p):
    'cycle : DO marcar_cycle_inicio body marcar_cycle_final WHILE "(" expression ")" ";"'
    p[0] = (p[1], p[2], p[3], "(", p[5], ")", ";")
    
def p_marcar_cycle_inicio(p):
    'marcar_cycle_inicio :'
    estructura.detector_ciclo = True


def p_marcar_cycle_final(p):
    'marcar_cycle_final :'
    estructura.linea += 1
    saltos_dados = estructura.linea - estructura.linea_ciclo
    val = saltos_dados
    for cuadruple in estructura.cuadruples[val-1:estructura.linea-1]:  # tu lista de cuádruples
        if None in cuadruple[:5]:
            break
        saltos_dados += 1
    estructura.cuadruples.append((estructura.linea, 'GOTOV', -1, -1, saltos_dados))
    estructura.linea_ciclo = 0 
    estructura.detector_ciclo = False

#Condition
def p_condition_if(p):
    'condition : IF "(" expression ")" marcar_if_inicio body ";"'
    p[0] = (p[1], "(", p[3], ")", p[6], ";")
    llenar_salto() #marcar el salto

# todavia no funciona
def p_condition_if_else(p):
    'condition : IF "(" expression ")" marcar_if_inicio  body marcar_if_final ELSE marcar_else_inicio body marcar_else_final ";"'
    p[0] = (p[1], "(", p[3], ")", p[6], p[8], p[10], ";")

def p_marcar_if_inicio(p):
    'marcar_if_inicio :'
    generar_goto_falso()

def p_marcar_if_final(p):
    'marcar_if_final :'
    llenar_salto_else()

def p_marcar_else_inicio(p):
    'marcar_else_inicio :'
    generar_goto()

def p_marcar_else_final(p):
    'marcar_else_final :'
    llenar_salto_else()
    

# Assign
def p_assign(p):
    'assign : ID "=" expression ";"'
    valor, tipo = estructura.stack_operandos.pop()
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea,'=', valor, -1, p[1], tipo))
    estructura.var_names[p[1]] = tipo
    p[0] = (p[1], "=", p[3], ";")
    
# f_call
def p_f_call_args(p):
    'f_call : ID "(" expression f_call_ayuda ")" ";"'
    
    arg, tipo = estructura.stack_operandos.pop()
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "param", arg, -1, tipo))
    p[0] = (p[1], "(", p[3], p[4], ")", ";")
    estructura.linea +=1
    if p[1] in estructura.dir_func:
        des = estructura.dir_func[p[1]]["inicio"]
    else:
        print(f"La función '{p[0]}' no existe en dir_func.")
        des = -1
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "gosub", p[1], -1, des))
    
def p_f_call_no_args(p):
    'f_call : ID "(" ")" ";"'
    p[0] = (p[1], "(", ")", ";")
    if p[1] in estructura.dir_func:
        des = estructura.dir_func[p[1]]["inicio"]
    else:
        print(f"La función '{p[1]}' no existe en dir_func.")
        des = -1
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "gosub", p[1], -1, des))

def p_f_call_ayuda(p):
    'f_call_ayuda : "," expression f_call_ayuda'
    arg, tipo = estructura.stack_operandos.pop()
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "param", arg, -1, tipo))
    p[0] = (",", p[2], p[3])

def p_f_call_ayuda_empty(p):
    'f_call_ayuda : empty'
    p[0] = p[1]

# statements
def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]
    hay_ciclo()

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]
    hay_ciclo()

def p_statement_assign(p):
    'statement : assign'
    p[0] = p[1]
    hay_ciclo()

def p_statement_condition(p):
    'statement : condition'
    p[0] = p[1]
    hay_ciclo()

def p_statement_cycle(p):
    'statement : cycle'
    p[0] = p[1]
    hay_ciclo()

def p_statement_f_call(p):
    'statement : f_call'
    p[0] = p[1]
    hay_ciclo()

def p_statement_print(p):
    'statement : print'
    p[0] = p[1]
    hay_ciclo()

# body
def p_body(p):
    'body : "{" statements "}"'
    p[0] = ("{", p[2], "}")


# cte
def p_cte_int(p):
    'cte : CONST_INT'
    estructura.stack_operandos.append([p[1], 'int'])
    estructura.cte_int += 1
    p[0] = p[1]
    m = estructura.len_cte_int
    estructura.var_dir.append([p[1], (17000 + m)])
    estructura.len_cte_int +=1


def p_cte_float(p):
    'cte : CONST_FLOAT'
    estructura.stack_operandos.append([p[1], 'float'])
    estructura.cte_float += 1
    p[0] = p[1]
    m = estructura.len_cte_float
    estructura.var_dir.append([p[1], (18000 + m)])
    estructura.len_cte_float += 1

 
# Funcs
def p_funcs_params(p):
    'func : VOID ID "(" ID ":" type funcs_ayuda ")" func_start "[" vars body "]" ";"'
    estructura.isFunc = True
    p[0] = (p[1], p[2], "(", p[4], ":", p[6], p[7], ")", "[", p[11], p[12], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", -1, -1,-1))
    estructura.saltos.append(len(estructura.cuadruples) - 1)
    llenar_salto()

    parametros = [{"key": p[4], "tipo": p[6]}]
    parametros.extend(p[7])
    
    agregar_funcion_dir_func(
        key=p[2],
        tipo="void",
        inicio=estructura.destino[-1],  # línea de inicio
        parametros=parametros,
        variables=estructura.variables.pop()
    )
    parametros = []
    estructura.isFunc = False

def p_funcs_empty_params(p):
    'func : VOID ID "(" ")" func_start "[" vars body "]" ";"'
    estructura.isFunc = True
    p[0] = (p[1], p[2], "(", ")", "[", p[7], p[8], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", -1, -1,-1))
    estructura.saltos.append(len(estructura.cuadruples) - 1)
    llenar_salto()

    parametros = []
    
    agregar_funcion_dir_func(
        key= p[2],
        tipo= "void",
        inicio= estructura.destino[-1], 
        parametros= parametros,
        variables= estructura.variables.pop()
    )
    estructura.isFunc = False

def p_funcs_params_no_vars(p):
    'func : VOID ID "(" ID ":" type funcs_ayuda ")" func_start "[" body "]" ";"'
    estructura.isFunc = True
    p[0] = (p[1], p[2], "(", p[4], ":", p[6], p[7], ")", "[", p[11], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", -1, -1,-1))
    estructura.saltos.append(len(estructura.cuadruples) - 1) 
    llenar_salto()
    
    parametros = [{"key": p[4], "tipo": p[6]}]
    parametros.extend(p[7])
    
    agregar_funcion_dir_func(
        key=p[2],
        tipo="void",
        inicio=estructura.destino[-1], 
        parametros=parametros,
        variables = [] 
    )
    parametros = []
    estructura.isFunc = False

def p_funcs_empty_params_no_vars(p):
    'func : VOID ID "(" ")" func_start "[" body "]" ";"'
    estructura.isFunc = True
    p[0] = (p[1], p[2], "(", ")", "[", p[7], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", -1, -1,-1))
    estructura.saltos.append(len(estructura.cuadruples) - 1)
    llenar_salto()
    agregar_funcion_dir_func(
        key=p[2],
        tipo="void",
        inicio=estructura.destino[-1], 
        parametros= [],
        variables= []
    )
    estructura.isFunc = False


def p_func_start(p):
    'func_start : '
    estructura
    estructura.linea +=1
    estructura.destino.append(estructura.linea)
    estructura.linea -=1

def p_funcs_list(p):
    'funcs_list : funcs_list func'
    p[0] = p[1] + [p[2]]

def p_funcs_list_single(p):
    'funcs_list : func'
    p[0] = [p[1]]

def p_funcs_list_empty(p):
    'funcs_list : empty'
    p[0] = []

def p_funcs_ayuda(p):
    'funcs_ayuda : "," ID ":" type funcs_ayuda'
    #p[0] = (",", p[2], ":", p[4], p[5])
    p[0] = [{"key": p[2], "tipo": p[4]}] + p[5]

def p_funcs_ayuda_empty(p):
    'funcs_ayuda : empty'
    p[0] = []

    
# Program
def p_program(p):
    'program : PROGRAM ID ";" vars funcs_list MAIN inicio_main body END'
    p[0] = (p[1], p[2], ";", p[4], p[5], p[6], p[8], p[9])
    estructura.isFunc = False
    agregar_funcion_dir_func(
        key= p[2],
        tipo= "program",
        inicio= 0,  # línea de inicio
        parametros= [],
        variables= estructura.variables.pop()
    )

def p_inicio_main(p):
    'inicio_main : '
    estructura.cuadruples[0] = (0,"gotomain",-1,-1,estructura.linea+1)

# error
def p_error(p):
    if p:
         print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")
    
parser = yacc.yacc()

#Función para la lectura del listado de casos de prueba
for caso in documento:
    num_caso += 1 
    with open(caso, 'r') as file:
        codigo = file.read()
    print(f'Caso {num_caso}: {caso}')
    m.tabla(codigo)

    try:
        print('\n')
        result = parser.parse(codigo, lexer=m.lexer)
        print(result)
        print("\nCuádruplos generados:")
        convert_cuadruplos()
        for i in estructura.cuadruples:
            print(i)
        print("\nTabla de funciones:")
        for key, valor in estructura.dir_func.items():
            print(f"\nkey: {key}, Tipo: {valor['tipo']}, Inicio: {valor['inicio']}, n_params: {valor['num_parametros']}")
            print("Tabla de variables: ")
            for var in valor['variables']:
                print(f"    key: {var[0]}, Tipo: {var[1]}, Scope: {var[2]}")

    except SyntaxError as e:
        print(e)


    print("\n")

    constantes = unico_constante(estructura.var_dir)
    print(constantes)


    print(f"""
global_int {estructura.global_int}
global_float {estructura.global_float}
global_void {estructura.global_void}
\nlocal_int {estructura.local_int}
local_float {estructura.local_float}
\ntemp_int {estructura.temp_int}
temp_float {estructura.temp_float}
temp_bool {estructura.temp_bool}
\ncte_int {estructura.cte_int}
cte_float {estructura.cte_float}
cte_str {estructura.cte_str}
""")
    
    exportar_salida("salida.txt")
    print("Archivo 'salida.txt' generado exitosamente.")
    m.clear_table()
    estructura = Estructura()
    
