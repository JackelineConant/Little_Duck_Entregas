import ply.yacc as yacc
from ply_tokenizer import MyLexer

start = 'program'
tokens = MyLexer.tokens
literals = MyLexer.literals

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value '{p.value}', line {p.lineno}")
        raise SyntaxError(...)
    
def p_assign(p):
    'assign : ID "=" expresion ";"'
    p[0] = ('assign', p[1], p[3])

def p_expresion(p):
    '''expresion : exp
                | exp ">" exp
                | exp "<" exp
                | exp EQ exp
                | exp GE exp
                | exp LE exp
                | exp NE exp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('relop', p[2], p[1], p[3])
            
def p_exp(p):
    '''exp : termino
            | exp "+" termino
            | exp "-" termino'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])
            
def p_termino(p):
    '''termino : factor
            | termino "*" factor
            | termino "/" factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])
            
def p_factor(p):
    '''factor : "(" expresion ")"
                | signo atomo'''
    if len(p) == 4:  # ( expresion )
        p[0] = p[2]
    else:
        signo = p[1]
        valor = p[2]
        if signo == '-':
            p[0] = -valor
        else:
            p[0] = valor
    
def p_atomo(p):
    '''atomo : ID
            | cte'''
    p[0] = p[1]

def p_cte(p):
    '''cte : CONST_INT
            | CONST_FLOAT'''
    p[0] = p[1]
    
def p_signo(p):
    '''signo : "+"
            | "-"
            | empty'''
    p[0] = p[1]
    
def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]
    
def p_cycle(p):
    'cycle : WHILE "(" expresion ")" DO body ";"'
    p[0] = ('cycle', p[2], p[5])
    
def p_condition(p):
    '''condition : IF "(" expresion ")" body ";"
                | IF "(" expresion ")" body ELSE body ";"'''
    if len(p) == 7:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])
    
def p_var(p):
    'var : VAR var_prime'
    p[0] = p[2]

def p_var_prime(p):
    '''var_prime : id_list ":" type ";"
                | id_list ":" type ";" var_prime'''
    decls = [('var_decl', var, p[3]) for var in p[1]]
    if len(p) == 5:
        p[0] = decls
    else:
        p[0] = decls + p[5]
        
def p_id_list(p):
    '''id_list : ID
               | ID "," id_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_statment(p):
    '''statment : assign
                | condition
                | cycle
                | f_call
                | print'''
    p[0] = p[1]
    
def p_body(p):
    'body : "{" body_state "}"'
    p[0] = p[2]

def p_body_state(p):
    '''body_state : statment 
                | statment body_state
                | empty'''
    if len(p) == 2:  
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]
        
def p_program(p):
    'program : PROGRAM ID ";" vars program_funcs MAIN body END'
    p[0] = ('program', p[2], p[4], p[5], p[7])

def p_vars(p):
    '''vars : var
                    | empty'''
    p[0] = p[1]

def p_program_funcs(p):
    '''program_funcs : funcs 
                    | funcs program_funcs
                    | empty'''
    if len(p) == 2:  
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_funcs(p):
    'funcs : VOID ID "(" funcs_prime ")" "[" vars body "]" ";"'
    p[0] = ('funcs', p[2], p[4], p[7], p[8])
    
def p_funcs_prime(p):
    '''funcs_prime : ID ":" type
                    | ID ":" type "," funcs_prime
                    | empty'''
    if len(p) == 2:  
        p[0] = []
    elif len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = [(p[1], p[3])] + p[5]

def p_f_call(p):
    'f_call : ID "(" f_call_prime ")" ";"'
    p[0] = ('f_call', p[1], p[3])

def p_f_call_prime(p):
    '''f_call_prime : expresion
                    | expresion "," f_call_prime
                    | empty'''
    if len(p) == 2:  
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
    
def p_print(p):
    'print : PRINT "(" print_prime ")" ";"'
    p[0] = ('print', p[3])

def p_print_prime(p):
    '''print_prime : print_item
                   | print_item "," print_prime'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_print_item(p):
    '''print_item : expresion
                  | CONST_STRING'''
    p[0] = p[1]


#inicializar lexer
lexer = MyLexer()
lexer.build()

parser = yacc.yacc()
    
with open("test_parser.txt", "r") as file:
    data = file.read()

try:
    result = parser.parse(data, lexer=lexer.lexer)
    print(result)
except SyntaxError as e:
    print(e)
