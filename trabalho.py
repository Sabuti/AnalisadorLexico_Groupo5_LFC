# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
# RA1 5

#Implementar parseExpressao(std::string linha, std::vector<std::string>& _tokens_) (ou equivalente em Python/C) para analisar uma linha de expressão RPN e extrair tokens.
def parseExpressao(linha, _tokens_):
    tokens = linha.split()
    for token in tokens:
        _tokens_.append(token)
    return True

#Implementar bool isOperador(std::string token) (ou equivalente em Python/C) para verificar se um token é um operador válido (+, -, *, /).
def isOperador(token):
    operadores_validos = ['+', '-', '*', '/']
    return token in operadores_validos

#Implementar o analisador léxico usando Autômatos Finitos Determinísticos (AFDs), com cada estado como uma função (ex.: estadoNumero, estadoOperador, estadoParenteses).
def estadoNumero(caractere):
    return caractere.isdigit()
def estadoOperador(caractere):
    return caractere in ['+', '-', '*', '/']
def estadoParenteses(caractere):
    return caractere in ['(', ')']
def analisadorLexico(linha):
    tokens = []
    i = 0
    while i < len(linha):
        caractere = linha[i]
        if caractere.isspace():
            i += 1
            continue
        elif estadoNumero(caractere):
            num = ''
            while i < len(linha) and estadoNumero(linha[i]):
                num += linha[i]
                i += 1
            tokens.append(num)
        elif estadoOperador(caractere):
            tokens.append(caractere)
            i += 1
        elif estadoParenteses(caractere):
            tokens.append(caractere)
            i += 1
        else:
            raise ValueError(f"Caractere inválido: {caractere}")
    return tokens

#Implementar a função principal que lê um arquivo de entrada, processa cada linha com parseExpressao, valida os tokens com isOperador e usa o analisador léxico para extrair tokens.
def main():
    arquivo_entrada = 'arquivo_teste.txt'
    with open(arquivo_entrada, 'r') as f:
        linhas = f.readlines()
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        tokens = []
        if parseExpressao(linha, tokens):
            print(f"Linha: {linha}")
            print(f"Tokens: {tokens}")
            for token in tokens:
                if isOperador(token):
                    print(f"'{token}' é um operador válido.")
                else:
                    print(f"'{token}' não é um operador.")
            print("Analisador Léxico:")
            try:
                lex_tokens = analisadorLexico(linha)
                print(f"Tokens extraídos: {lex_tokens}")
            except ValueError as e:
                print(e)
        else:
            print(f"Erro ao analisar a linha: {linha}")

if __name__ == "__main__":
    main()