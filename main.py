from lexer import Lexer
from base import w_dict

if __name__ == '__main__':
    src = 'test.c'
    with open(src, encoding='utf-8') as f:
        str = f.read()
        Lexer(str)
        print(w_dict)