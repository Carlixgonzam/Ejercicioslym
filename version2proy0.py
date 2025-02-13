"""<programa> ::= <declaraciones> <procedimientos> <bloque_principal>

<declaraciones> ::= "|" <lista_variables> "|"
<lista_variables> ::= <variable> <lista_variables> | ε
<variable> ::= [a-z]+  # Identificadores en minúscula

<procedimientos> ::= <procedimiento> <procedimientos> | ε
<procedimiento> ::= "proc" <nombre_proc> "[" <bloque> "]"
<nombre_proc> ::= [a-z]+

<bloque_principal> ::= "[" <bloque> "]"
<bloque> ::= <instrucción> "." <bloque> | ε

<instrucción> ::= <asignación>
                | <movimiento>
                | <llamada_procedimiento>
                | <condicional>
                | <bucle>

<asignación> ::= <variable> ":=" <valor>
<valor> ::= <numero> | <variable>

<llamada_procedimiento> ::= <nombre_proc> "."

<movimiento> ::= "move:" <numero> | "goto:" <numero> "with:" <numero>

<condicional> ::= "if:" <condición> "then:" "[" <bloque> "]" "else:" "[" <bloque> "]"

<bucle> ::= "while:" <condición> "do:" "[" <bloque> "]"

<condición> ::= "facing:" <direccion>  | "canMove:" <numero> "inDir:" <direccion>
<direccion> ::= "#north" | "#south" | "#west" | "#east"""

# Lista de palabras clave del lenguaje
PALABRAS_CLAVE = [
    "proc",
    "if:",
    "then:",
    "else:",
    "while:",
    "do:",
    "move:",
    "goto:",
    "with:",
    ":=",
    ".",
    "[",
    "]",
]
CARACTERES_ESPECIALES = ["|", ".", "[", "]", ":=", ":"]


# Definición del nodo del Árbol Sintáctico (AST)
class NodoAST:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo  # Tipo de nodo (ej: "PROC", "IF", "WHILE")
        self.valor = valor  # Valor opcional (ej: nombre de variable, número)
        self.hijos = []  # Lista de nodos hijos

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def mostrar(self, nivel=0):
        print("  " * nivel + f"{self.tipo}: {self.valor}")
        for hijo in self.hijos:
            hijo.mostrar(nivel + 1)


# Función para dividir el código en tokens (Análisis Léxico)
def analizar_tokens(codigo):
    tokens = []
    i = 0
    while i < len(codigo):
        caracter = codigo[i]

        # Ignorar espacios y saltos de línea
        if caracter in " \n\t":
            i += 1
            continue

        # Detectar caracteres especiales
        if caracter in CARACTERES_ESPECIALES:
            if codigo[i : i + 2] == ":=":
                tokens.append(("ASIGNACION", ":="))
                i += 2
            else:
                tokens.append((caracter, caracter))
                i += 1
            continue

        # Detectar palabras clave, variables y constantes
        palabra = ""
        while i < len(codigo) and codigo[i] not in " \n\t|[].:":
            palabra += codigo[i]
            i += 1

        if palabra in PALABRAS_CLAVE:
            tokens.append((palabra, palabra))
        elif palabra.startswith("#"):  # Detectar constantes
            tokens.append(("CONSTANTE", palabra))
        elif palabra[0].isalpha():  # Detectar variables y nombres de procedimientos
            tokens.append(("IDENTIFICADOR", palabra))
        elif palabra.isdigit():  # Detectar números
            tokens.append(("NUMERO", palabra))
        else:
            return None, f"Error: Token no reconocido: {palabra}"

    return tokens, None  # Sin errores


# Función para analizar la estructura del código y construir el AST
def analizar_programa(tokens):
    indice = 0
    variables = set()
    procedimientos = {}

    def consumir(tipo_esperado):
        nonlocal indice
        if indice < len(tokens) and tokens[indice][0] == tipo_esperado:
            indice += 1
            return True
        return False

    def analizar_declaraciones():
        if not consumir("|"):
            return None, "Error: Se esperaba '|' para iniciar las variables"

        nodo_declaraciones = NodoAST("DECLARACIONES")
        while indice < len(tokens) and tokens[indice][0] == "IDENTIFICADOR":
            variables.add(tokens[indice][1])
            nodo_declaraciones.agregar_hijo(NodoAST("VARIABLE", tokens[indice][1]))
            indice += 1

        if not consumir("|"):
            return None, "Error: Se esperaba '|' para cerrar las variables"

        return nodo_declaraciones, None

    def analizar_procedimiento():
        if not consumir("proc"):
            return None, "Error: Se esperaba 'proc' para definir un procedimiento"

        if indice >= len(tokens) or tokens[indice][0] != "IDENTIFICADOR":
            return None, "Error: Falta el nombre del procedimiento"

        nombre_proc = tokens[indice][1]
        indice += 1

        if not consumir("["):
            return None, "Error: Se esperaba '[' para abrir el procedimiento"

        nodo_proc = NodoAST("PROC", nombre_proc)
        nodo_bloque, error = analizar_bloque()
        if error:
            return None, error
        nodo_proc.agregar_hijo(nodo_bloque)

        if not consumir("]"):
            return None, "Error: Se esperaba ']' para cerrar el procedimiento"

        procedimientos[nombre_proc] = nodo_proc
        return nodo_proc, None

    def analizar_bloque():
        nodo_bloque = NodoAST("BLOQUE")
        while indice < len(tokens) and tokens[indice][0] != "]":
            nodo_inst, error = analizar_instruccion()
            if error:
                return None, error
            nodo_bloque.agregar_hijo(nodo_inst)
            if not consumir("."):
                return None, "Error: Se esperaba '.' al final de la instrucción"
        return nodo_bloque, None

    def analizar_instruccion():
        if indice >= len(tokens):
            return None, "Error: Fin inesperado del programa"

        if tokens[indice][0] == "IDENTIFICADOR":
            return analizar_asignacion()
        elif tokens[indice][0] == "move:":
            return analizar_movimiento()
        elif tokens[indice][0] == "if:":
            return analizar_condicional()
        elif tokens[indice][0] == "while:":
            return analizar_bucle()
        return None, f"Error: Instrucción no válida '{tokens[indice][1]}'"

    def analizar_asignacion():
        nombre_var = tokens[indice][1]
        if nombre_var not in variables:
            return None, f"Error: Variable '{nombre_var}' no declarada"
        nodo = NodoAST("ASIGNACION", nombre_var)
        indice += 1
        if not consumir("ASIGNACION"):
            return None, "Error: Se esperaba ':=' en la asignación"
        nodo.agregar_hijo(NodoAST("VALOR", tokens[indice][1]))
        indice += 1
        return nodo, None

    def analizar_movimiento():
        nodo = NodoAST("MOVIMIENTO", tokens[indice][1])
        indice += 1
        if not consumir("NUMERO"):
            return None

    def analizar_condicional():
        pass

    def analizar_bucle():
        pass

    # Construcción del AST
    nodo_programa = NodoAST("PROGRAMA")

    nodo_declaraciones, error = analizar_declaraciones()
    if error:
        return None, error
    nodo_programa.agregar_hijo(nodo_declaraciones)

    while indice < len(tokens) and tokens[indice][0] == "proc":
        nodo_proc, error = analizar_procedimiento()
        if error:
            return None, error
        nodo_programa.agregar_hijo(nodo_proc)

    return nodo_programa, None  # Sin errores


# Función principal para ejecutar el parser
def main():
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

    tokens = analizar_tokens(codigo_robot)

    print("Tokens:", tokens)

    ast = analizar_programa(tokens)
    print("AST:", ast)

main()
