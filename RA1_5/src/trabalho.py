# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
# RA1 5
#teste 1

import sys # import para gerenciar argumentos de linha de comando

# Implementar lerArquivo(std::string nomeArquivo, std::vector<std::string>& linhas) 
# para ler o arquivo de entrada;
def lerArquivo(nomeArquivo, linhas):
    try:
        with open(nomeArquivo, 'r') as file:
            for linha in file:
                linha = linha.strip()
                if linha:  # Ignorar linhas vazias
                    linhas.append(linha)
    except FileNotFoundError:
        print(f"Erro: arquivo '{nomeArquivo}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return
    return linhas


# Implementar parseExpressao(std::string linha, std::vector<std::string>& _tokens_) 
# (ou equivalente em Python/C) para analisar uma linha de expressão RPN e extrair tokens.
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


# Implementado o analisador léxico que recebe os tokens extraídos por parseExpressao e 
# imprime cada token com seu tipo.
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
                    return False  # indica que deu erro
    """ --- Código de debug ---
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
    """
    return True

