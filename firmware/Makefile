#
# Makefile for the firmware of "Faberdanaio"
#
SHELL = /bin/sh
all:
	@echo Building firmware...
	@gpasm -ppic12f509 main.asm && cat main.lst | grep "Program Memory"
	@if [ $$? -ne 1 ]; then \
		echo Build succeeded. Programming device...; \
		pk2cmd -M -PPIC12f509 -Fmain.hex; \
	fi
	
build:
	@echo Building firmware...
	@gpasm -ppic12f509 main.asm && cat main.lst | grep "Program Memory"
	
run:
	@pk2cmd -T -R -PPIC12f509

clean:
	@rm *.hex *.cod *.lst
	