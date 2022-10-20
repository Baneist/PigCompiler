from parser import parser

if __name__ == '__main__':
    src = 'test.c'
    with open(src, encoding='utf-8') as f:
        str = f.read()
        parser(str)
