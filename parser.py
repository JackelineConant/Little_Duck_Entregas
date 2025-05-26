from ply_lexer import MyLexer
import ply.yacc as yacc

class Estructura:
    stack_operandos = []
    cubo = {}
    counter_temporales = 0
    cuadruples = []
    saltos = []
    linea = 0
    var_names = {}
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
    cuad[4] = destino  # índice 4 es el destino del salto
    estructura.cuadruples[salto] = tuple(cuad)

def generar_goto():
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea,'GOTO', None, None, None))
    estructura.saltos.append(len(estructura.cuadruples) - 1)


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

def p_var_ayuda(p):
    'var_ayuda : ID var_doble_ayuda ":" type ";" var_ayuda_tail'
    p[0] = (p[1], p[2], ":", p[4], ";", p[6])

def p_var_ayuda_tail(p):
    'var_ayuda_tail : var_ayuda'
    p[0] = p[1]

def p_var_ayuda_tail_empty(p):
    'var_ayuda_tail : empty'
    p[0] = p[1]

def p_var_doble_ayuda(p):
    'var_doble_ayuda : "," ID var_doble_ayuda'
    p[0] = (",", p[2], p[3])

def p_var_doble_ayuda_empty(p):
    'var_doble_ayuda : empty'
    p[0] = p[1]

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
    arg, tipo = estructura.stack_operandos.pop()
    estructura.counter_temporales += 1
    estructura.linea +=1
    estructura.cuadruples.append(((estructura.linea,"Print", arg , None)))
    p[0] = (p[1], "(", p[3], p[4], ")", ";")
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea,"Print", "\n", None,))


def p_print_string(p):
    'print : PRINT "(" CONST_STRING print_ayuda ")" ";"'   
    estructura.counter_temporales += 1
    estructura.linea +=1
    estructura.cuadruples.append(((estructura.linea,"Print", p[3] , None)))
    
    p[0] = (p[1], "(", p[3], p[4], ")", ";")
    estructura.linea +=1
    estructura.cuadruples.append((estructura.linea,"Print", "\n", None,))


def p_print_ayuda_expr(p):
    'print_ayuda : "," expression print_ayuda'
    p[0] = (",", p[2], p[3])

def p_print_ayuda_string(p):
    'print_ayuda : "," STRING print_ayuda'
    p[0] = (",", p[2], p[3])

def p_print_ayuda_empty(p):
    'print_ayuda : empty'
    p[0] = p[1]

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
    '''
    condition : IF "(" expression ")" marcar_if_inicio body ";"
    '''
    llenar_salto()
    p[0] = ("IF", p[3], p[6])

def p_marcar_if_inicio(p):
    'marcar_if_inicio :'
    generar_goto_falso()


def p_condition_if_else(p):
    '''
    condition : IF "(" expression ")" marcar_if_else_inicio body marcar_else_inicio ELSE body ";"
    '''
    llenar_salto()  # Llenamos el salto que quedó pendiente al final del else
    p[0] = ("IF-ELSE", p[3], p[6], p[9])

# Genera GOTOF para condición falsa y guarda el salto pendiente
def p_marcar_if_else_inicio(p):
    'marcar_if_else_inicio :'
    generar_goto_falso()

# Al terminar el bloque del IF, genera un GOTO para saltarse el ELSE
# Y llena el salto del GOTOF con la línea actual (inicio del else)
def p_marcar_else_inicio(p):
    'marcar_else_inicio :'
    generar_goto()
    llenar_salto()  # llena el salto del GOTOF (si condición fue falsa)




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
    p[0] = (p[1], "(", p[3], p[4], ")", ";")

def p_f_call_no_args(p):
    'f_call : ID "(" ")" ";"'
    p[0] = (p[1], "(", ")", ";")

def p_f_call_ayuda(p):
    'f_call_ayuda : "," expression f_call_ayuda'
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
    'funcs : VOID ID "(" ID ":" type funcs_ayuda ")" "[" vars body "]" ";"'
    p[0] = (p[1], p[2], "(", p[4], ":", p[6], p[7], ")", "[", p[10], p[11], "]", ";")

def p_funcs_empty_params(p):
    'funcs : VOID ID "(" ")" "[" vars body "]" ";"'
    p[0] = (p[1], p[2], "(", ")", "[", p[6], p[7], "]", ";")

def p_funcs_params_no_vars(p):
    'funcs : VOID ID "(" ID ":" type funcs_ayuda ")" "[" body "]" ";"'
    p[0] = (p[1], p[2], "(", p[4], ":", p[6], p[7], ")", "[", p[10], "]", ";")

def p_funcs_empty_params_no_vars(p):
    'funcs : VOID ID "(" ")" "[" body "]" ";"'
    p[0] = (p[1], p[2], "(", ")", "[", p[6], "]", ";")

def p_funcs_multiple(p):
    'funcs : funcs funcs'
    p[0] = p[1] + [p[2]]

def p_funcs_empty(p):
    'funcs : empty'
    p[0] = p[1]

def p_funcs_ayuda(p):
    'funcs_ayuda : "," ID ":" type funcs_ayuda'
    p[0] = (",", p[2], ":", p[4], p[5])

def p_funcs_ayuda_empty(p):
    'funcs_ayuda : empty'
    p[0] = p[1]

    
# Program
def p_program(p):
    'program : PROGRAM ID ";" vars funcs MAIN body END'

    p[0] = (p[1], p[2], ";", p[4], p[5], p[6], p[7], p[8])

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
        

    except SyntaxError as e:
        print(e)


    m.clear_table()
    estructura.stack_operandos = []
    estructura.cuadruples = []
    estructura.counter_temporales = 0
    estructura.saltos = []
    print("\n")