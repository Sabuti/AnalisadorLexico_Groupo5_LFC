# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
# RA1 5

import os # import para gerenciar arquivos
import sys # import para gerenciar argumentos de linha de comando

#Implementar parseExpressao(std::string linha, std::vector<std::string>& _tokens_) (ou equivalente em Python/C) para analisar uma linha de expressão RPN e extrair tokens.
def parseExpressao(linha, _tokens_): 
    token = ""
    parenteses = 0
    i = 0
    while i < len(linha):
        char = linha[i]
        if char =="$":
            i += 1
            break
        elif char.isspace():# Ignorar espaços
            if token:
                _tokens_.append(token)
                token = ""
        elif char in "()":# Tratamento de parênteses
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)
            if char == "(":
                parenteses += 1
            else:
                parenteses -= 1
                if parenteses < 0:
                    raise ValueError("Erro: parêntese fechado sem correspondente.")
        elif char in "+-*/%^": # Tratamento de operadores
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)
        else: # Acúmulo de token (pode ser número ou identificador)
            token += char
        i += 1
    if token:
        _tokens_.append(token)
    if parenteses != 0:# Verificação final dos parênteses
        raise ValueError("Erro: parênteses desbalanceados.")
    return True

#Implementado o analisador léxico que recebe os tokens extraídos por parseExpressao e imprime cada token com seu tipo.
def analisadorLexico(tokens): 
    operadores_valida = ['+', '-', '*', '/', '%','^' ,'(', ')', 'RES']  
    for t in tokens:# Validação dos tokens
        if t not in operadores_valida and t not in ["(", ")"]:  
            # Testa número
            try:
                float(t)
            except ValueError:
                # Se não for número, tem que ser identificador válido (apenas maiúsculas)
                if not (t.isalpha() and t.isupper()):
                    raise ValueError(f"Erro: token inválido '{t}'")
    operadores = {'+': 'Operador de Adição', 
                  '-': 'Operador de Subtração', 
                  '*': 'Operador de Multiplicação', 
                  '/': 'Operador de Divisão', 
                  '%': 'Operador de Resto', 
                  '^': 'Operador de Potenciação', 
                  '(': 'Parêntese Aberto', 
                  ')': 'Parêntese Fechado', 
                  'RES': 'RES',
                  'MEM': 'Memoria'}
    for token in tokens:
        if token in operadores:
            print(f"Token: {token}, Tipo: {operadores[token]}")
        else:
            try:
                float(token)
                print(f"Token: {token}, Tipo: Número")
            except ValueError:
                print(f"Token: {token}, Tipo: Memoria")

def executarExpressao(tokens, resultados, memoria):
    pilha = []
    i = 0
    comand_mem = False  # marca se expressão foi só comando (ex: MEM)
    comando_res  = False  # marca se expressão foi res (ex: N RES)
    comand_other = False  # marca se expressão foi de memoria (ex: N MEM)

    while i < len(tokens):
        token = tokens[i]
        if token == '(' or token == ')':
            i += 1 # pular parênteses
            continue
        if len(tokens) == 3: # recebeu o nome da memoria
            if token not in memoria:
                pilha.append(0.0)  # valor padrão se não existir
            else:
                pilha.append(memoria[token])
            comand_mem = True
        elif len(tokens) == 4 and tokens[i + 1] == 'RES': # recebeu (N RES)
            n = int(token)
            comando_res = True
            i += 1  # pular "RES"
        elif len(tokens) == 4 and tokens[i + 1] != 'RES': # recebeu (N MEM)
            n = float(token)
            memoria.update({tokens[i+1]: n})
            comand_other = True
            i += 1  # pular nome da memoria
        else: # Recebeu expressão matemática
            if token not in {"+", "-", "*", "/", "%", "^"}: # se não for operador
                pilha.append(float(token))
            else: # se for operador
                b = pilha.pop()
                a = pilha.pop()
                if token == "+": res = a + b
                elif token == "-": res = a - b
                elif token == "*": res = a * b
                elif token == "/":
                    if b == 0: raise ZeroDivisionError("Divisão por zero")
                    res = a / b
                elif token == "%":
                    if b == 0: raise ZeroDivisionError("Resto por zero")
                    res = a % b
                elif token == "^": res = a ** b
                pilha.append(float(res))
        i += 1

    # --- Verificação e returns ---
    if comand_mem:
        memory_value = pilha.pop()
        return memory_value
    elif comando_res:
        if n < 0 or n >= len(resultados):
            raise ValueError(f"Histórico inválido: {n}")
        return resultados[-(n)]
    elif comand_other:
        return memoria
    elif len(pilha) == 1:
        result = pilha.pop()
        resultados.append(result)
        return result
    else:
        raise ValueError("Expressão inválida (sobraram itens na pilha)")

#implementado o main que lê o arquivo_teste.txt, chama parseExpressao e depois analisadorLexico.
def main():
    #arquivo_teste = sys.argv[0] teste
    arquivo_teste = 'arquivo_teste.txt'
    memoria = {}
    resultados = []
    with open(arquivo_teste, 'r') as file:
        if os.path.getsize(arquivo_teste) == 0:
            print(f"O arquivo '{arquivo_teste}' está vazio.")
        for linha in file:
            linha = linha.strip()
            if linha:  # Ignorar linhas vazias
                tokens = []
                try:
                    parseExpressao(linha, tokens)
                    analisadorLexico(tokens)
                    print(executarExpressao(tokens, resultados, memoria))
                except ValueError as e:
                    print(e)

if __name__ == "__main__":
    main()