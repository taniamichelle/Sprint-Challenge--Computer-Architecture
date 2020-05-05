"""CPU functionality."""

import sys

### OP CODES ###
LDI = 0b10000010
CALL = 0b01010000
RET = 0b00010001
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
PUSH = 0b01000101
POP = 0b1000110
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory

        self.register = [0] * 8  # 8 registers of 1-byte each

        self.pc = 0  # Program counter starting at 0th block of memory

        self.sp = 7  # SP is R7

        self.flag = 0

        self.methods_hash = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            ADD: self.ALU,
            MUL: self.ALU,
            SUB: self.ALU,
            PUSH: self.PUSH,
            POP: self.POP,
            CALL: self.CALL,
            RET: self.RET,
            CMP: self.ALU,
            JMP: self.JMP,
            JEQ: self.JEQ,
            JNE: self.JNE
        }
    
    def CALL(self):
        # Get address of next instruction
        reg = self.pc + 2
        # Push address of next instruction onto top of stack
        self.ram[self.sp] = reg
        # Decrement SP
        self.sp -= 1
        print("Self.pc 1: ", self.pc)
        # Set PC to the address stored in the given register (which causes us to jump to that location in RAM)

        self.pc = self.register[self.ram[self.pc + 1]]        
        print("Self.pc: ", self.pc)
        
        print("Register: ", self.register)
        # First instruction in the subroutine executes.
        
    def RET(self):
        # Increment SP
        self.sp += 1
        # Pop the value from the top of the stack 
        val = self.ram[self.sp]
        # Store value(address) in the PC
        self.pc = val

    def PUSH(self):
        '''
        Runs `PUSH`. Stack begins at address F3 and grows downward. SP points at value at top of stack or at F4 if stack is empty. Registers R0-R6 get pushed onto the stack in that order.
        '''
        # Grab register from reg argument
        reg = self.ram[self.pc + 1]
        val = self.register[reg]

        # Decrement SP
        self.register[self.sp] -= 1
        # print("sp end in push: ", self.sp)
        # Copy the value in the given register(from R0-R6) to the address pointed to by SP
        self.ram[self.register[self.sp]] = val
        self.pc += 2  # Comment out if using handle_pc function

    def POP(self):
        '''
        Runs `POP`. Registers R6-R0 are popped off the stack in that order.
        '''
        #  Grabs the value from memory at the top of stack.
        reg = self.ram[self.pc + 1]
        val = self.ram[self.register[self.sp]]

        # Copy the value from address pointed to by SP to the given register
        self.register[reg] = val
        # Increment SP
        self.register[self.sp] += 1
        # print("sp end in pop: ", self.sp)
        self.pc += 2  # comment out if using handle_pc function

    def LDI(self, operand_a, operand_b):
        '''
        Runs `LDI`, which sets the value of a register to an integer.
        '''
        self.register[operand_a] = operand_b  # Store value (op b) in reg 0 (op a)
        self.pc += 3

    def PRN(self, operand_a):
        '''
        Prints numeric value (decimal integer)stored in the given register to console.
        '''
        print("PRN: ", self.register[operand_a])
        self.pc += 2

    def HLT(self):
        '''
        Halts the CPU and exits the emulator.
        '''
        sys.exit()

    def JMP(self, register_a):
        '''
        Jump to the address stored in the given register.
        Set the PC to the address stored in the given register.
        '''
        self.pc = self.register[register_a]  # Set pc to register_a
    
    def JEQ(self, register_a):
        '''
        If equal flag is set (true), jump to the address stored 
        in the given register.
        '''
        if self.flag == 0b00000001:  # If equal flag
            self.JMP(register_a)
        else: 
            self.pc += 2  # Increment pc by 2

    def JNE(self, register_a):
        '''
        If E flag is clear (false, 0), jump to the address stored 
        in the given register.
        '''
        if self.flag == 0b00000010 or self.flag == 0b00000100:  # If flag < or >, respectively
            self.JMP(register_a)
        else:
            self.pc += 2

    def ram_read(self, MAR):
        '''
        Accepts the address to read and returns the value stored there.
        '''
        return self.ram[MAR]                  

    def ram_write(self, MAR, MDR):
        '''
        Accepts a value to write and the address to write it to.
        '''
        self.ram[MAR] = MDR

    def load(self):
        """Loads a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.strip().split("#")
                    value = comment_split[0].strip()
                    if value == "":
                        continue
                    num = int(value, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print("File not found.")
            sys.exit(2)

    def ALU(self, op, reg_a, reg_b):
        """
        ALU operations, including ADD, MUL, CMP.
        """

        if op == ADD:
            self.register[reg_a] += self.register[reg_b]
            self.pc += 3
        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
            self.pc += 3
        elif op == SUB: 
            self.register[reg_a] -= self.register[reg_b]
            self.pc += 3
        elif op == CMP:
            # set L (less-than) flag set to 1 if registerA is less than registerB, zero otherwise. 
            if self.register[reg_a] < self.register[reg_b]:
                self.flag = 0b00000010
            
            # set G (greater-than) flag set to 1 if registerA is greater than registerB, zero otherwise. 
            elif self.register[reg_a] < self.register[reg_b]:
                self.flag = 0b00000100
            
            # set E (equal) flag to 1 if registerA is equal to registerB, zero otherwise.
            elif self.register[reg_a] == self.register[reg_b]:
                self.flag = 0b00000001
            
            self.pc += 3  # Increment pc by 3
        else:
            raise Exception("Unsupported ALU operation.")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """
        Reads the memory address stored in `PC` 
        and stores the result in `IR`. Runs the CPU. 
        """

        while True:
            IR = self.pc
            op = self.ram_read(IR)
            
            operand_a = self.ram_read(IR + 1)  # Get operand_a
            operand_b = self.ram_read(IR + 2)  # Get operand_b
            
            if op in self.methods_hash:
                if op in [ADD, MUL, CMP]:
                    self.methods_hash[op](op, operand_a, operand_b)  # Invoke our methods_hash as a function w/ 2 operands
                elif op >> 6 == 0:
                    self.methods_hash[op]()  # Invoke our methods_hash as a function              
                elif op >> 6 == 1:
                    self.methods_hash[op](operand_a)  
                elif op >> 6 == 2:
                    self.methods_hash[op](operand_a, operand_b)  # Invoke our methods_hash as a function
            else:    
                print(f"Unknown instruction.")
                sys.exit(1)
