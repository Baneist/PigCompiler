from lexer import Lexer
from gparser import GParser
from analyser import codeSave
from syntax import drawSyntaxTree
from base import args, mid_code
from colorama import init
from generator import Generator

if __name__ == '__main__':
    init(autoreset=True)
    try:
        with open(args.src, encoding='utf-8') as f:
            str = f.read()
            if Lexer(str) and GParser() and Generator():
                codeSave(args.output)
                print('\033[1;32;32m[Info]Compile success!\033[0m')
                if(args.tree): 
                    drawSyntaxTree()
    except FileNotFoundError as err:
        print('\033[1;31;31m[Error]#101\033[0m')
