from lexer import Lexer
from parser import Parser
from base import grammar_tree

if __name__ == '__main__':
    src = 'test.c'
    with open(src, encoding='utf-8') as f:
        str = f.read()
        if Lexer(str) and Parser():
            print(grammar_tree)
            print('[Info]Compile success!')