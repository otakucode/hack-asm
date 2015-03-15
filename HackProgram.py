__author__ = 'otakucode'

from SymbolTable import SymbolTable
from HackAssemblyCommands import HackCommandType, A_Command, L_Command, C_Command
from pyparsing import Word, ZeroOrMore, OneOrMore, OnlyOnce, Literal, Optional, oneOf, dblSlashComment
import string

class HackProgram:
    dest_dict = {'' : '000',
                  'M=' : '001',
                  'D=' : '010',
                  'MD=' : '011',
                  'A=' : '100',
                  'AM=' : '101',
                  'AD=' : '110',
                  'AMD=' : '111'}
    comp_dict = {'0' : '0101010',
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
    jump_dict = {'' : '000',
                  ';JGT' : '001',
                  ';JEQ' : '010',
                  ';JGE' : '011',
                  ';JLT' : '100',
                  ';JNE' : '101',
                  ';JLE' : '110',
                  ';JMP' : '111'}

    def __init__(self):
        self.symbols = SymbolTable()
        self.command_list = []
        self.next_variable_address = 16
        self.machine_code = []

    def ParseAssembly(self, text):
        start_symbol_char = string.ascii_letters + '_.$:'
        symbol_char = string.ascii_letters + string.digits + '_.$:'
        symbol_name = Word(start_symbol_char, symbol_char)

        positive_number = Word(string.digits)
        minus = Literal('-')
        negative_number = minus + positive_number
        number = (negative_number ^ positive_number)

        address = (positive_number ^ symbol_name)
        start_a_command = '@'
        a_command = start_a_command + address("ADDRESS")

        start_l_command = '('
        end_l_command = ')'
        l_command = start_l_command + symbol_name("LABEL") + end_l_command

        dest = oneOf(list(self.dest_dict.keys()))
        comp = oneOf(list(self.comp_dict.keys()))
        jump = oneOf(list(self.jump_dict.keys()))
        c_command = Optional(dest, default='')("DEST") + comp("COMP") + Optional(jump, default='')("JUMP")

        comment_line = dblSlashComment
        command_line = (a_command("A_CMD") ^ l_command("L_CMD") ^ c_command("C_CMD")) + Optional(dblSlashComment)
        code_line = command_line ^ comment_line

        self.rom_location = 0

        for line in text:
            line = line.rstrip()
            if len(line) == 0:    # Skip blank lines
                continue
            result = code_line.parseString(line)
            if "A_CMD" in result:
                self.rom_location += 1
                self.command_list.append(A_Command(result.ADDRESS))

            elif "L_CMD" in result:
                self.command_list.append(L_Command(result.LABEL, self.rom_location))
                self.symbols.addEntry(result.LABEL, self.rom_location)
            elif "C_CMD" in result:
                self.rom_location += 1
                self.command_list.append(C_Command(result.DEST, result.COMP, result.JUMP))



    def ParseMachineCode(self, code):
        pass

    def EmitAssembly(self):
        pass



    def EmitMachineCode(self):
        for cmd in self.command_list:
            if cmd.command_type == HackCommandType.A_COMMAND:
                if not cmd.address.isnumeric():
                    if self.symbols.contains(cmd.address):
                        addressval = self.symbols.GetAddress(cmd.address)
                    else:
                        if not self.symbols.contains(cmd.address):
                            self.symbols.addEntry(cmd.address, self.next_variable_address)
                            self.next_variable_address += 1

                else:
                    addressval = int(cmd.address)
                out = '0' + '{0:015b}\n'.format(addressval)
                self.machine_code.append(out)

            elif cmd.command_type == HackCommandType.L_COMMAND:
                continue

            elif cmd.command_type == HackCommandType.C_COMMAND:
                out = '111' + self.comp_dict[cmd.comp] + self.dest_dict[cmd.dest] + self.jump_dict[cmd.jump] + '\n'
                self.machine_code.append(out)

        return self.machine_code