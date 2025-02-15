def validar_corchetes(code):
    #valido que los corchetes esten balanceados y analiza los bloques
    def revisar_balance(i, prof):
        if i >= len(code):
            return prof == 0
        if code[i] == '[':
            return revisar_balance(i + 1, prof + 1)
        elif code[i] == ']':
            if prof == 0:
                return False
            return revisar_balance(i + 1, prof - 1)
        return revisar_balance(i + 1, prof)
    
    return revisar_balance(0, 0)

def definir(codigo):
    #código del robot basado en reglas predefinidas
    comandos = ["move:", "turn:", "face:", "put:", "pick:", "jump:", "if:", "while:", "for:", "nop", "proc:", "repeatTimes:", "goTo:", "canMove:", "canJump:", "facing:"]
    lista = []
    p = codigo.replace("\n", " ").split()
    
    for palabra in p:
        if palabra in comandos or palabra.replace(".", "") in comandos:
            lista.append(palabra.replace(".", ""))
    
    return lista

def parse(t):
    stack = []
    for tata in t:
        if tata in ["if:", "while:", "for:", "proc:"]:
            stack.append(tata)
        elif tata == "[":
            stack.append(tata)
        elif tata == "]":
            if not stack or stack[-1] != "[":
                return False
            stack.pop()
        elif tata == "else:":
            if not stack or stack[-1] != "if:":
                return False
    return stack

def analizar(cod):
    if not validar_corchetes(cod):
        print("Error: Los bloques de código no están balanceados.")
        return False
    
    tok= definir(cod)
    if not parse(tok):
        print("Error: Estructura del código inválida.")
        return False
    
    return True

# Código de prueba
code = """
|nom x y one|

proc putChips: n andBalloons: m [
    |c, b|
    c := n .
    b := m .
    put: c ofType: #chips . put: b ofType: #balloons .
]

proc goNorth [
    while: canMove: 1 inDir: #north do: [ move: 1 inDir: #north . ]
]

proc goWest [
    if: canMove: 1 inDir: #west then: [ move: 1 inDir: #west . ] else: [ nop . ]
]

[
    goTo: 3 with: 3 .
    putChips: 2 andBalloons: 1 .
]
"""

if analizar(code):
    print("Código válido")
else:
    print("Código inválido")
