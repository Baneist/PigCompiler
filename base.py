#词法分析BASE
#保留字表
reserve_word = [ 
    ",", "!=", "==", "<",  "<=", "=",  ">", ">=", "=", 
    "*",  "+", "-", "/",  ";", "(",  ")", "{",  "}", ".", "&&",
    "else", "if", "int", "float", "return", "void", "while"
]
#另外增加的 $identifier $digit_int
w_dict = [] #
def JudgeReverseWord(w):
    return '$'+w if w in reserve_word else -1

def isSymbol(c:str):
    if(c.isalpha() or c.isdigit() or c in [' ', '\n', '_']):
        return False
    return True

#语法分析器BASE
#产生式表
production = [
    {'left': '<开始>', 'right': ['<程序>']},
    {'left': '<程序>', 'right': ['<类型>','$identifier','$(', '$)', '<语句块>']},
    {'left': '<类型>', 'right': ['$int']},
    {'left': '<类型>', 'right': ['$void']},
    {'left': '<语句块>', 'right': ['${','<内部声明>','<语句串>','$}']},
    {'left': '<内部声明>', 'right': []},#这里略作修改
    {'left': '<内部声明>', 'right': ['<内部变量声明>', '$;', '<内部声明>']},
    {'left': '<内部变量声明>', 'right': ['$int', '$identifier']},
    {'left': '<语句串>', 'right': []},
    {'left': '<语句串>', 'right': ['<语句>', '<语句串>']},
    {'left': '<语句>', 'right': ['<if语句>']},
    {'left': '<语句>', 'right': ['<while语句>']},
    {'left': '<语句>', 'right': ['<return语句>']},
    {'left': '<语句>', 'right': ['<赋值语句>']},
    {'left': '<赋值语句>', 'right': ['$identifier', '$=', '<表达式>', '$;']},
    {'left': '<return语句>', 'right': ['return','<return内容>',';']},#这里略作修改
    {'left': '<return内容>', 'right': []},
    {'left': '<return内容>', 'right': ['<表达式>']},
    {'left': '<while语句>', 'right': ['$while', '$(', '<表达式>', '$)', '<语句块>']},
    {'left': '<if语句>', 'right': ['$if', '$(', '<表达式>', '$)', '<语句块>', '<else内容>']},
    {'left': '<else内容>', 'right': []},
    {'left': '<else内容>', 'right': ['$else', '<语句块>']},
    {'left': '<表达式>', 'right': ['<加法表达式>', '<拓展表达式>']},
    {'left': '<拓展表达式>', 'right': []},
    {'left': '<拓展表达式>', 'right': ['<比较符号>', '<加法表达式>', '<拓展表达式>']},
    {'left': '<比较符号>', 'right': ['$<']},
    {'left': '<比较符号>', 'right': ['$<=']},
    {'left': '<比较符号>', 'right': ['$>']},
    {'left': '<比较符号>', 'right': ['$>=']},
    {'left': '<比较符号>', 'right': ['$==']},
    {'left': '<比较符号>', 'right': ['$!=']},
    {'left': '<加法表达式>', 'right': ['<项>', '<加法表达式追加>']},
    {'left': '<加法表达式追加>', 'right': []},
    {'left': '<加法表达式追加>', 'right': ['$+' ,'<项>', '<加法表达式追加>']},
    {'left': '<加法表达式追加>', 'right': ['$-' ,'<项>', '<加法表达式追加>']},
    {'left': '<项>', 'right': ['<因子>', '<项追加>']},
    {'left': '<项追加>', 'right': ['$*' ,'<因子>', '<项追加>']},
    {'left': '<项追加>', 'right': ['$/' ,'<因子>', '<项追加>']},
    {'left': '<因子>', 'right': ['$digit_int']},
    {'left': '<因子>', 'right': ['$identifier', '<FTYPE>']},
    {'left': '<因子>', 'right': ['$(','<表达式>','$)']},
    {'left': '<FTYPE>', 'right': []},
    {'left': '<FTYPE>', 'right': ['<函数调用>']},
    {'left': '<函数调用>', 'right': ['$(','<实参列表>','$)']},
    {'left': '<实参列表>', 'right': []},
    {'left': '<实参列表>', 'right': ['<表达式>', '<追加实参列表>']},
    {'left': '<追加实参列表>', 'right': []},
    {'left': '<追加实参列表>', 'right': ['$,','<表达式>', '<追加实参列表>']}
]
def isTerminalSymbol(word):
    if word[0] in ['$', '#']:
        return True
    return False

project_set = []

'''
project = []
for sent in production: #生成所有项目集
    for i in range(len(sent['right'])+1):

新项目 = []  # {'left': "S'", 'right': ['S'], 'point': 0, "origin": 0, "accept": "#"}
'''   
