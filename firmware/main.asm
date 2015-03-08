;****************************************************************
; Entry point for the firmware of 'Faberdanaio'
;
; Pin assignments:
; GP0 - unused (ICSPDAT exposed through the ICSP connector)
; GP1 - LED square wave out (ICSPCLK)
; GP2 - detector input
; GP3 - unused (MCLR with pull-down)
; GP4 - TTL TX
; GP5 - TTL RX
;
; This code is distributed under the GNU GPL v3.0
; Copyright (C) 2015 - Electric Ant <electricant@anche.no>
;****************************************************************
#include p12f509.inc

;************************
;* CONFIGURATION VALUES *
;************************
	__CONFIG _CP_OFF & _WDT_OFF & _MCLRE_ON & _IntRC_OSC
#define GPIO_SERIAL_INPUT  4
#define GPIO_SERIAL_OUTPUT 5
#define GPIO_LED_OUTPUT    1
#define COIN               GPIO,2

;* Some useful constants
#define SER_OUT     GPIO,GPIO_SERIAL_OUTPUT
#define SER_IN      GPIO,GPIO_SERIAL_INPUT
#define LED_OUT     GPIO,GPIO_LED_OUTPUT
#define RECV_MASK   1<<GPIO_SERIAL_INPUT
#define TOGGLE_MASK 1<<GPIO_LED_OUTPUT

; VARIABLES
t        EQU 0x07		; used for computing delays
ser_data EQU 0x08		; serial data (either received or to send)
ser_cnt  EQU 0x09		; counter for serial transmission
coin     EQU 0x0A		; set to 1 when COIN is 1 and reset otherwhise

; CODE
	ORG	0x000	
	goto init
;**************
; Subroutines *
;**************

; Waste w * 4us. Actually the delay taken to enter and exit this subroutine
; must also be taken into account. This time amounts to 5us more so decrease
; the desired value for w by one.
; If w is 0 then the delay is 256*w as w is decremented first
delay_w4us
	movwf t
dly	nop
	decfsz t,f
	goto	dly
	retlw 0

; Receive data through the serial port. The result is stored in ser_data.
; This function does not wait for the start bit as this is already done in
; the main loop.
ser_receive
	movlw	8
	movwf ser_cnt
	clrf	ser_data
	movlw 24		; sample in the middle of the waveform
	call	delay_w4us
read
	btfss	SER_IN
	bcf	STATUS,C	; If bit = 0, set Carry = 0
	btfsc	SER_IN
	bsf	STATUS,C	; If bit = 1, set Carry = 1
	rrf	ser_data,f	; Shift Carry into the output byte
	movlw	15		; determined by trial and error
	call	delay_w4us
	decfsz ser_cnt,f
	goto 	read
	retlw	0

; Send the data stored in ser_data through the serial port
; the content of ser_data is destroyed
ser_send
	; send start bit
	bcf	SER_OUT
	movlw	16		; determined by trial and error this value gives
	call	delay_w4us  ; a delay of exactly 104us
	movlw	8
	movwf ser_cnt
send
	rrf	ser_data,f
	btfss	STATUS,C
	bcf	SER_OUT	; bit is 0 => line low
	btfsc	STATUS,C
	bsf	SER_OUT	; bit is 1 => line high
	movlw	16
	call	delay_w4us
	decfsz ser_cnt,f
	goto	send
	; idle value for the line is high (+5v)
	bsf	SER_OUT
	movlw	16
	call	delay_w4us
	retlw	0

;***************
; Program code *
;***************
init	; device configuration
	movlw	b'00000000'	; ignore what is written in this part.
	movwf	OSCCAL	; calibrate the oscillator directly
	movlw	b'011101'	; see pin assignments
	tris	GPIO
	bsf	SER_OUT	; idle value for TTL is 5V
	bsf	LED_OUT	; enable LED
	movlw	b'11000101' ; setup TIMER_0 prescaler to 64
	option
	bsf	coin,1	; ignore first coin (startup glitch)

main_loop	; test for a low bit from the serial port or a coin input
	btfss	SER_IN
	goto	cmd_parse
	
	btfss	TMR0,0	; when the last bit is 1 toggle LED_OUT
	goto	main_loop
	clrf	TMR0
	movlw	TOGGLE_MASK
	xorwf	GPIO,f
	btfsc	COIN		; check for coin
	goto	coin_high
	btfss	coin,0	; if coin was 1 then send signal
	goto	main_loop
	movlw	0x21		; !
	movwf	ser_data
	btfss	coin,1	; do not signal if IGNORE is set
	call	ser_send
	clrf	coin		; reset detector status
	goto	main_loop
coin_high
	bsf	coin,0
	goto	main_loop
; Receive the command and parse it
cmd_parse
	call	ser_receive
	bsf	coin,1	; ignore the next coin as it probably is spurious
	
	movlw 0x76		; v
	xorwf	ser_data,w
	btfsc	STATUS,Z
	goto	send_version

	; invalid command received. echo & Abort
	call	ser_send
	goto	main_loop

; send a (short) string containing version information
; not a subroutine because of the limited stack depth of this part
send_version
	movlw	0x76		; v
	movwf	ser_data
	call	ser_send
	movlw	0x30		; 0
	movwf	ser_data
	call	ser_send
	movlw	0x2E		; .
	movwf	ser_data
	call	ser_send
	movlw	0x32		; 2	
	movwf	ser_data
	call	ser_send
	goto	main_loop	
END
