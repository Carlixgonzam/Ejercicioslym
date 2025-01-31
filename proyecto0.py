import re

def tokenize_robot_language(code):
    token_patterns = [
        (r'\b(proc|if:|else:|while:|repeatTimes:)\b', 'KEYWORD'),
        (r'\b(M|R|C|B|c|b|P);\b', 'COMMAND'),
        (r'\bJ\(\d+\);\b', 'COMMAND_JUMP'),
        (r'\bG\(\d+,\d+\);\b', 'COMMAND_GOTO'),
        (r'\|[a-z0-9 ]+\|', 'VARIABLE_DECLARATION'),
        (r'\b[a-z][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
        (r'#\w+', 'CONSTANT'),
        (r'\:=', 'ASSIGNMENT_OP'),
        (r'\.', 'DOT'),
        (r':', 'COLON'),
        (r'\d+', 'NUMBER'),
        (r'\s+', None)
    ]
    
    tokens = []
    for pattern, token_type in token_patterns:
        for match in re.finditer(pattern, code):
            if token_type:
                tokens.append((match.group(), token_type))
    return tokens

def parse_program(tokens):
    root = {"Program": []}
    while tokens:
        if tokens[0][1] == 'VARIABLE_DECLARATION':
            root["Program"].append(parse_variable(tokens))
        elif tokens[0][1] == 'KEYWORD' and tokens[0][0] == 'proc':
            root["Program"].append(parse_procedure(tokens))
        elif tokens[0][1] in {'COMMAND', 'COMMAND_JUMP', 'COMMAND_GOTO', 'IDENTIFIER'}:
            root["Program"].append(parse_instruction(tokens))
        elif tokens[0][1] == 'KEYWORD' and tokens[0][0] in {'if:', 'while:', 'repeatTimes:'}:
            root["Program"].append(parse_conditional(tokens))
        else:
            print(f"Error: Token inesperado '{tokens[0][0]}'")
            return None
    return root

def parse_variable(tokens):
    return {"VariableDeclaration": tokens.pop(0)[0]}

def parse_procedure(tokens):
    tokens.pop(0)  # "proc"
    proc_name = tokens.pop(0)[0]  # Nombre del procedimiento
    proc_node = {"Procedure": {"name": proc_name, "body": []}}
    tokens.pop(0)  # "["
    while tokens and tokens[0][0] != "]":
        proc_node["Procedure"]["body"].append(parse_instruction(tokens))
    tokens.pop(0)  # "]"
    return proc_node

def parse_instruction(tokens):
    instr_node = {"Instruction": tokens.pop(0)[0]}
    instr_node["Parameters"] = []
    while tokens and tokens[0][1] in {'NUMBER', 'CONSTANT', 'IDENTIFIER', 'COLON'}:
        instr_node["Parameters"].append(tokens.pop(0)[0])
    return instr_node

def parse_conditional(tokens):
    cond_node = {"Conditional": {"type": tokens.pop(0)[0], "condition": None, "body": []}}
    if tokens and tokens[0][1] == 'CONSTANT':
        cond_node["Conditional"]["condition"] = tokens.pop(0)[0]
    if tokens and tokens[0][1] == 'KEYWORD' and tokens[0][0] == 'then:':
        tokens.pop(0)
        cond_node["Conditional"]["body"].append(parse_instruction(tokens))
    if tokens and tokens[0][1] == 'KEYWORD' and tokens[0][0] == 'else:':
        tokens.pop(0)
        cond_node["Conditional"]["body"].append(parse_instruction(tokens))
    return cond_node

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

tokens = tokenize_robot_language(robot_code)
parse_tree = parse_program(tokens)
if parse_tree:
    import json
    print(json.dumps(parse_tree, indent=2))
