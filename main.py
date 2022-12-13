from lexer import Lexer
from gparser import GParser
from syntaxTree import drawSyntaxTree
from base import args, mid_code

if __name__ == '__main__':
    try:
        with open(args.src, encoding='utf-8') as f:
            str = f.read()
            if Lexer(str) and GParser():
                print('\033[1;32;32m[Info]Compile success!\033[0m')
                #if(args.debug): 
                #drawSyntaxTree()
                print(mid_code)
    except FileNotFoundError as err:
        print('\033[1;31;31m[Error]#101\033[0m')
    if(args.debug): input("输入回车继续...")