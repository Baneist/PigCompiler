reserve_word = [
",", "!=", "==", "<",  "<=", "=",  ">", ">=", "=", 
"*",  "+", "-", "/",  ";", "(",  ")", "{",  "}", ".", "&&",
"else", "if", "int", "float", "return", "void", "while"
]

w_dict = []

reserve_word_dict = dict()
for i, word in enumerate(reserve_word):
    reserve_word_dict[word] = i
def JudgeReverseWord(w):
    return reserve_word_dict[w] if w in reserve_word_dict else -1

class WordType():
    TYPE_WORD = 101
    TYPE_INT = 102
    TYPE_FLOAT = 103

def isSymbol(c:str):
    if(c.isalpha() or c.isdigit() or c in [' ', '\n', '_']):
        return False
    return True