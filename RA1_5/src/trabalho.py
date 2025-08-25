# Ana Maria Midori Rocha Hinoshita - anamariamidori
# Lucas Antonio Linhares - Sabuti
# RA1 5

import sys # import para gerenciar argumentos de linha de comando
import math

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

# Implementar parseExpressao(std::string linha, std::vector<std.string>& _tokens_) 
# (ou equivalente em Python/C) para analisar uma linha de expressão RPN e extrair tokens.
def parseExpressao(linha, _tokens_): 
    token = ""
    parenteses = 0
    i = 0
    while i < len(linha):
        char = linha[i]
        if char == "$":
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
    return True

# Implementar executarExpressao(const std::vector<std.string>& _tokens_, 
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

def gerarAssembly(tokens, assembly, assembly_rodata, temp_count):
    stack = []
    next_reg = 22  # registradores livres começam em r22

    # Funções para chamar rotinas 16-bit
    def add_16(dst, src):
        assembly.append(f"mov r24, {src[0]}")
        assembly.append(f"mov r25, {src[1]}")
        assembly.append(f"add r22, r24")
        assembly.append(f"adc r23, r25")

    def sub_16(dst, src):
        assembly.append(f"mov r24, {src[0]}")
        assembly.append(f"mov r25, {src[1]}")
        assembly.append("sub r22, r24")
        assembly.append("sbc r23, r25")

    def mul_16(dst, src):
        assembly.append(f"mov r24, {src[0]}")
        assembly.append(f"mov r25, {src[1]}")
        assembly.append(f"andi r24, 0x80") 

    def div_16(dst, src):
        assembly.append(f"mov r24, {src[0]}")
        assembly.append(f"mov r25, {src[1]}")
        assembly.append("rcall div16")  # dst = dst / src

    def mod_16(dst, src):
        assembly.append(f"mov r24, {src[0]}")
        assembly.append(f"mov r25, {src[1]}")
        assembly.append("rcall mod16")  # dst = dst % src

    def pow_16(dst, src):
        assembly.append(f"mov r24, {src[0]}")
        assembly.append(f"mov r25, {src[1]}")
        assembly.append("rcall pow16")  # dst = dst ^ src

    def load_float_16(val):
        nonlocal temp_count
        try:
            fval = float(val)
        except ValueError:
            return ValueError(f"Token inválido: {val}")

        # Handle special cases
        if fval == 0.0:
            word_val = 0x0000  # Zero
        elif math.isinf(fval):
            word_val = 0x7C00 if fval > 0 else 0xFC00  # Infinity (+/-)
        elif math.isnan(fval):
            word_val = 0x7E00  # NaN
        else:
            # Convert to IEEE 754 half-precision
            # Python's struct can convert to float16, but we need to extract the bits
            # Use a custom conversion for simplicity
            sign = 0 if fval >= 0 else 1
            fval = abs(fval)
            if fval == 0:
                word_val = 0
            else:
                # Extract exponent and mantissa
                exponent = math.floor(math.log2(fval)) if fval != 0 else 0
                mantissa = fval / (2 ** exponent) - 1.0  # Get fractional part
                biased_exponent = exponent + 15  # Bias = 15
                if biased_exponent <= 0:  # Denormal
                    mantissa = fval / (2 ** -14)  # Adjust for denormal
                    biased_exponent = 0
                elif biased_exponent >= 31:  # Infinity
                    return 0x7C00 if sign == 0 else 0xFC00
                mantissa_bits = int(mantissa * (2 ** 10)) & 0x3FF  # 10-bit mantissa
                word_val = (sign << 15) | (biased_exponent << 10) | mantissa_bits

        label = f"flt{temp_count}"
        assembly_rodata.append(f"{label}: .word 0x{word_val:04X}")
        temp_count += 1
        assembly.append(f"ldi r30, lo8({label})")
        assembly.append(f"ldi r31, hi8({label})")
        assembly.append("lpm r22, Z+")
        assembly.append("lpm r23, Z")
        return ["r22", "r23"]

    for token in tokens:
        try:
            float(token)
            is_number = True
        except ValueError:
            is_number = False

        if is_number:
            reg = load_float_16(token)
            if isinstance(reg, ValueError):
                return reg
            stack.append(reg)
        elif token in ['+', '-', '*', '/', '%', '^']:
            try:
                b = stack.pop()
                a = stack.pop()
            except IndexError:
                return ValueError("Operador inválido.")
            if token == '+':
                add_16(a, b)
            elif token == '-':
                sub_16(a, b)
            elif token == '*':
                mul_16(a, b)
            elif token == '/':
                div_16(a, b)
            elif token == '%':
                mod_16(a, b)
            elif token == '^':
                pow_16(a, b)
            stack.append(a)  # Result in r22:r23
        else:
            pass  # Ignore other tokens (e.g., parentheses)

    # Retorna o valor atualizado de temp_count
    return temp_count

#implementado o main que lê o arquivo_teste.txt, chama parseExpressao e depois 
# analisadorLexico.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <nome_do_arquivo>")
    else:
        linhas = []
        memoria = {}
        resultados = []
        codigoAssembly = []
        assembly_rodata = []
        temp_count = 0
        codigoAssembly.append(".global main")
        codigoAssembly.append(".text")
        codigoAssembly.append("main:")
        caminho = sys.argv[1]
        lerArquivo(caminho, linhas)
        for linha in linhas:
            tokens = []
            try:
                # Tenta analisar a linha
                parseExpressao(linha, tokens)
                analisadorLexico(tokens)

                # Processa a linha com o interpretador primeiro
                result_exec = executarExpressao(tokens, resultados, memoria)
                
                # Se o interpretador retornar um erro, imprime a mensagem e pula para a próxima linha
                if isinstance(result_exec, ValueError):
                    print(f"Erro na linha '{linha}': {result_exec}")
                    continue

                # Se a execução foi bem sucedida e a linha é uma expressão matemática,
                # gera o assembly para ela.
                is_math_expression = all(t not in ['MEM', 'RES', 'MEN'] for t in tokens)
                if is_math_expression:
                    result_asm = gerarAssembly(tokens, codigoAssembly, assembly_rodata, temp_count)

                    if isinstance(result_asm, ValueError):
                        print(f"Erro ao gerar Assembly para a linha '{linha}': {result_asm}")
                        continue
                    else:
                        temp_count = result_asm
                else:
                    # Imprime o resultado do interpretador, mas não gera assembly
                    print(f"Linha '{linha}' processada, mas ignorada para geração de assembly.")

            except ValueError as e:
                # Captura erros de parsing ou léxico
                print(f"Erro na linha '{linha}': {e}")
                continue

        codigoAssembly.append("rjmp main")

        # grava tudo no final em um arquivo
        with open("saida.S", "w") as f:
            f.write(".section .rodata\n")
            f.write("\n".join(assembly_rodata) + "\n")
            f.write(".text\n.global main\n")
            f.write("\n".join(codigoAssembly))