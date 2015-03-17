__author__ = 'otakucode'
# hack-asm - An assembler for the Hack architecture defined in the NAND2Tetris course.

import sys, os


builtin_symbols = {'SP' : 0,
                   'LCL' : 1,
                   'ARG' : 2,
                   'THIS' : 3,
                   'THAT' : 4,
                   'R0' : 0,
                   'R1' : 1,
                   'R2' : 2,
                   'R3' : 3,
                   'R4' : 4,
                   'R5' : 5,
                   'R6' : 6,
                   'R7' : 7,
                   'R8' : 8,
                   'R9' : 9,
                   'R10' : 10,
                   'R11' : 11,
                   'R12' : 12,
                   'R13' : 13,
                   'R14' : 14,
                   'R15' : 15,
                   'SCREEN' : 16384,
                   'KBD' : 24576 }

variable_starting_address = 16


class Parser():
    class CommandType:
        A_COMMAND, C_COMMAND, L_COMMAND = range(3)

    def __init__(self, filename):
        self.in_file = open(filename, 'r')
        self.next_line = self.in_file.readline()

    def hasMoreCommands(self):
        if self.next_line == '':
            return False
        else:
            return True

    def _remove_comment(self, line):
        if '//' in line:
             return line[0:line.find('//')]
        else:
            return line

    def _remove_whitespace(self, line):
        return line.replace(' ', '').replace('\t', '')

    def advance(self):
        # Parse the line, skipping all 'empty' lines if necessary

        while self._remove_whitespace(self._remove_comment(self.next_line.strip())) == '':
            self.next_line = self.in_file.readline()
            if self.next_line == '':
                return
        self.next_line = self._remove_whitespace(self._remove_comment(self.next_line.strip()))
        if self.next_line.startswith('@'):
            self.parse_a_command()
        elif self.next_line.startswith('('):
            self.parse_l_command()
        else:
            self.parse_c_command()
        self.next_line = self.in_file.readline()

    def parse_a_command(self):
        self.command = Parser.CommandType.A_COMMAND
        pstring = self.next_line[1:]
        self.csymbol = pstring

    def parse_l_command(self):
        self.command = Parser.CommandType.L_COMMAND
        pstring = self.next_line[1:-1]
        self.csymbol = pstring

    def parse_c_command(self):
        self.command = Parser.CommandType.C_COMMAND
        pstring = self.next_line
        self.cdest = self.ccomp = self.cjump = None
        if '=' in pstring:
            self.cdest = pstring[:pstring.find('=')]
            pstring = pstring[pstring.find('=') + 1:]
        if ';' in pstring:
            self.ccomp = pstring[:pstring.find(';')]
            pstring = pstring[pstring.find(';') + 1:]
            self.cjump = pstring
        else:
            self.ccomp = pstring

    def commandType(self):
        return self.command

    def symbol(self):
        return self.csymbol

    def dest(self):
        return self.cdest

    def comp(self):
        return self.ccomp

    def jump(self):
        return self.cjump


class Code:
    def __init__(self):
        self.dest_dict = {None : '000',
                          'M' : '001',
                          'D' : '010',
                          'MD' : '011',
                          'A' : '100',
                          'AM' : '101',
                          'AD' : '110',
                          'AMD' : '111'}
        self.comp_dict = {'0' : '0101010',
                          '1' : '0111111',
                          '-1' : '0111010',
                          'D' : '0001100',
                          'A' : '0110000',
                          'M' : '1110000',
                          '!D' : '0001101',
                          '!A' : '0110001',
                          '!M' : '1110001',
                          '-D' : '0001111',
                          '-A' : '0110011',
                          '-M' : '1110011',
                          'D+1' : '0011111',
                          'A+1' : '0110111',
                          'M+1' : '1110111',
                          'D-1' : '0001110',
                          'A-1' : '0110010',
                          'M-1' : '1110010',
                          'D+A' : '0000010',
                          'D+M' : '1000010',
                          'D-A' : '0010011',
                          'D-M' : '1010011',
                          'A-D' : '0000111',
                          'M-D' : '1000111',
                          'D&A' : '0000000',
                          'D&M' : '1000000',
                          'D|A' : '0010101',
                          'D|M' : '1010101'}
        self.jump_dict = {None : '000',
                          'JGT' : '001',
                          'JEQ' : '010',
                          'JGE' : '011',
                          'JLT' : '100',
                          'JNE' : '101',
                          'JLE' : '110',
                          'JMP' : '111'}

    def dest(self, mneumonic):
        if mneumonic in self.dest_dict:
            return self.dest_dict[mneumonic]
        else:
            print("Unsupported DEST: {0}".format(mneumonic))

    def comp(self, mneumonic):
        if mneumonic in self.comp_dict:
            return self.comp_dict[mneumonic]
        else:
            print("Unsupported COMP: {0}".format(mneumonic))

    def jump(self, mneumonic):
        if mneumonic in self.jump_dict:
            return self.jump_dict[mneumonic]
        else:
            print("Unsupported JUMP: {0}".format(mneumonic))

class HackAssembler:
    def __init__(self, in_file):
        self._in_file = in_file

    def assemble(self):
        self.symbol_table = SymbolTable()
        self._machine_code = []
        self.first_pass()
        self.second_pass()

    def first_pass(self):
        # Parse through input file and extract label symbols to the symbol table,
        # giving them the address in ROM they refer to.
        rom_location = 0
        parser = Parser(self._in_file)

        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == Parser.CommandType.C_COMMAND:
                rom_location += 1

            elif parser.commandType() == Parser.CommandType.A_COMMAND:
                rom_location += 1

            elif parser.commandType() == Parser.CommandType.L_COMMAND:
                self.symbol_table.addEntry(parser.symbol(), rom_location)


    def second_pass(self):
        self.next_variable_address = variable_starting_address
        parser = Parser(self._in_file)
        code = Code()
        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() == Parser.CommandType.C_COMMAND:
                out = '111' + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump()) + '\n'
                self._machine_code.append(out)
            elif parser.commandType() == Parser.CommandType.A_COMMAND:
                if parser.symbol().isnumeric():
                    # Address
                    out = '0' + '{0:015b}'.format(int(parser.symbol())) + '\n'
                    self._machine_code.append(out)
                else:
                    # Symbol
                    if not self.symbol_table.contains(parser.symbol()):
                        self.symbol_table.addEntry(parser.symbol(), self.next_variable_address)
                        self.next_variable_address += 1

                    out = '0' + '{0:015b}\n'.format(self.symbol_table.GetAddress(parser.symbol()))
                    self._machine_code.append(out)

            elif parser.commandType() == Parser.CommandType.L_COMMAND:
                # Label line
                pass

    def assembled_output(self):
        return self._machine_code


class SymbolTable:
    def __init__(self):
        self._symbol_dict = {}
        self._symbol_dict.update(builtin_symbols)

    def addEntry(self, symbol, address):
        if symbol in self._symbol_dict:
            print("Attempted redefinition of symbol: {0}".format(symbol))
        else:
            self._symbol_dict[symbol] = address

    def contains(self, symbol):
        return symbol in self._symbol_dict

    def GetAddress(self, symbol):
        return self._symbol_dict[symbol]



if __name__ == '__main__':
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("Specified source file does not exist.")
        exit()
    asm = HackAssembler(input_file)
    asm.assemble()
    output_file = input_file.replace('.asm', '.hack')
    with open(output_file, 'w') as out_file:
        out_file.writelines(asm.assembled_output())

    print('Success.')
