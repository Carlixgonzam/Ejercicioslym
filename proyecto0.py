#Aca determinamos todas las reglas gramaticales que se tienen que tener en cuenta
#Se habilitan las reglas gramaticales para el lenguaje de programación de robots

GRAMMAR_RULES = {
    "program": ["definitions instructions"],
    "definitions": ["variables | procedures"],
    "variables": ["'|' variable_list '|'"],
    "variable_list": ["identifier ',' variable_list", "identifier"],
    "procedures": ["procedure procedures", "ε"],
    "procedure": ["'proc' identifier parameter_list '[' block ']'"],
    "parameter_list": ["':' identifier param_list", "ε"],
    "param_list": ["'and' identifier ':' identifier param_list", "ε"],
    "block": ["instruction block", "ε"],
    "instructions": ["instruction instructions", "ε"],
    "instruction": ["command", "assignment", "conditional", "loop", "procedure_call"],
    "command": ["'move:' number 'inDir:' direction '.'", "'turn:' direction '.'", "'put:' identifier 'ofType:' object_type '.'", "'pick:' identifier 'ofType:' object_type '.'", "'goTo:' number 'with:' number '.'", "'nop.'"],
    "assignment": ["identifier ':=' expression '.'"],
    "expression": ["number", "identifier"],
    "conditional": ["'if:' condition 'then:' '[' block ']' 'else:' '[' block ']'"],
    "condition": ["'facing:' direction", "'canMove:' number 'inDir:' direction", "'canPut:' number 'ofType:' object_type", "'canPick:' number 'ofType:' object_type", "'not:' condition"],
    "loop": ["'while:' condition 'do:' '[' block ']'"],
    "procedure_call": ["identifier argument_list '.'"],
    "argument_list": ["':' expression argument_list", "ε"],
    "object_type": ["'#chips'", "'#balloons'"],
    "direction": ["'#north'", "'#south'", "'#west'", "'#east'"],
    "number": ["[0-9]+"],
    "identifier": ["[a-zA-Z_][a-zA-Z0-9_]*"]
}

#En esta parte sw definen las funciones que se van a utilizar para el análisis sintatico

def tokenize_robot_language(code):
    tokens = []
    i = 0
    while i < len(code):
        char = code[i]
        
        if char.isspace():
            i += 1
        elif char.isalpha() or char == '_':
            start = i
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                i += 1
            token_value = code[start:i]
            token_type = 'KEYWORD' if token_value in {'proc', 'if:', 'else:', 'while:', 'repeatTimes:'} else 'IDENTIFIER'
            tokens.append((token_value, token_type))
        elif char.isdigit():
            start = i
            while i < len(code) and code[i].isdigit():
                i += 1
            tokens.append((code[start:i], 'NUMBER'))
        elif char in {':', '.', '|', '(', ')', '[', ']'}:
            tokens.append((char, 'SYMBOL'))
            i += 1
        elif char == '#':
            start = i
            i += 1
            while i < len(code) and code[i].isalpha():
                i += 1
            tokens.append((code[start:i], 'CONSTANT'))
        else:
            print(f"Error: Carácter inesperado '{char}'")
            return None
    
    return tokens

#En esta parte se define la funcion que se va a utilizar para el analisis sintatico
def parse_program(tokens):
    root = {"Program": []}
    while tokens:
        token, token_type = tokens.pop(0)
        if token_type == 'KEYWORD' and token == 'proc':
            root["Program"].append(parse_procedure(tokens))
        elif token_type == 'KEYWORD' and token in {'if:', 'while:', 'repeatTimes:'}:
            root["Program"].append(parse_conditional(tokens, token))
        else:
            root["Program"].append(parse_instruction(token, tokens))
    return root, True

#En esta parte se definen las funciones que se van a utiliza

def parse_procedure(tokens):
    proc_name = tokens.pop(0)[0]
    tokens.pop(0)  # "["
    body = []
    while tokens and tokens[0][0] != "]":
        body.append(parse_instruction(tokens.pop(0)[0], tokens))
    tokens.pop(0)  # "]"
    return {"Procedure": {"name": proc_name, "body": body}}

def parse_instruction(token, tokens):
    instr_node = {"Instruction": token, "Parameters": []}
    while tokens and tokens[0][1] in {'NUMBER', 'CONSTANT', 'IDENTIFIER'}:
        instr_node["Parameters"].append(tokens.pop(0)[0])
    return instr_node

#Los condiciones se definen en esta parte 

def parse_conditional(tokens, cond_type):
    condition = tokens.pop(0)[0]
    body = []
    if tokens and tokens[0][0] == 'then:':
        tokens.pop(0)
        body.append(parse_instruction(tokens.pop(0)[0], tokens))
    if tokens and tokens[0][0] == 'else:':
        tokens.pop(0)
        body.append(parse_instruction(tokens.pop(0)[0], tokens))
    return {"Conditional": {"type": cond_type, "condition": condition, "body": body}}

#Se plantea un ejemplo de código de robot para probar el analizador sintático
robot_code = """
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
#Se llama a las funciones para que se ejecute el analizador sintático
tokens = tokenize_robot_language(robot_code)
if tokens:
    parse_tree, is_valid = parse_program(tokens)
    print("Árbol Sintáctico:", parse_tree)
    print("Pertenece al lenguaje:", is_valid)
