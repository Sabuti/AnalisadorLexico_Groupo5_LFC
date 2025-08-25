# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
# RA1 5
#teste

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

# Implementar executarExpressao(const std::vector<std::string>& _tokens_, 
# std::vector<float>& resultados, float& memoria) para executar uma expressão RPN;
def executarExpressao(_tokens_, resultados, memoria):
    pilha = []
    i = 0
    comand_mem = False  # marca se expressão foi só comando (ex: MEM)
    comando_res  = False  # marca se expressão foi res (ex: N RES)
    comand_other = False  # marca se expressão foi de memoria (ex: N MEM)

    while i < len(_tokens_):
        token = _tokens_[i]
        if token == '(' or token == ')':
            i += 1 # pular parênteses
            continue
        if len(_tokens_) == 3: # recebeu o nome da memoria
            if token not in memoria:
                pilha.append(0.0)  # valor padrão se não existir
            else:
                pilha.append(memoria[token])
            comand_mem = True
        elif len(_tokens_) == 4 and _tokens_[i + 1] == 'RES': # recebeu (N RES)
            n = int(token)
            comando_res = True
            i += 1  # pular "RES"
        elif len(_tokens_) == 4 and _tokens_[i + 1] != 'RES': # recebeu (N MEM)
            n = float(token)
            memoria.update({_tokens_[i+1]: n})
            comand_other = True
            i += 1  # pular nome da memoria
        else: # Recebeu expressão matemática
            if token not in {"+", "-", "*", "/", "%", "^"}: # se não for operador
                try:
                    pilha.append(float(token))
                except ValueError:
                    return ValueError(f"Token inválido recebido")
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
    elif len(pilha) == 0:
        return ValueError("Comentário lido")
    elif len(pilha) == 1:
        result = pilha.pop()
        resultados.append(result)
        return result
    else:
        raise ValueError("Expressão inválida (sobraram itens na pilha)")

# Implementar exibirResultados(const std::vector<float>& resultados) para exibir 
# os resultados das expressões;    
def exibirResultados(linha, resultados, memoria):
    try:
        tokens = []
        parseExpressao(linha, tokens)
        if len(tokens) == 3:  # Comando de memória (ex: VAR)
            valor_memoria = executarExpressao(tokens, resultados, memoria)
            print(f"Valor na memória '{tokens[1]}': {valor_memoria}")
        elif len(tokens) == 4 and tokens[2] == 'RES':  # Comando RES (ex: N RES)
            n = int(tokens[1])
            valor_res = executarExpressao(tokens, resultados, memoria)
            print(f"Resultado RES {n}: {valor_res}")
        elif len(tokens) == 4 and tokens[2] != 'RES':  # Comando MEM (ex: N MEM)
            executarExpressao(tokens, resultados, memoria)
            print(f"Valor '{tokens[1]}' armazenado na memória '{tokens[2]}'")
        else:  # Expressão matemática
            resultado = executarExpressao(tokens, resultados, memoria)
            print(f"Resultado da expressão '{linha}': {resultado}")
    except ValueError as e:
        print(e)

def gerarAssembly(tokens, filename="saida.asm"):
    mem_vals = {}
    assembly = []
    stack = []
    temp_count = 0
    next_reg = 22  # registradores livres começam em r22

    mem_regs = {}  # token -> registradores [r?, r?]

    # Cabeçalho
    assembly.append(".include \"m328pdef.inc\"")
    assembly.append(".global main")
    assembly.append(".section .text")
    assembly.append("main:")

    # Função auxiliar para carregar float 16 bits
    def load_float_16(val):
        nonlocal temp_count
        label = f"flt{temp_count}"
        temp_count += 1
        # Armazena valor 16 bits (fix-point)
        assembly.append(".section .rodata")
        assembly.append(f"{label}: .word {int(val*65536)}  ; 16-bit fix-point")
        assembly.append(".section .text")
        assembly.append(f"ldi r30, lo8({label})")
        assembly.append(f"ldi r31, hi8({label})")
        assembly.append("ld r22, Z+")
        assembly.append("ld r23, Z")
        return ["r22", "r23"]

    # Função para pegar próximo registrador livre
    def alloc_regs(n=2):
        nonlocal next_reg
        regs = [f"r{next_reg + i}" for i in range(n)]
        next_reg += n
        return regs

    for token in tokens:
        # número literal
        if token.replace('.', '', 1).isdigit():
            regs = load_float_16(float(token))
            stack.append(regs)

        # token de memória / identificador
        elif token.isalpha():
            tok_upper = token.upper()
            if tok_upper in mem_regs:
                regs = mem_regs[tok_upper]
            else:
                # pega valor inicial do dicionário ou 0
                valor = mem_vals.get(tok_upper, 0)
                regs = load_float_16(valor)
                mem_regs[tok_upper] = alloc_regs()
                # mover valor para registradores da memória
                assembly.append(f"mov {mem_regs[tok_upper][0]}, {regs[0]}")
                assembly.append(f"mov {mem_regs[tok_upper][1]}, {regs[1]}")
                regs = mem_regs[tok_upper]
            stack.append(regs.copy())

        # operadores 16-bit
        elif token in ['+', '-', '*', '/']:
            if len(stack) < 2:
                raise ValueError(f"Pilha insuficiente para operador '{token}'")

            op2 = stack.pop()
            op1 = stack.pop()

            # mover para r18-r21
            assembly.append(f"mov r18, {op1[0]}")
            assembly.append(f"mov r19, {op1[1]}")
            assembly.append(f"mov r20, {op2[0]}")
            assembly.append(f"mov r21, {op2[1]}")

            # chama função correspondente (você precisaria criar __add16, etc.)
            if token == '+':
                assembly.append("call __add16")
            elif token == '-':
                assembly.append("call __sub16")
            elif token == '*':
                assembly.append("call __mul16")
            elif token == '/':
                assembly.append("call __div16")
            elif token == '^':
                # checa se o op2 é inteiro
                if '.' in op2 and float(op2) != int(float(op2)):
                    raise ValueError(f"op2 não inteiro: {op2} (pow só suporta inteiro no AVR)")

                assembly.append(f"; {op1} ^ {op2}")
                assembly.append("call __powisf2")
                stack.append("resultado_pow")


            # empilha resultado em r22-r23
            assembly.append("mov r22, r18")
            assembly.append("mov r23, r19")
            stack.append(["r22", "r23"])

        else:
            assembly.append(f"; Token desconhecido: {token}")

    assembly.append("; Resultado final em r22-r23")
    assembly.append("ret")

    # escrever arquivo
    with open(filename, "w") as f:
        f.write("\n".join(assembly))

    return "\n".join(assembly)


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
            parseExpressao(linha, tokens)
            analisadorLexico(tokens)
            executarExpressao(tokens, resultados, memoria)
            gerarAssembly(tokens)
            #exibirResultados(linha, resultados, memoria)