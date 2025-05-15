from ply_lexer import MyLexer
import ply.yacc as yacc

m = MyLexer() #crea una instancia del lexer
m.build()      # Construye el lexer 

# Guardamos la tabla de tokens
literals = MyLexer.literals
tokens = MyLexer.tokens + literals


# Listado de casos de prueba
documento = ['conversion_metros_yardas.ld','celsius_to_fahrenheit.ld','serie_fibonnacci.ld','mayor_valor.ld']
num_caso = 0 # Número de caso 

# Creamos el parser
#names = { }

def p_program(p):
    'program : PROGRAM ID ";" vars funcs MAIN body END'
    p[0] = (p[1], p[2], ";", p[4], p[5], p[6],p[7],p[8])

def p_program_none(p):
    'program : '
    pass

def p_vars_a(p):
    'vars : VAR var_ayuda'
    p[0] = (p[1], p[2])

def p_vars_none(p):
    'vars : '
    pass
    
def p_var_ayuda_a(p):
    'var_ayuda : ID var_doble_ayuda ":" type ";" var_ayuda'
    p[0] = (p[1], p[2], ":", p[4], ";", p[5])
    
def p_var_ayuda_none(p):
    'var_ayuda : '
    pass

def p_var_doble_ayuda_a(p):
    'var_doble_ayuda : "," ID var_doble_ayuda' 
    p[0] = (",", p[2],p[3])     

def p_var_doble_ayuda_none(p):
    'var_doble_ayuda : ' 
    pass    
    
def p_type_i(p):
    'type : INT'
    p[0] = p[1]
    names += 'type : INT'
    
def p_type_f(p):
    'type : FLOAT'
    p[0] = p[1]
    
def p_body(p):
    'body : "{" statement "}"'
    p[0] = { p[2] }

def p_statement_a(p):
    'statement : assign'
    p[0] = p[1]
    
def p_statement_b(p):
    'statement : condition'
    p[0] = p[1]
    
def p_statement_c(p):
    'statement : cycle'
    p[0] = p[1]

def p_statement_d(p):
    'statement : f_call'
    p[0] = p[1]

def p_statement_e(p):
    'statement : print'
    p[0] = p[1]
    
def p_statement_f(p):
    'statement : statement'
    p[0] = p[1]
    
def p_statement_none(p):
    'statement : '
    pass
    
def p_print_a(p):
    'print : PRINT "(" expression print_ayuda ")" ";"'
    p[0] = (p[1], "(", p[3], p[4], ")", ";")

def p_print_b(p):
    'print : PRINT "(" STRING print_ayuda ")" ";"'
    p[0] = (p[1], "(", p[3], p[4], ")", ";")
    
def p_print_ayuda_a(p):
    'print_ayuda : "," expression print_ayuda'
    p[0] = (",", p[2], p[3])
    
def p_print_ayuda_b(p):
    'print_ayuda : "," STRING print_ayuda'
    p[0] = (",", p[2], p[3])

def p_print_ayuda_none(p):
    'print_ayuda : '
    pass
    
def p_cycle(p):
    'cycle : DO body WHILE "(" expression ")" ";"'
    p[0] = ( p[1], p[2], p[3], "(", p[5], ")", ";")

'''def p_cycle(p):
    'cycle : '
    pass'''
    
def p_condition_a(p):
    'condition : IF "(" expression ")" body ";"'
    p[0] = (p[1], "(", p[3], ")", p[5], ";")
    
def p_condition_b(p):
    'condition : IF "(" expression ")" body ELSE body ";"'
    p[0] = (p[1], "(", p[3], ")", p[5], p[6], p[7], ";" )
    
def p_assign_a(p):
    'assign : ID "=" expression ";"'
    p[0] = (p[1], "=", p[3], ";") 
    
def p_assign_none(p):
    'assign : '
    pass
    
def p_expression_a(p):
    'expression : exp ">" exp'
    p[0] = p[1] > p[3]
    
def p_expression_b(p):
    'expression : exp "<" exp'
    p[0] = p[1] > p[3]
    
def p_expression_c(p):
    'expression : exp EQ exp'
    p[0] = p[1] == p[3]
    
def p_expression_d(p):
    'expression : exp GE exp'
    p[0] = p[1] >= p[3]
    
def p_expression_f(p):
    'expression : exp LE exp'
    p[0] = p[1] <= p[3]
    
def p_expression_g(p):
    'expression : exp NE exp'
    p[0] = p[1] != p[3]

def p_expression_h(p):
    'expression : exp '
    p[0] = p[1]
       
def p_expression_none(p):
    'expression : '
    pass

def p_cte_a(p):
    'cte : INT'
    p[0] = p[1]
    
def p_cte_b(p):
    'cte : FLOAT'
    p[0] = p[1]

def p_exp_i(p):
    ' exp : termino exp'
    p[0] = (p[1],p[2])
 
def p_exp_a(p):
    ' exp : termino "+" termino'
    p[0] = ("+", p[2],p[3])
    
def p_exp_ayuda_b(p):
    ' exp : termino "-" termino '
    p[0] = ("-", p[2],p[3])
    

def p_termino(p):
    ' termino : factor termino_ayuda'
    p[0] = (p[1],p[2])
    
def p_termino_ayuda_a(p):
    ' termino_ayuda : "/" factor termino_ayuda'
    p[0] = ("/", p[2],p[3])
    
def p_termino_ayuda_b(p):
    ' termino_ayuda : "*" factor termino_ayuda'
    p[0] = ("*", p[2],p[3])
    
def p_termino_ayuda_none(p):
    ' termino_ayuda : '
    pass

def p_factor_a(p):
    'factor : "(" expression ")"'
    p[0] = ("(", p[2], ")")
    
def p_factor_b(p):
    'factor : ID'
    p[0] = p[1]
    
def p_factor_c(p):
    'factor : "+" ID'
    p[0] = + p[2]
    
def p_factor_d(p):
    'factor : "-" ID'
    p[0] = - p[2]
    
def p_factor_f(p):
    'factor : "+" cte'
    p[0] = + p[2]
    
def p_factor_g(p):
    'factor : "-" cte'
    p[0] = - p[2]
    
def p_funcs_a(p):
    'funcs : VOID ID "("  ID ":" type funcs_ayuda ")" "[" vars body "]" ";"'
    p[0] = (p[1],p[2],"(",p[4], ":", p[6], p[7],")","[", p[10],p[11],"]",";")
    
def p_funcs_b(p):
    'funcs : VOID ID "(" ")" "[" vars body "]" ";"'
    p[0] = (p[1],p[2],"(", ")","[", p[6],p[7],"]",";")

def p_funcs_c(p):
    'funcs : VOID ID "(" ID ":" type funcs_ayuda ")" "[" body "]" ";"'
    p[0] = (p[1],p[2],"(",p[4], ":", p[6], p[7],")","[", p[10],"]",";")
 
def p_funcs_d(p):
    'funcs : VOID ID "(" ")" "[" body "]" ";"'
    p[0] = (p[1],p[2],"(", ")","[", p[6],"]",";") 

def p_funcs_ayuda_a(p):
    'funcs_ayuda : "," ID ":" type funcs_ayuda'
    p[0] = (",", p[2], ":", p[4], p[5])
     
def p_funcs_ayuda_none(p): 
    'funcs_ayuda : ' 
    pass

def p_f_call_a(p):
    'f_call : ID "(" expression f_call_ayuda ")" ";"'
    p[0] = (p[1], "(", p[3], p[4], ")", ";")

def p_f_call_b(p):
    'f_call : ID "(" ")" ";"'
    p[0] = (p[1], "(", ")", ";")
    
def p_f_call_ayuda_a(p):
    'f_call_ayuda : "," expression f_call_ayuda'
    p[0] = (",", p[2],p[3])
    
def p_f_call_ayuda_b(p):
    'f_call_ayuda : '
    pass

def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")
    
    
parser = yacc.yacc()

# Creamos la función para el parser
def parser_table(lineas):
    codigo_texto = ""
    for linea in lineas:
        for token in linea:
            codigo_texto += token + " "
        codigo_texto += "\n"
    #print(codigo_texto)
    parser.parse(codigo_texto)
    
'''result = parser.parse()            
print(result)
print(names)'''

#Función para la lectura del listado de casos de prueba
for caso in documento:
    num_caso += 1 
    with open(caso, 'r') as file:
        codigo = file.read()
    print(f'Caso {num_caso}: {caso}')
    # Pasar el contenido completo a las funciones del lexer
    m.tabla(codigo)
    
    # Creamos la lista de parsers 
    lineas = MyLexer.lineas_parser
    parser_table(lineas)
    #parser.parse(MyLexer.lineas_parser)
    # Limpiar la tabla de símbolos, para el siguiente caso.
    m.clear_table()
    
    # Limpiar las lineas de tokens que se mandaron al parser.
    MyLexer.lineas_parser = []
    print("\n")


'''# Creamos el parser 
parser = yacc.yacc()

while True:
    try:
        s = input ('sopa de macaco')'''
print(tokens)