from lexer import Lexer
from parser import Parser
from base import w_dict

if __name__ == '__main__':
    src = 'test.c'
    with open(src, encoding='utf-8') as f:
        str = f.read()
        if Lexer(str) and Parser():
            print('[Info]Compile success!')