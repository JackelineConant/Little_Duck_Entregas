import ply.lex as lex

# El código original le pertenece a la profesora Valentina
# Alumno: Jackeline Conant Rubalcava Matrícula: A01280544
# Yó como alumno edité este código para adaptarlo a lo especificado en el canvas


# Crear un diccionario para almacenar los valores de la lista:
table_of_symbols = {}

#Lista de palabras reservadas
reserved = {
    'print' : 'PRINT',
    'if' : 'IF',
    'elseif' : 'ELSEIF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'len' : 'LEN',
    'from' : 'FROM',
    'or' : 'OR',
    'def' : 'DEF',
    'None' : 'NONE',
    'break' : 'BREAK',
    'return' : 'RETURN',
    'input' : 'INPUT',
    'program' : 'PROGRAM',
    'int' : 'INT'
}

#Lista de delimitadores 
delimitadores = {'{' : 'L_DEL_BRACE',
                 '}' : 'R_DEL_BRACE',
                 '(' : 'L_DEL_PAREN',
                 ')' : 'R_DEL_PAREN',
                 '[' : 'L_DEL_BRACKET',
                 ']' : 'R_DEL_BRACKET'} 


# Lista con nombres de tokens
# Siempre debe existir
tokens = [
    'CONST_INT',
    'IDENTIFIER',
    'CONST_STRING',
    'OP_ASIGNA',
    'OP_IGUAL',
    'SEMICOL',
    'COMMENT',
    'OP_SUMA',
    'OP_RESTA',
    'OP_MULTIPLY',
    'OP_DIVISION',
    'TRIPLE_COMMENT',
    'F_STRING',
    'TWO_DOTS'
] + list(reserved.values()) + list(delimitadores.values())
#Se le tiene que agregar la lista de palabras reservadas 

# Los tokens simples tienen solo una expresion regular
# Se asignan en variables que inician con t_
# Deben coincidir con lo definido en la lista tokens

# Lista de operadores aritméticos 
t_OP_ASIGNA = r'='
t_OP_IGUAL = r'=='
t_SEMICOL  = r';'
t_OP_SUMA = r'\+'
t_OP_RESTA = r'\-'
t_OP_MULTIPLY = r'\*'
t_OP_DIVISION = r'\/'
t_TWO_DOTS = r':'

# Los tokens que requieran alguna accion adicional, se definen en funciones
# La primer linea es la expresion regular del token
# Luego, van las acciones, por ejemplo, convertir cadenas en enteros
def t_CONST_INT (t):
    r'[0-9]+'
    t.value = int(t.value)  
    return t

#Función de valores f string
def t_F_STRING(t):
    r'f"([a-zA-Z_][a-zA-Z0-9_]*)"'
    return t

# Función de valores string 
def t_CONST_STRING(t):
    r'"([^"]*)"' 
    return t

#
def t_IDENTIFIER (t):
    r'[a-zA-Z]\w*\b'
    t.type = reserved.get(t.value,'IDENTIFIER') 
    # Aqui, el identificador puede ir a la tabla de simbolos (for later)   
    # Además se agrega lo que es mis palabras reservadas a esta función identificadora, para que no las interprete como identificadores 
    return t

def t_DELIMITADORES(t): 
    r'[\{\}\(\)\[\]]' 
    t.type = delimitadores[t.value] 
    return t 

# Numeros de linea, espacios y errores:  no son parte de tokens
# Numeros de linea. 
# Hay un contador dentro la clase, aqui se incrementa
def t_newline (t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_COMMENT(t):
    r'\#.*'
    return t

def t_TRIPLE_COMMENT(t):
    r'\""".*"""'
    return t

# Esto especifica que simbolos se ignoran, tipicamente espacios y tabs
t_ignore  = ' \t'

# Muestra errores y sigue avanzando (con skip)
def t_error (t):
    print("Unknown symbol '%s'!!" % t.value[0])
    t.lexer.skip(1)
    


# Construye el objeto lexer
# La libreria 'sabe' que debe usar las funciones y variables que definimos arriba
lexer = lex.lex()
count = 0




#Entrada 
with open('fahrenheit_celsius.ld') as f:
  input_program = [line.strip() for line in f.readlines()]
  
for i in range(len(input_program)):
    count = i+1
    print(f"Línea {i+1}: {str(input_program[i])}")
    lexer.input(input_program[i])
    
    # Lexer
    # la funcion lexer() del modulo devuelve el siguiente token, va de una linea en una linea
    while True:
        tok = lexer.token()
        if not tok: # Aqui se acabo
            break      
        #print(tok)
        print(f"{tok.type}  value: {tok.value}  lexpos: {tok.lexpos}") # Imprime el objeto
        # Creamos este mounstro que puede ser optimizado, pero por causas del tiempo se quedará así.
        if tok.type in reserved.values():
            if tok.value not in table_of_symbols:
                table_of_symbols[tok.value] = {
                    'type': 'PALABRAS_RESERVADAS', 
                    'value': tok.value, 
                    'line': count, 
                    'position': tok.lexpos+1   # Posición en el archivo fuente
                }
        elif tok.type in delimitadores.values():
            if tok.value not in table_of_symbols:
                table_of_symbols[tok.value] = {
                    'type': 'DELIMITADORES', 
                    'value': tok.value, 
                    'line': count,  
                    'position': tok.lexpos+1   # Posición en el archivo fuente
                }
        
        else:
            if tok.value not in table_of_symbols:
                table_of_symbols[tok.value] = {
                    'type': tok.type, 
                    'value': tok.value, 
                    'line': count, 
                    'position': tok.lexpos+1   # Posición en el archivo fuente
                }
        
        
    print("\n")

        # O accede a sus atributos
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)

#Imprimir la tabla de símbolos que fueron agregados por tipo, valor y posición
print("\nTabla de símbolos:")
for token, info in table_of_symbols.items():
    print(f"{info}")
