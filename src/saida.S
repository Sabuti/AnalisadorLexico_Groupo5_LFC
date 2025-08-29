flt0: .word 0x4000
flt1: .word 0x3C00
flt2: .word 0x4000
flt3: .word 0x3E00
flt4: .word 0x4200
flt5: .word 0x3F99
flt6: .word 0x4200
flt7: .word 0x4000
flt8: .word 0x4DE0
flt9: .word 0x4600
flt10: .word 0x3C00
flt11: .word 0x4100
flt12: .word 0x4419
flt13: .word 0x4633
flt14: .word 0x3E66
.equ Fcpu, 16000000
.equ BAUD, 9600
.equ UBRRval, 103
.equ UDR0, 0xC6
.equ UBRR0H, 0xC5
.equ UBRR0L, 0xC4
.equ UCSR0B, 0xC1
.equ UCSR0C, 0xC2
.equ UCSR0A, 0xC0
.text
.global main
usart_init:
ldi r16, UBRRval >> 8
sts UBRR0H, r16
ldi r16, UBRRval & 0xFF
sts UBRR0L, r16
ldi r16, (1<<3)
sts UCSR0B, r16
ldi r16, (1<<2) | (1<<1)
sts UCSR0C, r16
ret
usart_transmit:
    ; Transmite o byte em r24
    lds r16, UCSR0A
    sbrs r16, 5
    rjmp usart_transmit
    sts UDR0, r24
    ret
print_hex16:
    mov r18, r25
    rcall print_hex8
    mov r19, r24
    rcall print_hex8
    ret
print_hex8:
    mov r19, r18
    swap r19
    andi r19, 0x0F
    rcall print_hex_digit
    andi r18, 0x0F
    rcall print_hex_digit
    ret
print_hex_digit:
    cpi r18, 10
    brlo print_hex_digit_num
    subi r18, 10
    ldi r24, 'A'
    add r24, r18
    rjmp print_hex_digit_send
print_hex_digit_num:
    ldi r24, '0'
    add r24, r18
print_hex_digit_send:
    rcall usart_transmit
    ret
main:
    rcall usart_init
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt0)
ldi r31, hi8(flt0)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt1)
ldi r31, hi8(flt1)
lpm r22, Z+
lpm r23, Z
movw r28, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
add r28, r26
adc r29, r27
movw r24, r28
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt2)
ldi r31, hi8(flt2)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt3)
ldi r31, hi8(flt3)
lpm r22, Z+
lpm r23, Z
movw r28, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
mod_loop:
    cp r26, r28
    cpc r27, r29
    breq mod_fim
    brlo mod_fim
    sub r26, r28
    sbc r27, r29
    adiw r24, 1
    rjmp mod_loop
mod_fim:
    movw r24, r26
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt4)
ldi r31, hi8(flt4)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt5)
ldi r31, hi8(flt5)
lpm r22, Z+
lpm r23, Z
movw r28, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
mov r18, r26
mov r19, r27
mov r20, r28
mov r21, r29
mul r18, r21
mov r22, r0
mov r23, r1
mul r19, r20
add r23, r0
mul r18, r20
add r23, r0
clr r0
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt6)
ldi r31, hi8(flt6)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt7)
ldi r31, hi8(flt7)
lpm r22, Z+
lpm r23, Z
movw r28, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
power_loop:
    tst r28
    brne do_mul_check
    tst r29
    brne do_mul_check
    rjmp power_end
do_mul_check:
    mov r18, r26
    mov r19, r27
    mov r20, r28
    mov r21, r29
    mul r18, r21
    mov r22, r0
    mov r23, r1
    mul r19, r20
    add r23, r0
    mul r18, r20
    add r23, r0
    clr r0
    sbiw r24, 1
    rjmp power_loop
power_end:
    movw r24, r28
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt8)
ldi r31, hi8(flt8)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt9)
ldi r31, hi8(flt9)
lpm r22, Z+
lpm r23, Z
movw r28, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
sub r28, r26
sbc r29, r27
mov r24, r28
mov r25, r29
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt10)
ldi r31, hi8(flt10)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt11)
ldi r31, hi8(flt11)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt12)
ldi r31, hi8(flt12)
lpm r22, Z+
lpm r23, Z
movw r28, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
add r28, r26
adc r29, r27
movw r24, r28
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt13)
ldi r31, hi8(flt13)
lpm r22, Z+
lpm r23, Z
movw r30, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
ldi r30, lo8(flt14)
ldi r31, hi8(flt14)
lpm r22, Z+
lpm r23, Z
movw r26, r22
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
mov r18, r24
mov r19, r25
mov r20, r26
mov r21, r27
mul r18, r21
mov r22, r0
mov r23, r1
mul r19, r20
add r23, r0
mul r18, r20
add r23, r0
clr r0
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
sub r26, r24
sbc r27, r25
mov r24, r26
mov r25, r27
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
clr r22
clr r23
clr r24
clr r25
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rcall print_hex16
ldi r24, 0x0A
rcall usart_transmit
rjmp main