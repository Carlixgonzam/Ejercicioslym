def obtener_tokens(codigo):
    """
    Función simplificada para tokenizar el código.
    Separa palabras, números y algunos símbolos básicos.
    """
    tokens = []
    i = 0
    while i < len(codigo):
        char = codigo[i]
        if char.isspace():
            i += 1
            continue
        if char.isalpha() or char == '_':
            inicio = i
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                i += 1
            tokens.append(codigo[inicio:i])
        elif char.isdigit():
            inicio = i
            while i < len(codigo) and codigo[i].isdigit():
                i += 1
            tokens.append(codigo[inicio:i])
        elif char in {':', '.', '|', '[', ']'}:
            tokens.append(char)
            i += 1
        elif char == '#':
            inicio = i
            i += 1
            while i < len(codigo) and codigo[i].isalpha():
                i += 1
            tokens.append(codigo[inicio:i])
        else:
            print("Error: Carácter inesperado:", char)
            return None
    return tokens

def parse_programa(tokens):
    """
    Función principal de análisis sintáctico.
    Recorre la lista de tokens y crea un árbol sintáctico básico.
    Retorna el AST y un booleano que indica si el código es válido.
    """
    ast = {"programa": []}
    pos = 0
    valido = True
    while pos < len(tokens):
        if tokens[pos] == "proc":
            nodo, pos, valido_local = parse_procedimiento(tokens, pos)
            if not valido_local:
                valido = False
            ast["programa"].append(nodo)
        else:
            nodo, pos, valido_local = parse_instruccion(tokens, pos)
            if not valido_local:
                valido = False
            ast["programa"].append(nodo)
    return ast, valido

def parse_procedimiento(tokens, pos):
    """
    Analiza una definición de procedimiento.
    Se espera el formato: proc <nombre> [ ...instrucciones... ]
    """
    nodo_proc = {"procedimiento": {}}
    # Se asume que tokens[pos] == "proc"
    pos += 1  # Saltamos "proc"
    if pos >= len(tokens):
        print("Error: se esperaba el nombre del procedimiento.")
        return None, pos, False
    nodo_proc["procedimiento"]["nombre"] = tokens[pos]
    pos += 1

    # Se espera que el bloque de instrucciones esté entre '[' y ']'
    if pos >= len(tokens) or tokens[pos] != '[':
        print("Error: se esperaba '[' para iniciar el bloque del procedimiento.")
        return None, pos, False
    pos += 1  # Saltamos '['

    instrucciones = []
    while pos < len(tokens) and tokens[pos] != ']':
        instr, pos, valido_local = parse_instruccion(tokens, pos)
        if not valido_local:
            return None, pos, False
        instrucciones.append(instr)
    if pos >= len(tokens) or tokens[pos] != ']':
        print("Error: se esperaba ']' para cerrar el bloque del procedimiento.")
        return None, pos, False
    pos += 1  # Saltamos ']'

    nodo_proc["procedimiento"]["cuerpo"] = instrucciones
    return nodo_proc, pos, True

def parse_instruccion(tokens, pos):
    """
    Analiza una instrucción.
    Se considera que una instrucción termina al encontrar el símbolo '.'.
    """
    nodo_instr = {"instruccion": []}
    while pos < len(tokens) and tokens[pos] != '.':
        nodo_instr["instruccion"].append(tokens[pos])
        pos += 1
    if pos < len(tokens) and tokens[pos] == '.':
        pos += 1  # Saltamos el '.'
        return nodo_instr, pos, True
    else:
        print("Error: se esperaba '.' al final de la instrucción.")
        return None, pos, False

# Ejemplo simplificado de código del robot
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
    arbol_ast, es_valido = parse_programa(tokens)
    print("Árbol Sintáctico:", arbol_ast)
    if es_valido:
        print("Pertenece al lenguaje: Sí")
    else:
        print("Pertenece al lenguaje: No")