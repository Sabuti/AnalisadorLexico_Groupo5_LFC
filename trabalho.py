# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
# RA1 5

#Implementar parseExpressao(std::string linha, std::vector<std::string>& _tokens_) (ou equivalente em Python/C) para analisar uma linha de expressão RPN e extrair tokens.
def parseExpressao(linha, _tokens_):
    operadores = ['+', '-', '*', '/', '(', ')', 'RES', 'MEN']
    token = ""
    parenteses = 0
    i = 0

    while i < len(linha):
        char = linha[i]
        # Espaços em branco
        if char.isspace():
            if token:
                _tokens_.append(token)
                token = ""
        # Verifica os parenteses e se estão balanceados
        elif char in "()":
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

        # Operadores
        elif char in "+-*/":
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)

        # Possível palavras RES ou MEN
        else:
            token += char

        i += 1

    if token:
        _tokens_.append(token)

    # Verificação final dos parênteses
    if parenteses != 0:
        raise ValueError("Erro: faltam parênteses")

    # Validação dos tokens
    for t in _tokens_:
        if t not in operadores:  # se não for operador/parêntese
            try:
                float(t)  # tenta converter pra número
            except ValueError:
                raise ValueError(f"Erro: token inválido '{t}'")

    return True

#Implementado o analisador léxico que recebe os tokens extraídos por parseExpressao e imprime cada token com seu tipo.
def analisadorLexico(tokens): 
    operadores = {'+': 'Operador de Adição', 
                  '-': 'Operador de Subtração', 
                  '*': 'Operador de Multiplicação', 
                  '/': 'Operador de Divisão', 
                  '(': 'Parêntese Aberto', 
                  ')': 'Parêntese Fechado', 
                  'RES': 'Operador RES',
                  'MEN': 'Operador Memoria'}
    for token in tokens:
        if token in operadores:
            print(f"Token: {token}, Tipo: {operadores[token]}")
        else:
            try:
                float(token)
                print(f"Token: {token}, Tipo: Número")
            except ValueError:
                print(f"Token: {token}, Tipo: Identificador")

def executarExpressao(tokens, resultados, memoria):
    pilha = []
    i = 0
    comando_puro = False  # marca se expressão foi só comando (ex: V MEM)
    comando_res  = False  # marca se expressão foi res (ex: N RES)

    while i < len(tokens):
        token = tokens[i]
        if token == '(' or token == ')':
            i += 1 # pular parênteses
            continue
        if len(tokens) == 3: # recebeu o nome da memoria
            if memoria is None:
                pilha.append(0)
            else:
                pilha.append(float(memoria))
            comando_puro = True
        elif len(tokens) == 4 and tokens[i + 1] == 'RES': # recebeu (N RES)
            n = int(token)
            comando_res = True
            i += 1  # pular "RES"
        elif len(tokens) == 4 and tokens[i + 1] != 'RES': # recebeu (N MEM)
            n = float(token)
            memoria.update({tokens[i+1]: n})
            comando_puro = True
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

    # --- Verificação final ---
    if comando_puro:
        return memoria
    elif comando_res:
        if n < 0 or n >= len(resultados):
            raise ValueError(f"Histórico inválido: {n}")
        return resultados[-(n)]
    elif len(pilha) == 1:
        resultado = pilha.pop()
        resultados.append(resultado)
        return resultado
    else:
        raise ValueError("Expressão inválida (sobraram itens na pilha)")

#implementado o main que lê o arquivo_teste.txt, chama parseExpressao e depois analisadorLexico.
def main():
    arquivo_teste = 'arquivo_teste.txt'
    memoria = {}
    resultados = []
    with open(arquivo_teste, 'r') as file:
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