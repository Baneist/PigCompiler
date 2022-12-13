from copy import deepcopy
import argparse
import json
#参数添加
parser = argparse.ArgumentParser(description='\033[1;34;34mPig Compiler for MIPSx54\033[0m')
parser.add_argument('src', type=str, nargs='?', default='input.c', help='Input File.')
parser.add_argument('-debug', type=int, default=0, help='Activate debug output.')
parser.add_argument('-output', type=str, default='a.s', help='Output File.')
args = parser.parse_args()

#词法分析BASE
#保留字表
s_code=['']
def getErrorCodeLine(l, p, str=''):
    return '\033[1;31;36m{}:{}\033[1;33;33m{}\033[1;31;36m{}\033[0m'.format(l,s_code[l][:p+1-len(str)], s_code[l][p+1-len(str):p+1], s_code[l][p+1:])
reserve_word = [ 
    ",", "!=", "==", "<",  "<=", "=",  ">", ">=", "=", 
    "*",  "+", "-", "/",  ";", "(",  ")", "{",  "}", ".", "&&",
    "else", "if", "int", "float", "return", "void", "while"
]
#另外增加的词法分析关键词
reserve_type = [
    "identifier", "digit_int", "digit_float"
]
w_dict = []
#词法分析辅助函数
def JudgeReverseWord(w):
    return '$'+w if w in reserve_word else -1
def isSymbol(c:str):
    if(c.isalpha() or c.isdigit() or c in [' ', '\n', '_']):
        return False
    return True

#语法分析器BASE
#产生式表
productions = []
prod_actions = []
project_set = []
action_goto={}

#json加载
with open('base.json', encoding='utf-8') as conf:
    cont = json.load(conf)
    for i in cont:
        productions.append(i['production'])
        prod_actions.append(i['action'])

symbol_list = {} #{符号:是否为终结符}
for w in reserve_word:
    symbol_list['$'+w] = 1
for w in reserve_type:
    symbol_list['$'+w] = 1
for p in productions:
    symbol_list[p['left']] = 0

def isTerminalSymbol(word):
    if word[0] in ['$', '#']:
        return True
    return False

first = {'#':['#']} #所有非终结符的first集，空集用'@'表示
def findSymbolFirst(sym):
    global first
    f=[] #初始化first集为空
    if sym in first: #如果它已经计算完毕，则直接返回
        f=deepcopy(first[sym])
        return f
    if isTerminalSymbol(sym): #如果他是终结符，直接返回它自己
        f.append(sym)
    else:
        for p in productions:
            if p['left'] == sym:#遍历每条从sym开始的产生式
                if len(p['right']) == 0: #如果它能推出空
                    f.append('@') #将空集加入
                elif isTerminalSymbol(p['right'][0]): #或者他是终结符
                    f.append(p['right'][0]) #将该终结符加入
                else:
                    for x in p['right']:
                        nf = findSymbolFirst(x) #递归求解其元素
                        if '@' in nf:#如果存在空集
                            nf.remove('@')#那么删除空集
                            f += nf
                        else:
                            f += nf
                            break
                    else:
                        f.append('@') #全部都含有空，将空集加入
    first[sym] = f #保存该元素值
    return f
for x in symbol_list: #求所有元素的first集
    findSymbolFirst(x)

grammar_tree=[] #[{'sym': 'S', 'son':[] , 'cont':''}]
def addGrammarTreeNode(sym, son_st, cont='', debug_pos=(0,0)): #添加树节点函数
    grammar_tree.append({'sym':sym, 'son':son_st, 'cont':cont, 'debug_pos': debug_pos})
    return len(grammar_tree) - 1

#语义分析参数
mid_code = []
nextquad = 100
list_dict = {
    'var': [],
    'func': [],
}