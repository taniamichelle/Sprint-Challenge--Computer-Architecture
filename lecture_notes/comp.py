import sys

# Write a program in Python that runs programs
​
# Parse the command line
program_filename = sys.argv[1]
​
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3   # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRN in the LS8
PUSH = 5
POP = 6
CALL = 7
RET = 8
​
"""
memory = [
	PRINT_BEEJ,
​
	SAVE_REG,    # SAVE R0,37   store 37 in R0      the opcode
	0,  # R0     operand ("argument")
	37, # 37     operand
​
	PRINT_BEEJ,
​
	PRINT_REG,  # PRINT_REG R0
	0, # R0
​
	HALT
]
"""
​
memory = [0] * 256
register = [0] * 8   # like variables R0-R7
​
# R7 is the SP. SP contains the address of the code at top of stack
## INITIAL CODE ##
# register[7] = 0xF4
SP = 7  # replace register[7] with register[SP] throughout code
register[SP] = 0xF4
​
# Load program into memory
address = 0
​
with open(program_filename) as f:  # f = file handle
	for line in f:
		line = line.split('#')  # remove comments 
		line = line[0].strip()  # remove whitespace
​
		if line == '':
			continue
​
		memory[address] = int(line)  # convert string to int
​
		address += 1  # move to next line
​
#print(type(memory[0]))
#sys.exit()
​
pc = 0 # Program Counter, the address of the current instruction
running = True
​
while running:
	inst = memory[pc]
​
	if inst == PRINT_BEEJ:
		print("Beej!")
		pc += 1
​
	elif inst == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3
​
	elif inst == PRINT_REG:
		reg_num = memory[pc + 1]
		value = register[reg_num]
		print(value)
		pc += 2

	elif inst == PUSH:  # Coded to specifically push a register value
		## INITIAL VERSION ##
		# register[7] -= 1  # decrement the SP
		# reg_num = memory[pc + 1]  # copy value from register to memory
		# value = register[reg_num]  # this is what we want to push
		# address = register[7]
		# memory[address] = 7  # store the value on the stack
		# pc += 2  # increment pc

		# decrement the stack pointer (so if SP starts at F3 --> F2)
		register[SP] -= 1   # address_of_the_top_of_stack -= 1
​
		# copy value from register into memory
		reg_num = memory[pc + 1]
		value = register[reg_num]  # this is what we want to push
​
		address = register[SP]    # addr of the new top of that stack
		memory[address] = value   # store the value on the stack
​
		pc += 2
​
	elif inst == POP:
		# copy value from register into memory
		reg_num = memory[pc + 1]
​
		address = register[SP]   # addr of item on the top of the stack
		value = memory[address]  # this is the value we popped
​
		register[reg_num] = value   # store the value in the register
​
		pc += 2
​
		# increment the stack pointer
		register[SP] += 1   # address_of_the_top_of_stack -= 1
​
	elif inst == CALL:  # Can't use PUSH b/c don't want to push a reg val
		# compute return address
		return_addr = pc + 2
​
		# push on the stack
		register[SP] -= 1
		memory[register[SP]] = return_addr
​
		# Set the PC to the value in the given register
		reg_num = memory[pc + 1]  # Get the value out of given register from memory
		dest_addr = register[reg_num]  # Where we're calling to
​
		pc = dest_addr  # call it. NOT incrementing PC
​
	elif inst == RET:
		# pop return address from top of stack
		return_addr = memory[register[SP]]
		register[SP] += 1  # increment SP
​
		# Set the pc to return address
		pc = return_addr
​
	elif inst == HALT:
		running = False
​
	else:
		print("Unknown instruction")
		running = False
