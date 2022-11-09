from lexer import Lexer
from gparser import GParser
from base import grammar_tree
from syntaxTree import drawSyntaxTree

if __name__ == '__main__':
    src = 'input.c'
    with open(src, encoding='utf-8') as f:
        str = f.read()
        if Lexer(str) and GParser():
            print(grammar_tree)
            print('[Info]Compile success!')
            drawSyntaxTree()