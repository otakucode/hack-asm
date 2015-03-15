__author__ = 'otakucode'

class HackCommandType:
    """Pseudo-enum used to indicate the type of command."""
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

class A_Command:
    """A commands are used to set the A register of the Hack CPU and indicate
       a 'working' address which is used when accessing memory."""
    def __init__(self, address):
        self.command_type = HackCommandType.A_COMMAND
        self.address = address



class L_Command:
    """L commands are really pseudo-commands which simply define a label which can be used in jump commands.
       L commands generate no actual instructions."""
    def __init__(self, label, rom_address):
        self.command_type = HackCommandType.L_COMMAND
        self.label = label
        self.rom_address = rom_address



class C_Command:
    """C commands are the commands that actually do all the work.  They control the Hack CPU to perform
       computations on the ALU and manipulate memory and registers."""
    def __init__(self, dest, comp, jump):
        self.command_type = HackCommandType.C_COMMAND
        self.dest = dest
        self.comp = comp
        self.jump = jump

