__author__ = 'otakucode'


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
