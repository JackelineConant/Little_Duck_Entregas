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
    var_names = {}
    dir_func = {}
    tab_vars = {}
    


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
        self.cuadruples = [(self.linea,"main",None,None,None)]
        self.linea = 0
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
documento = ['ejemplo.txt']
num_caso = 0 # Número de caso 
start = 'program'
# Creamos el parser

def generar_cuadruplo_binario(tipo1, op1, tipo2, op2, operador):
            
            result_type = estructura.cubo[(tipo1, tipo2, operador)]

            if result_type == 'error' or result_type is None:
                raise TypeError(f"Operación inválida: {tipo1} {operador} {tipo2}")
            
            temp = f"t{estructura.counter_temporales}"
            estructura.counter_temporales += 1
            estructura.linea +=1
            estructura.cuadruples.append((estructura.linea,operador, op1, op2, temp, result_type))
            estructura.stack_operandos.append((temp, result_type))
            return temp

def agregar_funcion_dir_func(key, tipo, inicio, parametros, variables):
    elementos = []
    for param in parametros:
        elementos.append((param["key"], param["tipo"], "param"))
    for var in variables:
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
    estructura.cuadruples.append((estructura.linea, 'GOTOF', cond, None, None))
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
    estructura.cuadruples.append((estructura.linea,'GOTO', None, None, None))
    estructura.saltos.append(len(estructura.cuadruples) - 1)

def recolectar_ids(tupla):
    ids = []
    while tupla:
        ids.append(tupla[0])
        tupla = tupla[1]
    return ids

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
    estructura.vars = p[2]

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
        estructura.cuadruples.append((estructura.linea, "Print", arg, None))

    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea, "Print", "\n", None))
    p[0] = (p[1], "(", p[3], p[4], ")", ";")


def p_print_string(p):
    'print : PRINT "(" CONST_STRING print_ayuda ")" ";"'
    argumentos = [p[3]]

    if isinstance(p[4], list):
        argumentos.extend(p[4])

    for arg in argumentos:
        estructura.linea += 1
        estructura.cuadruples.append((estructura.linea, "Print", arg, None))

    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea, "Print", "\n", None))
    p[0] = (p[1], "(", p[3], p[4], ")", ";")


def p_print_ayuda_expr(p):
    'print_ayuda : "," expression print_ayuda'
    arg, tipo = estructura.stack_operandos.pop()
    lista = [arg]
    if isinstance(p[3], list):
        lista += p[3]
    p[0] = lista


def p_print_ayuda_string(p):
    'print_ayuda : "," STRING print_ayuda'
    lista = [p[2]]
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
    'cycle : DO body WHILE "(" expression ")" ";"'
    p[0] = (p[1], p[2], p[3], "(", p[5], ")", ";")

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
    estructura.cuadruples.append((estructura.linea,'=', valor, None, p[1], tipo))
    estructura.var_names[p[1]] = tipo
    p[0] = (p[1], "=", p[3], ";")
    
# f_call
def p_f_call_args(p):
    'f_call : ID "(" expression f_call_ayuda ")" ";"'
    
    arg, tipo = estructura.stack_operandos.pop()
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "param", arg, None, tipo))
    p[0] = (p[1], "(", p[3], p[4], ")", ";")
    estructura.linea +=1
    if p[1] in estructura.dir_func:
        des = estructura.dir_func[p[1]]["inicio"]
    else:
        print(f"La función '{p[0]}' no existe en dir_func.")
        des = None
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "gosub", p[1], None, des))
    
def p_f_call_no_args(p):
    'f_call : ID "(" ")" ";"'
    p[0] = (p[1], "(", ")", ";")
    if p[1] in estructura.dir_func:
        des = estructura.dir_func[p[1]]["inicio"]
    else:
        print(f"La función '{p[1]}' no existe en dir_func.")
        des = None
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "gosub", p[1], None, des))

def p_f_call_ayuda(p):
    'f_call_ayuda : "," expression f_call_ayuda'
    arg, tipo = estructura.stack_operandos.pop()
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea, "param", arg, None, tipo))
    p[0] = (",", p[2], p[3])

def p_f_call_ayuda_empty(p):
    'f_call_ayuda : empty'
    p[0] = p[1]

# statements
def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]

def p_statement_assign(p):
    'statement : assign'
    p[0] = p[1]

def p_statement_condition(p):
    'statement : condition'
    p[0] = p[1]

def p_statement_cycle(p):
    'statement : cycle'
    p[0] = p[1]

def p_statement_f_call(p):
    'statement : f_call'
    p[0] = p[1]

def p_statement_print(p):
    'statement : print'
    p[0] = p[1]

# body
def p_body(p):
    'body : "{" statements "}"'
    p[0] = ("{", p[2], "}")


# cte
def p_cte_int(p):
    'cte : CONST_INT'
    estructura.stack_operandos.append([p[1], 'int'])
    p[0] = p[1]

def p_cte_float(p):
    'cte : CONST_FLOAT'
    estructura.stack_operandos.append([p[1], 'float'])
    p[0] = p[1]

 
# Funcs
def p_funcs_params(p):
    'func : VOID ID "(" ID ":" type funcs_ayuda ")" func_start "[" vars body "]" ";"'
    p[0] = (p[1], p[2], "(", p[4], ":", p[6], p[7], ")", "[", p[11], p[12], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", None, None,None))
    estructura.saltos.append(len(estructura.cuadruples) - 1)
    llenar_salto()

    parametros = [{"key": p[4], "tipo": p[6]}]
    if isinstance(p[7], list):
        for i in range(0, len(p[7]), 4):
            parametros.append({"key": p[7][i+1], "tipo": p[7][i+3]})
    
    agregar_funcion_dir_func(
        key=p[2],
        tipo="void",
        inicio=estructura.destino[-1],  # línea de inicio
        parametros=parametros,
        variables=estructura.vars
    )

def p_funcs_empty_params(p):
    'func : VOID ID "(" ")" func_start "[" vars body "]" ";"'
    p[0] = (p[1], p[2], "(", ")", "[", p[7], p[8], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", None, None,None))
    estructura.saltos.append(len(estructura.cuadruples) - 1)
    llenar_salto()

    parametros = []
    
    agregar_funcion_dir_func(
        key=p[2],
        tipo="void",
        inicio=estructura.destino[-1], 
        parametros=parametros,
        variables=estructura.vars
    )
    estructura.vars = []

def p_funcs_params_no_vars(p):
    'func : VOID ID "(" ID ":" type funcs_ayuda ")" func_start "[" body "]" ";"'
    p[0] = (p[1], p[2], "(", p[4], ":", p[6], p[7], ")", "[", p[11], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", None, None,None))
    estructura.saltos.append(len(estructura.cuadruples) - 1) 
    llenar_salto()
    
    parametros = [{"key": p[4], "tipo": p[6]}]
    if isinstance(p[7], list):
        for i in range(0, len(p[7]), 4):
            parametros.append({"key": p[7][i+1], "tipo": p[7][i+3]})
    estructura.vars = []
    
    agregar_funcion_dir_func(
        key=p[2],
        tipo="void",
        inicio=estructura.destino[-1], 
        parametros=parametros,
        variables=estructura.vars
    )

    

def p_funcs_empty_params_no_vars(p):
    'func : VOID ID "(" ")" func_start "[" body "]" ";"'
    p[0] = (p[1], p[2], "(", ")", "[", p[7], "]", ";")
    estructura.linea += 1
    estructura.cuadruples.append((estructura.linea,"endFun", None, None,None))
    estructura.saltos.append(len(estructura.cuadruples) - 1)
    llenar_salto()

    

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
    p[0] = (",", p[2], ":", p[4], p[5])

def p_funcs_ayuda_empty(p):
    'funcs_ayuda : empty'
    p[0] = p[1]

    
# Program
def p_program(p):
    'program : PROGRAM ID ";" vars funcs_list MAIN inicio_main body END'
    p[0] = (p[1], p[2], ";", p[4], p[5], p[6], p[8], p[9])

def p_inicio_main(p):
    'inicio_main : '
    estructura.cuadruples[0] = (0,"main",None,estructura.linea+1,None)

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


    m.clear_table()
    estructura.stack_operandos = []
    estructura.cuadruples = []
    estructura.counter_temporales = 0
    estructura.saltos = []
    estructura.destino = []
    estructura.dir_func = {}
    estructura.var_names = []
    estructura.tab_vars = []
    print("\n")