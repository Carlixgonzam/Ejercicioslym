REGLAS_GRAMATICA = {
    "program": ["{definitiones} {instrucciones}"],
    "definitiones": ["{variables} | {procedimientos}"],  # Variables y procedimientos como bloques
    "variables": ["'|' {variable_lista} '|'"],  # bloque de var
    "variable_lista": ["{id} ',' variable_lista", "{id}"],
    "procedimientos": ["{procedimiento} procedimientos", "#lambda?"],
    "procedimiento": ["'proc' {id} param_lista '[' {bloque} ']'"],
    # "parameter_list": ["':' {id} param_lista"],
    "param_lista": ["'and' | ':' {id} ':' {id} param_lista", "{bloque}"],
    "bloque": ["{instruccion} {bloque}", "#lambda?"],
    "instrucciones": ["{instruccion} instrucciones | #que puedo poner lambda?"],
    "instruccion": ["comando","asignar","condicional","ciclo","{llamada_procedimiento}",],
    "comando": [
        "'move:' {number} 'inDir:' {direccion} '.'",
        "'turn:' {direccion} '.'",
        "'put:' {id} 'ofType:' {objeto_tipo} '.'",
        "'pick:' {id} 'ofType:' {objeto_tipo} '.'",
        "'goTo:' {number} 'with:' {number} '.'",
        "'nop.'",],
    "asignar": ["{id} ':=' expre '.'"],
    "expre": ["{number}", "id"],
    "condicional": [ "'if:' {condicion} 'then:' '[' {bloque} ']' 'else:' '[' {bloque} ']'"],
    "condicion": [
        "'facing:' {direccion}",
        "'canMove:' {number} 'inDir:' {direccion}",
        "'canPut:' {number} 'ofType:' {objeto_tipo}",
        "'canPick:' {number} 'ofType:' {objeto_tipo}","'not:' {condicion}",],
    "ciclo": ["'while:' {condicion} 'do:' '[' {bloque} ']'"],
    "llamada_procedimiento": ["{id} {argument_lista} '.'"],
    "argument_lista": ["':' expre {argument_lista}", "{bloque}"],
    "objeto_tipo": ["'#chips'", "'#balloons'"],
    "direccion": ["'#north'", "'#south'", "'#west'", "'#east'"],
    "number": ["[0-9]+"],
    "id": ["[a-zA-Z_][a-zA-Z0-9_]*"],
}

#corregir esta funcion del arbol
#validacioens usarlas funciones dentro del arbol
#Podemos hacer la lectura de los strings 
#Podemos revisar tambien de manera recursiva los valores 
#Tambien considerar corregir el arbol de tal manera que el problema solo sea sintaxis
#considero semantica?
#Funciones con valor y luego definir esos valores
#Podemos implementar busquedas inorder para determinar los strings
#Se puede analizar el string de manera que pueda leer todo hasta el ]


def nodos_arbol(caracter):

    seti = set()
    for i in caracter:
        valor = parseo(caracter)
        seti.add(valor)

    return seti


def parseo(cadena):
    cadena_guarda = ()
    for i in cadena:
        if cadena[i] == "[":
            funcion = analizar_procedimiento(cadena[i])
            cadena_guarda.__add__(funcion)
        else:
            return False


    return cadena_guarda

def parseo_constant(cadena):
    for i in range(cadena):
        if cadena[i] == analizar_instruccion:
            const = cadena[i]
    return const
def ana_proc(cadena):
    cadena_guarda = {}
    while "[" == True:
        if cadena in cadena_guarda:
            continue
        else:
            return False
    return cadena_guarda

def obtener(codigo):
    lista = []
    i = 0
    while i < len(codigo):
        char = codigo[i]
        if char == " " or char == "\n" or char == "\t":
            i += 1
        elif (
            (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
            or char == "_"):
            inicio = i
            while i < len(codigo) and (
                (codigo[i] >= "a" and codigo[i] <= "z")
                or (codigo[i] >= "A" and codigo[i] <= "Z")
                or (codigo[i] >= "0" and codigo[i] <= "9")
                or codigo[i] == "_"):
                i += 1
            valor = codigo[inicio:i]
            tipo = "PALABRA_RESERVADA"
            if valor in {"proc", "if:", "else:", "while:", "repeatTimes:"}:
                tipo = "PALABRA_RESERVADA"
            else:
                "IDENTIFICADOR"
            lista.append((valor, tipo))
        elif char >= "0" and char <= "9":
            inicio = i
            while i < len(codigo) and (codigo[i] >= "0" and codigo[i] <= "9"):
                i += 1
            lista.append((codigo[inicio:i], "NUMERO"))
        elif char in {":", ".", "|", "(", ")", "[", "]"}:
            lista.append((char, "SIMBOLO"))
            i += 1
        elif char == "#":
            inicio = i
            i += 1
            while i < len(codigo) and (
                (codigo[i] >= "a" and codigo[i] <= "z")
                or (codigo[i] >= "A" and codigo[i] <= "Z")
            ):
                i += 1
            lista.append((codigo[inicio:i], "CONSTANTE"))
        else:
            print("Erroooooor '{char}'")
            return None
        

    return lista


# parse
def analizar_programa(lista):
    arbol_sintactico = {"Program": []}
    while lista:
        car, tipo = lista.pop(0)
        if tipo == "PALABRA_RESERVADA" and car == "proc":
            arbol_sintactico["Program"].append(analizar_procedimiento(lista))
        elif tipo == "PALABRA_RESERVADA" and car in {"if:", "while:", "repeatTimes:"}:
            arbol_sintactico["Program"].append(analizar_condicional(lista, car))
        else:
            arbol_sintactico["Program"].append(analizar_instruccion(car, lista))
    return arbol_sintactico, True


# definición de un procedimiento
def analizar_procedimiento(lista):
    nombre_proc = lista.pop(0)[0]
    lista.pop(0)
    cuerpo = []
    while lista and lista[0][0] != "]":
        cuerpo.append(analizar_instruccion(lista.pop(0)[0], lista))
    lista.pop(0)
    return {"Procedimiento": {"nombre": nombre_proc, "cuerpo": cuerpo}}


# instrucción simple
def analizar_instruccion(punto, lista):
    nodoinstruccion = {"Instruccion": punto, "Parametros": []}
    while lista and lista[0][1] in {"NUMERO", "CONSTANTE", "IDENTIFICADOR"}:
        nodoinstruccion["Parametros"].append(lista.pop(0)[0])
    return nodoinstruccion


def analizar_condicional(lista, tipo_condicional):
    condicion = lista.pop(0)[0]
    bloques = []
    while lista and lista[0][0] != "]":
        bloques.append(analizar_instruccion(lista.pop(0)[0], lista))
    if lista and lista[0][0] == "else:":
        lista.pop(0)
        bloques.append(analizar_instruccion(lista.pop(0)[0], lista))
    return {
        "Condicional": {
            "tipo": tipo_condicional,
            "condicion": condicion,
            "bloques": bloques,
        }
    }

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


t = obtener(codigo_robot)
if t:
    arbol, valido = analizar_programa(t)
    print("Árbol Sintáctico:", arbol)
    print("Pertenece al lenguaje:", valido)
