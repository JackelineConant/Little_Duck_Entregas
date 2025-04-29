import ply.lex as lex

class MyLexer(object):
    
    def __init__(self):
        self.symbol_table = {}

    #Especificamos las palabras reservadas que utiliza nuestro lexer
    reserved = {
       'if' : 'IF',
       'then' : 'THEN',
       'else' : 'ELSE',
       'while' : 'WHILE',
       'print' : 'PRINT',
       'for' : 'FOR',
       'program' : 'PROGRAM',
       'main' : 'MAIN',
       'end' : 'END',
       'void' : 'VOID',
       'do' : 'DO',
       'var' : 'VAR',
       'int' : 'INT',
       'float' : 'FLOAT',
       'string': 'STRING'
    }
    
    #se definen literales que ply puede definir con la variable literals
    literals = ['+','-','*','=', ',', ':',';','/','>','<','(',')','{','}','[',']']

    # Lista de los tokens que se utilizan mas la lista de palabras reservadas
    tokens = ['CONST_INT', 'CONST_FLOAT', 'CONST_STRING', 'ID', 'EQ', 'GE', 'LE', 'NE'] + list(reserved.values())

    # Se definen las expreciones regulares de los tokens utilizados
    t_EQ = r'=='
    t_GE = r'>='
    t_LE = r'<='
    t_NE = r'!='
    t_ignore = ' \t'
    
    #token de float, se convierte el valor a un dato de tipo float
    @staticmethod
    def t_FLOAT(t):
        r'[0-9]+\.[0-9]+'
        t.value = float(t.value)
        return t

    #token de int, se convierte el valor a un dato de tipo int
    @staticmethod
    def t_CONST_INT(t):
        r'[0-9]+'
        t.value = int(t.value)
        return t
    
    #token de string
    @staticmethod
    def t_CONST_STRING(t):
        r'"([^\\"]|\\.)*"|\'([^\\\']|\\.)*\''
        t.value = t.value[1:-1]
        return t
    
    #token de ID, se evalua que no sea una palabra reservada 
    @staticmethod
    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = MyLexer.reserved.get(t.value, 'ID')
        return t

    #token para el salto de linea
    @staticmethod
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    #token de comentario, cuando encuntra un # ignora lo que se contenga en la linea
    @staticmethod
    def t_COMMENT(t):
        r'\#.*'
        pass
    
    #Manejo de errores en caso de que se encuentre un caracter que no sea parte de los tokens especificados
    @staticmethod
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
    # funcion para inicializar el lexer  o analizador de lexico
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    #La tabla de simbolos  que guarda el valor la calve, las lineas donde se encunetra el simbolo y sus pociones
    def table_symbols(self, nombre_var, valor, clave, linea, pos):
        if nombre_var in self.symbol_table:
            self.symbol_table[nombre_var]['lineas'].append(linea)
            self.symbol_table[nombre_var]['lugares'].append(pos)
        else:
            self.symbol_table[nombre_var] = {
                'valor': valor,
                'clave': clave,
                'lineas': [linea],
                'lugares': [pos]
            }
     # funcion para imprimir los resultados de lexer
    def tabla(self, data):
        for line_number, line in enumerate(data.splitlines(), start=1):
            if line.strip() == "":
                continue
            print(f"\nLine {line_number}: {line}")
            self.lexer.input(line)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                print(f"  Type: {tok.type} | Value: {tok.value} | lexpos: {tok.lexpos}")
                if tok.type == 'ID':
                    self.table_symbols(tok.value, None, tok.type, line_number, tok.lexpos)

        # Mostrar tabla de símbolos
        print("\nTabla de Símbolos:")
        print("{:<15} {:<10} {:<20} {:<20}".format("Nombre", "Tipo", "Líneas", "Posiciones"))
        for nombre, info in self.symbol_table.items():
            print("{:<15} {:<10} {:<20} {:<20}".format(
                nombre, info['clave'], str(info['lineas']), str(info['lugares'])
            ))
    # función para depurar la tabla de símbolos por cada caso
    def clear_table(self):
        self.symbol_table = {}

m = MyLexer() #crea una instancia del lexer
m.build()      # Construye el lexer 

documento = ['conversion_metros_yardas.ld','celsius_to_fahrenheit.ld','serie_fibonnacci.ld','mayor_valor.ld']
num_caso = 0
for caso in documento:
    num_caso += 1
    with open(caso, 'r') as file:
        codigo = file.read()
    print(f'Caso {num_caso}: {caso}')
    # Pasar el contenido completo a las funciones del lexer
    m.tabla(codigo)
    m.clear_table()
    print("\n")


