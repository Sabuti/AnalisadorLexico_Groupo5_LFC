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
    if not token:
        return False
    try:
        if token.count(".") > 1: # Checa se há mais de um ponto decimal
            return False
        float(token)
        return True
    except ValueError:
        return False
    
def estadoOperador(token):
    match token:
        case "+" | "-" | "*" | "/" | "%" | "^":
            return True
        case _:
            return False

def estadoParenteses(token):
    match token:
        case "(" | ")":
            return True
        case _:
            return False

# AFD: identificadores/COMANDOS (RES/MEM)
def RESorMEM(token):
    if not token:
        return False

    estado = "Q0"  # Q0(início), QID
    for ch in token:
        match estado:
            case "Q0":
                if ch.isalpha() and ch.isupper():
                    estado = "QID"
                else:
                    return False
            case "QID":
                if ch.isalpha() and ch.isupper():
                    pass
                elif ch.isdigit():
                    pass
                else:
                    return False

    if token in {"RES", "MEM"}:
        return True
    return True

# -------------------------
# Analisador léxico: valida CADA token isoladamente
def analisadorLexico(tokens):
    f = open("funcoes_analisador.txt", "a")
    for token in tokens:
        if estadoParenteses(token):
            f.write(token+"\n")
            continue
        if estadoOperador(token):
            f.write(token)
            continue
        if estadoNumero(token):
            f.write(token)
            continue
        if RESorMEM(token):
            f.write(token)  # aceita tanto CMD (RES/MEM) quanto ID (nomes de memória)
            continue

        # Se não passou em nada, é inválido
        raise ValueError(f"Erro léxico: token inválido -> {token}")

    return True

# Implementar executarExpressao(const std::vector<std.string>& _tokens_, 
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

def gerarAssembly(tokens, assembly, assembly_rodata, temp_count):
    stack = []
    reg_temp = 26
    for r in range(22, 26): # Limpa registradores temporários
        assembly.append(f"clr r{r}")

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
        assembly.append(f"ldi r30, lo8({label})") # Carrega endereço do float
        assembly.append(f"ldi r31, hi8({label})") # Carrega endereço do float
        assembly.append("lpm r22, Z+") # Carrega parte baixa
        assembly.append("lpm r23, Z") # Carrega parte alta
        return ["r22", "r23"] # Resultado da equação fica em r22:r23

    for token in tokens:
        try:
            float(token)
            is_number = True
        except ValueError:
            is_number = False

        if is_number:
            if reg_temp > 30:  # Limite de registradores temporários
                reg_temp = 26  # Reseta para o início
            reg = load_float_16(token)
            assembly.append(f"movw r{reg_temp}, r22")  # Move word para registrador temporário
            reg_temp += 2
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
                assembly.append(f"add r{reg_temp-2}, r{reg_temp-4}")
                assembly.append(f"adc r{reg_temp-1}, r{reg_temp-3}")
                assembly.append(f"movw r24, r{reg_temp-2}")
            elif token == '-':
                assembly.append(f"sub r{reg_temp-2}, r{reg_temp-4}")
                assembly.append(f"sbc r{reg_temp-1}, r{reg_temp-3}")
                assembly.append(f"mov r24, r{reg_temp-2}")  # Move resultado para r24:r25
                assembly.append(f"mov r25, r{reg_temp-1}")
            elif token == '*':
                assembly.append(f"mov r18, r{reg_temp-4}")  # Multiplicando em r18:r19
                assembly.append(f"mov r19, r{reg_temp-3}")
                assembly.append(f"mov r20, r{reg_temp-2}")  # Multiplicador em r20:r21
                assembly.append(f"mov r21, r{reg_temp-1}")
                assembly.append("mul r18, r21")  # a_low * b_low
                assembly.append("mov r22, r0")   # Armazena o resultado parcial
                assembly.append("mov r23, r1")
                assembly.append("mul r19, r20") # a_high * b_low (<<8)
                assembly.append("add r23, r0")  # Adiciona ao resultado parcial
                assembly.append("mul r18, r20") # a_low * b_high (<<8)
                assembly.append("add r23, r0")  # Adiciona ao resultado parcial
                assembly.append("clr r0")      # Limpa registrador temporário
            elif token == '/':
                assembly.append("div_loop:")
                assembly.append(f"    cp r{reg_temp-4}, r{reg_temp-2}")  # Compara A com B
                assembly.append(f"    cpc r{reg_temp-3}, r{reg_temp-1}")
                assembly.append("    breq div_fim") 
                assembly.append("    brlo div_fim")
                assembly.append(f"    sub r{reg_temp-4}, r{reg_temp-2}")  # Evita divisão por zero
                assembly.append(f"    sbc r{reg_temp-3}, r{reg_temp-1}")
                assembly.append("    adiw r24, 1")  # r24 pra qociente += 1
                assembly.append("    rjmp div_loop")
                assembly.append("div_fim:")
                assembly.append(f"    movw r24, r{reg_temp-4}")  # Resultado em r24:r25
            elif token == '%': # parecido com divisão, mas resultado é o resto
                assembly.append("mod_loop:")
                assembly.append(f"    cp r{reg_temp-4}, r{reg_temp-2}")  # Compara A com B
                assembly.append(f"    cpc r{reg_temp-3}, r{reg_temp-1}")
                assembly.append("    breq mod_fim")
                assembly.append("    brlo mod_fim") 
                assembly.append(f"    sub r{reg_temp-4}, r{reg_temp-2}")  # Evita divisão por zero
                assembly.append(f"    sbc r{reg_temp-3}, r{reg_temp-1}")
                assembly.append("    adiw r24, 1")  # r24 pra qociente += 1
                assembly.append("    rjmp mod_loop")
                assembly.append("mod_fim:")
                assembly.append(f"    movw r24, r{reg_temp-4}") # Move resultado para r24:r25
            elif token == '^':
                assembly.append("power_loop:")
                assembly.append(f"    tst r{reg_temp-2}") # Testa se B é zero
                assembly.append("    brne do_mul_check") 
                assembly.append(f"    tst r{reg_temp-1}")
                assembly.append("    brne do_mul_check") 
                assembly.append("    rjmp power_end")  
                assembly.append("do_mul_check:")
                assembly.append(f"    mov r18, r{reg_temp-4}")  # Multiplicando em r18:r19
                assembly.append(f"    mov r19, r{reg_temp-3}")
                assembly.append(f"    mov r20, r{reg_temp-2}")  # Multiplicador em r20:r21
                assembly.append(f"    mov r21, r{reg_temp-1}")
                assembly.append("    mul r18, r21")  # a_low * b_low
                assembly.append("    mov r22, r0")   # Armazena o resultado parcial
                assembly.append("    mov r23, r1")
                assembly.append("    mul r19, r20") # a_high * b_low (<<8)
                assembly.append("    add r23, r0")  # Adiciona ao resultado parcial
                assembly.append("    mul r18, r20") # a_low * b_high (<<8)
                assembly.append("    add r23, r0")  # Adiciona ao resultado parcial
                assembly.append("    clr r0")      # Limpa registrador temporário
                assembly.append(f"    sbiw r24, 1") # Decrementa B
                assembly.append("    rjmp power_loop")
                assembly.append("power_end:")
                assembly.append(f"    movw r24, r{reg_temp-2}")  # Move resultado para r24:r25
            stack.append(["r24", "r25"])
        else:
            pass  # Ignore other tokens (e.g., parentheses)
        assembly.append("rcall print_hex16") # Imprime resultado em hexadecimal
        assembly.append("ldi r24, 0x0A")      # Imprime nova linha
        assembly.append("rcall usart_transmit")

    # Retorna o valor atualizado de temp_count
    return temp_count

def usart_init(assembly):
    assembly.append("usart_init:")
    assembly.append("ldi r16, UBRRval >> 8") # Configura baud rate
    assembly.append("sts UBRR0H, r16")
    assembly.append("ldi r16, UBRRval & 0xFF")
    assembly.append("sts UBRR0L, r16") 
    assembly.append("ldi r16, (1<<3)") # Habilita TX (TXEN)
    assembly.append("sts UCSR0B, r16")
    assembly.append("ldi r16, (1<<2) | (1<<1)") # 8 bits (UCSZ01, UCSZ00)
    assembly.append("sts UCSR0C, r16")
    assembly.append("ret")

def usart_transmit(assembly):
    assembly.append("usart_transmit:")
    assembly.append("    ; Transmite o byte em r24")
    assembly.append("    lds r16, UCSR0A")  # Carrega o byte a ser enviado
    assembly.append("    sbrs r16, 5")  # Espera até que o buffer esteja vazio
    assembly.append("    rjmp usart_transmit")
    assembly.append("    sts UDR0, r24")  # Envia o byte
    assembly.append("    ret")

def print_format(assembly):
    assembly.append("print_hex16:")
    assembly.append("    mov r18, r25")
    assembly.append("    rcall print_hex8")
    assembly.append("    mov r19, r24")
    assembly.append("    rcall print_hex8")
    assembly.append("    ret")
    assembly.append("print_hex8:")
    assembly.append("    mov r19, r18")
    assembly.append("    swap r19")
    assembly.append("    andi r19, 0x0F")
    assembly.append("    rcall print_hex_digit")
    assembly.append("    andi r18, 0x0F")
    assembly.append("    rcall print_hex_digit")
    assembly.append("    ret")
    assembly.append("print_hex_digit:")
    assembly.append("    cpi r18, 10")
    assembly.append("    brlo print_hex_digit_num")
    assembly.append("    subi r18, 10")
    assembly.append("    ldi r24, 'A'")
    assembly.append("    add r24, r18")
    assembly.append("    rjmp print_hex_digit_send")
    assembly.append("print_hex_digit_num:")
    assembly.append("    ldi r24, '0'")
    assembly.append("    add r24, r18")
    assembly.append("print_hex_digit_send:")
    assembly.append("    rcall usart_transmit")
    assembly.append("    ret")

#implementado o main que lê o arquivo_teste.txt, chama parseExpressao e depois 
# analisadorLexico.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <nome_do_arquivo>")
    else:
        temp_count = 0
        linhas = []
        memoria = {}
        resultados = []
        codigoAssembly = []
        assembly_rodata = []
        codigoAssembly.append(".equ Fcpu, 16000000")# Define a frequência do clock
        codigoAssembly.append(".equ BAUD, 9600")    # Define a taxa de
        codigoAssembly.append(".equ UBRRval, 103")  # valor do UBRR calculado Fcpu/(16*BAUD)-1
        codigoAssembly.append(".equ UDR0, 0xC6")    # definindo os registradores
        codigoAssembly.append(".equ UBRR0H, 0xC5") 
        codigoAssembly.append(".equ UBRR0L, 0xC4")
        codigoAssembly.append(".equ UCSR0B, 0xC1")
        codigoAssembly.append(".equ UCSR0C, 0xC2")
        codigoAssembly.append(".equ UCSR0A, 0xC0")
        codigoAssembly.append(".text")
        codigoAssembly.append(".global main")
        usart_init(codigoAssembly) # Inicializa rotina de USART
        usart_transmit(codigoAssembly)
        print_format(codigoAssembly)
        codigoAssembly.append("main:")
        codigoAssembly.append("    rcall usart_init")  # Inicializa USART
        caminho = sys.argv[1]
        lerArquivo(caminho, linhas)
        for linha in linhas:
            tokens = []
            try:
                parseExpressao(linha, tokens)
                analisadorLexico(tokens)
                retorno = executarExpressao(tokens, resultados, memoria)
                exibirResultados(linha, retorno)
                is_math_expression = all(t not in ['RES'] for t in tokens)
                if is_math_expression and not isinstance(retorno, ValueError) and len(tokens) > 1:
                    result_asm = gerarAssembly(tokens, codigoAssembly, assembly_rodata, temp_count)

                    if isinstance(result_asm, ValueError):
                        print(f"Erro ao gerar Assembly para a linha '{linha}': {result_asm}")
                        continue
                    else:
                        temp_count = result_asm
            except ValueError as e:
                print(e)

        codigoAssembly.append("rjmp main")

        # grava tudo no final em um arquivo
        with open("./src/saida.S", "w") as f: # cria arquivo no src
            f.write("\n".join(assembly_rodata) + "\n")
            f.write("\n".join(codigoAssembly))