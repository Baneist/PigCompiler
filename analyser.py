from base import prod_actions, productions, grammar_tree, getErrorCodeLine
from base import nextquad, mid_code, list_dict as ldict
import re

#故障处理函数
def checkFuncDefined(name, node):
    if name not in ldict['func']:
        raise Exception('\033[1;31;31m[Error]#301 in line {}, position {}: Function name <{}> not defined.\n{}'.format(*node['debug_pos'],name,getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkFuncNotDefined(name, node):
    if name in ldict['func']:
        raise Exception('\033[1;31;31m[Error]#302 in line {}, position {}: Function name <{}> has already defined.\n{}'.format(*node['debug_pos'],name,getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkVarDefined(name, node):
    var_list = [x[0] for x in ldict['var']]
    if name not in var_list:
        raise Exception('\033[1;31;31m[Error]#303 in line {}, position {}: Variable name <{}> not defined.\n{}'.format(*node['debug_pos'],name,getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkVarNotDefined(name, node):
    var_list = [x[0] for x in ldict['var']]
    if name in var_list:
        raise Exception('\033[1;31;31m[Error]#304 in line {}, position {}: Variable name <{}> has already defined.\n{}'.format(*node['debug_pos'],name,getErrorCodeLine(*node['debug_pos'], node['cont'])))

#工作函数
def emit(expr, t1, t2, s1):
    mid_code.append((expr,t1,t2,s1))

#回填函数
def MidCodeFill(no, pos, name):
    mid_code[no-100][pos] = name

var_num = 0
def newVar():
    global var_num
    name = 'tmp_' + str(var_num)
    var_num += 1
    return name



def analysis(id, last_oper):
    for lst in prod_actions[last_oper]:
        if lst != 'pass':
            lst = re.sub(r'\.(\w+)',lambda x: "['{}']".format(x.group(1)), lst)#翻译 将.val 翻成['val']
            lst = re.sub(r'@l',"grammar_tree[id]", lst) #翻译 将@l 翻成实际左边元素
            lst = re.sub(r'@r(\d+)',lambda x: "grammar_tree[{}]".format(grammar_tree[id]['son'][int(x.group(1))]), lst) #翻译 将@r1 翻译为实际右边元素
            lst = re.sub(r'->','.', lst)#翻译 将-> 翻成.
            print(lst)
            try:
                exec(lst)
            except Exception as err:
                print(err)
                return False
    return True