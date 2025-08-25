.include "m328pdef.inc"
.global main
.section .text
main:
; Token desconhecido: (
.section .rodata
flt0: .word 1540096  ; 16-bit fix-point
.section .text
ldi r30, lo8(flt0)
ldi r31, hi8(flt0)
ld r22, Z+
ld r23, Z
.section .rodata
flt1: .word 393216  ; 16-bit fix-point
.section .text
ldi r30, lo8(flt1)
ldi r31, hi8(flt1)
ld r22, Z+
ld r23, Z
mov r18, r22
mov r19, r23
mov r20, r22
mov r21, r23
call __sub16
mov r22, r18
mov r23, r19
; Token desconhecido: )
; Resultado final em r22-r23
ret