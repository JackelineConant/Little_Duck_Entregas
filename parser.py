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
names = { }

def p_program(p):
    'program : PROGRAM ID ";"'
    pass

def p_factor(p):
    'factor : CONST_INT'
    p[0] = p[1]

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


'''# Creamos el parser 
parser = yacc.yacc()

while True:
    try:
        s = input ('sopa de macaco')'''
#print(tokens)