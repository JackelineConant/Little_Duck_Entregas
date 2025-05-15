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

# Program
def p_program(p):
    'program : PROGRAM ID ";" vars funcs MAIN body END'
    p[0] = (p[1], p[2], ";", p[4], p[5], p[6], p[7], p[8])

# Vars
def p_vars_multiple(p):
    'vars : vars VAR var_ayuda'
    p[0] = p[1] + [(p[2], p[3])]

def p_vars_single(p):
    'vars : VAR var_ayuda'
    p[0] = [(p[1], p[2])]

def p_var_ayuda(p):
    'var_ayuda : ID var_doble_ayuda ":" type ";" var_ayuda_tail'
    p[0] = (p[1], p[2], ":", p[4], ";", p[6])

def p_var_ayuda_tail(p):
    'var_ayuda_tail : var_ayuda'
    p[0] = p[1]

def p_var_ayuda_tail_empty(p):
    'var_ayuda_tail :'
    p[0] = []

def p_var_doble_ayuda(p):
    'var_doble_ayuda : "," ID var_doble_ayuda'
    p[0] = (",", p[2], p[3])

def p_var_doble_ayuda_empty(p):
    'var_doble_ayuda :'
    p[0] = []

# Type
def p_type_int(p):
    'type : INT'
    p[0] = p[1]

def p_type_float(p):
    'type : FLOAT'
    p[0] = p[1]

# body
def p_body(p):
    'body : "{" statements "}"'
    p[0] = ("{", p[2], "}")

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

# Print
def p_print_expr(p):
    'print : PRINT "(" expression print_ayuda ")" ";"'
    p[0] = (p[1], "(", p[3], p[4], ")", ";")

def p_print_string(p):
    'print : PRINT "(" STRING print_ayuda ")" ";"'
    p[0] = (p[1], "(", p[3], p[4], ")", ";")

def p_print_ayuda_expr(p):
    'print_ayuda : "," expression print_ayuda'
    p[0] = (",", p[2], p[3])

def p_print_ayuda_string(p):
    'print_ayuda : "," STRING print_ayuda'
    p[0] = (",", p[2], p[3])

def p_print_ayuda_empty(p):
    'print_ayuda :'
    p[0] = []

# Cycle
def p_cycle(p):
    'cycle : DO body WHILE "(" expression ")" ";"'
    p[0] = (p[1], p[2], p[3], "(", p[5], ")", ";")

# Condition
def p_condition_if(p):
    'condition : IF "(" expression ")" body ";"'
    p[0] = (p[1], "(", p[3], ")", p[5], ";")

def p_condition_if_else(p):
    'condition : IF "(" expression ")" body ELSE body ";"'
    p[0] = (p[1], "(", p[3], ")", p[5], p[6], p[7], ";")

# Assign
def p_assign(p):
    'assign : ID "=" expression ";"'
    p[0] = (p[1], "=", p[3], ";")

# expresión
def p_expression_gt(p):
    'expression : exp ">" exp'
    p[0] = (p[1], ">", p[3])

def p_expression_lt(p):
    'expression : exp "<" exp'
    p[0] = (p[1], "<", p[3])

def p_expression_eq(p):
    'expression : exp EQ exp'
    p[0] = (p[1], "==", p[3])

def p_expression_ge(p):
    'expression : exp GE exp'
    p[0] = (p[1], ">=", p[3])

def p_expression_le(p):
    'expression : exp LE exp'
    p[0] = (p[1], "<=", p[3])

def p_expression_ne(p):
    'expression : exp NE exp'
    p[0] = (p[1], "!=", p[3])

def p_expression_exp(p):
    'expression : exp'
    p[0] = p[1]

# exp
def p_exp_add(p):
    'exp : exp "+" termino'
    p[0] = (p[1], "+", p[3])

def p_exp_sub(p):
    'exp : exp "-" termino'
    p[0] = (p[1], "-", p[3])

def p_exp_term(p):
    'exp : termino'
    p[0] = p[1]

def p_termino_mul(p):
    'termino : termino "*" factor'
    p[0] = (p[1], "*", p[3])

def p_termino_div(p):
    'termino : termino "/" factor'
    p[0] = (p[1], "/", p[3])

def p_termino_factor(p):
    'termino : factor'
    p[0] = p[1]

# factor
def p_factor_group(p):
    'factor : "(" expression ")"'
    p[0] = ("(", p[2], ")")

def p_factor_id(p):
    'factor : ID'
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

# cte
def p_cte_int(p):
    'cte : INT'
    p[0] = p[1]

def p_cte_float(p):
    'cte : FLOAT'
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
    'funcs :'
    p[0] = []

def p_funcs_ayuda(p):
    'funcs_ayuda : "," ID ":" type funcs_ayuda'
    p[0] = (",", p[2], ":", p[4], p[5])

def p_funcs_ayuda_empty(p):
    'funcs_ayuda :'
    p[0] = []

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
    'f_call_ayuda :'
    p[0] = []

# error
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
    print(codigo_texto)
    parser.parse(codigo_texto)
    


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


#print(tokens)