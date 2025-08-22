.macro div
	loop:
		sub @0, @1
		inc @2
		cpi @1, 0x0
		breq end
		rjmp loop
	end:
		add @0, @2
.endmacro

.macro pow
    loop:
        mul @0, @0
        inc @2
        cp  @1, @2
        breq end
        rjmp loop
    end:
.endmacro