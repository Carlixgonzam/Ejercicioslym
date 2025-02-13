#Aca determinamos todas las reglas gramaticales que se tienen que tener en cuenta
#Se habilitan las reglas gramaticales para el lenguaje de programación de robots

# Se definen las reglas gramaticales del lenguaje del robot
REGLAS_GRAMATICA = {
    "program": ["definitiones instructiones"],
    "definitiones": ["variables | procedimientos"],
    "variables": ["'|' variable_list '|'"],
    "variable_lista": ["identificador ',' variable_lista", "identificador"],
    "procedimientos": ["procedimiento procedimientos", "ε"],
    "procedimiento": ["'proc' identificador parameter_list '[' bloque ']'"],
    "parameter_list": ["':' identificador param_list", "ε"],
    "param_list": ["'and' identificador ':' identificador param_list", "ε"],
    "bloque": ["instruccion bloque", "ε"],
    "instructiones": ["instruccion instructiones", "ε"],
    "instruccion": ["command", "assignment", "conditional", "loop", "procedure_call"],
    "command": ["'move:' number 'inDir:' direction '.'", "'turn:' direction '.'", "'put:' identificador 'ofType:' object_type '.'", "'pick:' identificador 'ofType:' object_type '.'", "'goTo:' number 'with:' number '.'", "'nop.'"],
    "assignment": ["identificador ':=' expression '.'"],
    "expression": ["number", "identificador"],
    "conditional": ["'if:' condition 'then:' '[' bloque ']' 'else:' '[' bloque ']'"],
    "condition": ["'facing:' direction", "'canMove:' number 'inDir:' direction", "'canPut:' number 'ofType:' object_type", "'canPick:' number 'ofType:' object_type", "'not:' condition"],
    "loop": ["'while:' condition 'do:' '[' bloque ']'"],
    "procedure_call": ["identificador argument_list '.'"],
    "argument_list": ["':' expression argument_list", "ε"],
    "objeto_tipo": ["'#chips'", "'#balloons'"],
    "direction": ["'#north'", "'#south'", "'#west'", "'#east'"],
    "number": ["[0-9]+"],
    "identificador": ["[a-zA-Z_][a-zA-Z0-9_]*"]
}

# Función para tokenizar el código del robot
def obtener_tokens(codigo):
    lista_tokens = []
    i = 0
    while i < len(codigo):
        char = codigo[i]
        
        if char.isspace():
            i += 1
        elif char.isalpha() or char == '_':
            inicio = i
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                i += 1
            valor_token = codigo[inicio:i]
            # Se consideran algunas palabras reservadas
            tipo_token = 'PALABRA_RESERVADA' if valor_token in {'proc', 'if:', 'else:', 'while:', 'repeatTimes:'} else 'IDENTIFICADOR'
            lista_tokens.append((valor_token, tipo_token))
        elif char.isdigit():
            inicio = i
            while i < len(codigo) and codigo[i].isdigit():
                i += 1
            lista_tokens.append((codigo[inicio:i], 'NUMERO'))
        elif char in {':', '.', '|', '(', ')', '[', ']'}:
            lista_tokens.append((char, 'SIMBOLO'))
            i += 1
        elif char == '#':
            inicio = i
            i += 1
            while i < len(codigo) and codigo[i].isalpha():
                i += 1
            lista_tokens.append((codigo[inicio:i], 'CONSTANTE'))
        else:
            print(f"Error: Carácter inesperado '{char}'")
            return None
    
    return lista_tokens

# Función principal para analizar (parsear) el programa
def analizar_programa(lista_tokens):
    arbol_sintactico = {"Programa": []}
    while lista_tokens:
        token, tipo = lista_tokens.pop(0)
        if tipo == 'PALABRA_RESERVADA' and token == 'proc':
            arbol_sintactico["Programa"].append(analizar_procedimiento(lista_tokens))
        elif tipo == 'PALABRA_RESERVADA' and token in {'if:', 'while:', 'repeatTimes:'}:
            arbol_sintactico["Programa"].append(analizar_condicional(lista_tokens, token))
        else:
            arbol_sintactico["Programa"].append(analizar_instruccion(token, lista_tokens))
    return arbol_sintactico, True

# Función para analizar la definición de un procedimiento
def analizar_procedimiento(lista_tokens):
    nombre_proc = lista_tokens.pop(0)[0]
    lista_tokens.pop(0)  # Se descarta el símbolo "[" que abre el cuerpo
    cuerpo = []
    while lista_tokens and lista_tokens[0][0] != "]":
        cuerpo.append(analizar_instruccion(lista_tokens.pop(0)[0], lista_tokens))
    lista_tokens.pop(0)  # Se descarta el símbolo "]" que cierra el cuerpo
    return {"Procedimiento": {"nombre": nombre_proc, "cuerpo": cuerpo}}

# Función para analizar una instrucción simple
def analizar_instruccion(token, lista_tokens):
    nodo_instruccion = {"Instruccion": token, "Parametros": []}
    while lista_tokens and lista_tokens[0][1] in {'NUMERO', 'CONSTANTE', 'IDENTIFICADOR'}:
        nodo_instruccion["Parametros"].append(lista_tokens.pop(0)[0])
    return nodo_instruccion

# Función para analizar estructuras condicionales (if)
def analizar_condicional(lista_tokens, tipo_condicional):
    condicion = lista_tokens.pop(0)[0]
    bloques = []
    if lista_tokens and lista_tokens[0][0] == 'then:':
        lista_tokens.pop(0)  # Se descarta el 'then:'
        bloques.append(analizar_instruccion(lista_tokens.pop(0)[0], lista_tokens))
    if lista_tokens and lista_tokens[0][0] == 'else:':
        lista_tokens.pop(0)  # Se descarta el 'else:'
        bloques.append(analizar_instruccion(lista_tokens.pop(0)[0], lista_tokens))
    return {"Condicional": {"tipo": tipo_condicional, "condicion": condicion, "bloques": bloques}}

# Ejemplo de código del robot para probar el analizador sintáctico
codigo_robot = """
|x y|
proc goNorth [ while: canMove: 1 inDir: #north do: [ move: 1 inDir: #north .] ]
move: 2 inDir: #east .
turn: #right .
face: #north .
jump: 3 toThe: #front .
nop .
repeatTimes: for: 5 repeat: [ move: 1 . ]
if: facing: #north then: [ move: 2 .] else: [ turn: #right . ]
"""

# Ejecución del análisis sintáctico
tokens = obtener_tokens(codigo_robot)
if tokens:
    arbol, valido = analizar_programa(tokens)
    print("Árbol Sintáctico:", arbol)
    print("Pertenece al lenguaje:", valido)