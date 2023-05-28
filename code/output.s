lui $ra, 0x40
addi $ra, $ra, 0xc
j main
j __END__
#0: (':', 'test', '', '')
test:

#1: ('+', 'a', 'b', '@tmp_0')
lw $4, 268500992 #load <a> in func <test>
lw $5, 268500996 #load <b> in func <test>
add $6, $4, $5

#2: ('+', '@tmp_0', 'c', '@tmp_1')
lw $7, 268501000 #load <c> in func <test>
add $8, $6, $7

#3: ('=', '@tmp_1', '', '#eax')
add $v0, $8, $zero

#4: ('ret', '', '', '')
jr $ra


#5: (':', 'main', '', '')
main:

#6: ('=i', '1', '', '@tmp_2')
addi $4, $zero, 1

#7: ('=i', '2', '', '@tmp_3')
addi $5, $zero, 2

#8: ('=i', '3', '', '@tmp_4')
addi $6, $zero, 3

#9: ('par', '@tmp_2', 0, 'test')
sw $4, 268500992

#10: ('par', '@tmp_3', 1, 'test')
sw $5, 268500996

#11: ('par', '@tmp_4', 2, 'test')
sw $6, 268501000

#12: ('call', 'test', '', '')
add $a0, $ra, $zero
jal test
add $ra, $a0, $zero

#13: ('=', '#eax', '', '@tmp_5')
add $4, $v0, $zero

#14: ('=', '@tmp_5', '', 'a')
add $5, $4, $zero

#15: ('ret', '', '', '')
jr $ra


# compile finished.
__END__:
