; Ana Maria Midori Rocha Hinoshita - anamariamidori
; Lucas Antonio Linhares - Sabuti
; RA1 5
	jmp start
		.include "macros.inc"
start:
    ldi R16, 0xF # pra ser 15
    ldi R17, 0x5
    ldi R18, 0x0

    add R16, R17 # R16 = R16 + R17
    sub R16, R17 # R16 = R16 - R17
    div R16, R17 # R16 = R16 / R17
    mul R16, R17 # R16 = R16 * R17 UNSIGNED, REVER DPS

    push R1    # add R1 a pilha
    rjmp start