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
        if char.isspace():  # espaço em branco
            if token:
                _tokens_.append(token)
                token = ""
        elif char in "()":  # parênteses
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
        elif char in "+-*/%^":  # operadores
            if token:
                _tokens_.append(token)
                token = ""
            _tokens_.append(char)
        else:  # acumula números ou comandos (ex: MEM, RES)
            token += char
        i += 1
    if token:
        _tokens_.append(token)
    if parenteses != 0:
        raise ValueError("Erro: parênteses desbalanceados.")
    return True

#funções de estado para o analisador léxico
def estadoNumero(token):
    try:
        if token.count(".") > 1: # Checa se há mais de um ponto decimal
            return False
        float(token)
        return True
    except ValueError:
        return False
    
def estadoOperador(token):
    operadores = {"+", "-", "*", "/", "%", "^"}
    if token in operadores:
        return True
    else:
        return False
def estadoParenteses(token):
    if token in {"(", ")"}:
        return True
    else:
        return False

def estadoComando(token):
    if token == "RES" :
        return True
    elif token.isalpha() and token.isupper():
        return True
    else:
        return False


# Implementado o analisador léxico que recebe os tokens extraídos por parseExpressao e 
# imprime cada token com seu tipo.
def analisadorLexico(tokens):
    for token in tokens:
        if estadoNumero(token):
            continue
        elif estadoOperador(token):
            continue
        elif estadoParenteses(token):
            continue
        elif estadoComando(token):
            continue
        else:
            raise ValueError(f"Erro token inválido: {token}")
    return True
    

# Implementar executarExpressao(const std::vector<std::string>& _tokens_, 
# std::vector<float>& resultados, float& memoria) para executar uma expressão RPN;
def executarExpressao(_tokens_, resultados, memoria):
    pilha = []
    i = 0
    comand_mem = False
    comando_res  = False
    comand_other = False

    while i < len(_tokens_):
        token = _tokens_[i]
        if token == '(' or token == ')':
            i += 1
            continue
        if len(_tokens_) == 3:  # Comando memória: VAR
            if token not in memoria:
                pilha.append(0.0)
            else:
                pilha.append(memoria[token])
            comand_mem = True
        elif len(_tokens_) == 4 and _tokens_[i + 1] == 'RES':  # N RES
            n = int(token)
            comando_res = True
            i += 1
        elif len(_tokens_) == 4 and _tokens_[i + 1] != 'RES':  # N MEM
            n = float(token)
            memoria.update({_tokens_[i+1]: n})
            comand_other = True
            i += 1
        else:  # expressão matemática
            if token not in {"+", "-", "*", "/", "%", "^"}:
                try:
                    pilha.append(float(token))
                except ValueError:
                    return ValueError(f"Token inválido recebido: {token}")
            else:
                try:
                    b = pilha.pop()
                    a = pilha.pop()
                except IndexError:
                    return ValueError("Expressão inválida: operandos insuficientes")

                if token == "+": res = a + b
                elif token == "-": res = a - b
                elif token == "*": res = a * b
                elif token == "/":
                    if b == 0: return ValueError("Erro: divisão por zero")
                    res = a / b
                elif token == "%":
                    if b == 0: return ValueError("Erro: resto por zero")
                    res = a % b
                elif token == "^": res = a ** b
                pilha.append(float(res))
        i += 1

    # --- Verificação final ---
    if comand_mem:
        return pilha.pop()
    elif comando_res:
        if n < 0 or n >= len(resultados):
            return ValueError(f"Histórico inválido: {n}")
        return resultados[-(n)]
    elif comand_other:
        return memoria
    elif len(pilha) == 0:
        return ValueError("Comentário lido")
    elif len(pilha) == 1:
        result = pilha.pop()
        resultados.append(result)
        return result
    else:
        return ValueError("Expressão inválida (sobraram itens na pilha)")

# Implementar exibirResultados(const std::vector<float>& resultados) para exibir 
# os resultados das expressões; 
def exibirResultados(linha, retorno):
    if isinstance(retorno, (float, int)):
        print(f"Resultado da expressão '{linha}': {retorno:.1f}")
    elif isinstance(retorno, dict):
        for chave, valor in retorno.items():
            print(f"Memória '{chave}': {valor:.1f}")
    elif isinstance(retorno, ValueError):
        print(f"Erro na linha '{linha}': {retorno}")
    else:
        print(f"Linha '{linha}' ignorada.")

#implementado o main que lê o arquivo_teste.txt, chama parseExpressao e depois 
# analisadorLexico.
if __name__ == "__main__":
    if len(sys.argv) < 2:
       print("Uso: python script.py <nome_do_arquivo>")
    else:
        linhas = []
        memoria = {}
        resultados = []
        caminho = sys.argv[1]
        lerArquivo(caminho, linhas)
        for linha in linhas:
            tokens = []
            try:
                    parseExpressao(linha, tokens)
                    analisadorLexico(tokens)
                    retorno = executarExpressao(tokens, resultados, memoria)
                    exibirResultados(linha, retorno)
            except ValueError as e:
                    print(e)
