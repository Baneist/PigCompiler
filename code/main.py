from lexer import Lexer
from gparser import GParser
from analyser import midCodeSave
from syntax import drawSyntaxTree
from base import args, mid_code
from colorama import init
from generator import genCode

if __name__ == '__main__':
    init(autoreset=True)
    try:
        with open(args.src, encoding='utf-8') as f:
            str = f.read()
            if Lexer(str) and GParser() and genCode():
                midCodeSave(args.output)
                print('\033[1;32;32m[Info]Compile success!\033[0m')
                #print('中间代码已输出到同级文件夹下..')
                if(args.tree): 
                    drawSyntaxTree()
                    #print('中间代码为:', mid_code)
    except FileNotFoundError as err:
        print('\033[1;31;31m[Error]#101\033[0m')
    #input("输入回车继续...")