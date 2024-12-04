.data
x: .word 0
str_2: .asciiz ""Give me a number: ""
y: .word 0
.text
.globl main
main:
la $a0, str_2
li $v0, 4
syscall
li $v0, 5
syscall
sw $v0, x
li $t1, 1
li $t2, 2
add $t0, $t1, $t2
sw $t0, x
lw $t4, x
li $t5, 4
add $t3, $t4, $t5
sw $t3, y
lw $a0, y
li $v0, 1
syscall
li $v0, 10
syscall