# hack-asm4 : An attempt at a Hack assembly language parser using pyparsing

__author__ = 'otakucode'

from HackProgram import HackProgram
import sys, os

# TODO: Update to use argparse in order to make improvements easier.
if len(sys.argv) != 2:
    print("Supply name of assembly source file.")
    exit()

if not os.path.exists(sys.argv[1]):
    print("Source file not found.")
    exit()

with open(sys.argv[1]) as infile:
    program = HackProgram()
    program.ParseAssembly([line.rstrip() for line in infile.readlines()])
    result = program.EmitMachineCode()

with open(sys.argv[1].replace('.asm', '.hack'), 'w') as outfile:
    outfile.write(''.join(result))

