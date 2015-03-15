__author__ = 'otakucode'

import re
import ply.lex as lex


dest_dict = {None : '000',
              'M' : '001',
              'D' : '010',
              'MD' : '011',
              'A' : '100',
              'AM' : '101',
              'AD' : '110',
              'AMD' : '111'}

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

jump_dict = {None : '000',
              'JGT' : '001',
              'JEQ' : '010',
              'JGE' : '011',
              'JLT' : '100',
              'JNE' : '101',
              'JLE' : '110',
              'JMP' : '111'}


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AT = r'@'
t_SYMBOL = r'[a-zA-Z\.:_\$][a-zA-Z\.:_$0-9]*'
t_EQUAL = r'='
t_SEMICOLON = r';'
dest_tokens = list(dest_dict.keys())
dest_tokens.remove(None)
dest_tokens.sort()
dest_tokens.reverse()
t_DEST = r'(' + '|'.join([re.escape(k) for k in dest_tokens if k is not None]) + ')'
comp_tokens = list(comp_dict.keys())
comp_tokens.sort()
comp_tokens.reverse()
t_COMP = r'(' + '|'.join([re.escape(k) for k in comp_tokens]) + ')'
jump_tokens = list(jump_dict.keys())
jump_tokens.remove(None)
jump_tokens.sort()
jump_tokens.reverse()
t_JUMP = r'(' + '|'.join([re.escape(k) for k in jump_tokens if k is not None]) + ')'
t_COMMENT = r'//.*'

t_ignore = ' \t\n'

def t_ADDRESS(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character '{0}'".format(t.value[0]))
    t.lexer.skip(1)




tokens = (
    'LPAREN',
    'RPAREN',
    'AT',
    'SYMBOL',
    'ADDRESS',
    'EQUAL',
    'SEMICOLON',
    'DEST',
    'COMP',
    'JUMP',
    'COMMENT'
)


def build_lexer():
    return lex.lex()

