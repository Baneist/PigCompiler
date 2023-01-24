from base import prod_actions, productions, grammar_tree, getErrorCodeLine, args
from base import nextquad, mid_code, list_dict as ldict
import re

#故障处理函数
def checkFuncDefined(name, node):
    if name not in ldict['func']:
        raise Exception('\033[1;31;31m[Error]#301 in line {}, position {}: Function name <{}> not defined.\n{}'.format(*node['debug_pos'], name, getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkFuncNotDefined(name, node):
    if name in ldict['func']:
        raise Exception('\033[1;31;31m[Error]#302 in line {}, position {}: Function name <{}> has already defined.\n{}'.format(*node['debug_pos'], name, getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkVarDefined(name,func,node):
    var_list = [x[0] for x in ldict['var'] if x[2] == '$global' or x[2] == func]
    if name not in var_list:
        raise Exception('\033[1;31;31m[Error]#303 in line {}, position {}: Variable name <{}> not defined.\n{}'.format(*node['debug_pos'], name, getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkVarNotDefined(name,func,node):
    var_list = [x[0] for x in ldict['var'] if x[2] == func]
    if name in var_list:
        raise Exception('\033[1;31;31m[Error]#304 in line {}, position {}: Variable name <{}> has already defined.\n{}'.format(*node['debug_pos'], name, getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkHasReturn(fname, node):
    if ldict['return'] == 0:
        raise Exception('\033[1;31;31m[Error]#305 in line {}, position {}: Function <{}> doesn\'t have return statement.\n{}'.format(*node['debug_pos'], fname, getErrorCodeLine(*node['debug_pos'], node['cont'])))

def checkFuncParNum(fname, num, node):
    if ldict['func'][fname] != num:
        raise Exception('\033[1;31;31m[Error]#306 in line {}, position {}: Call <{}> mismatch parameters, need {} but give {}.\n{}'.format(*node['debug_pos'], fname,ldict['func'][fname],num,getErrorCodeLine(*node['debug_pos'], node['cont'])))

def WarningVarType(type1,type2,node):
    if maxType(type1, type1, 0) < maxType(type2, type2, 0):
        print('\033[1;31;35m[Warning]#101 in line {}, position {}: Potential type downgrading <{}> to <{}>.\n{}'.format(*node['debug_pos'],type2,type1,getErrorCodeLine(*node['debug_pos'], node['cont'])))

def WarningVoid(node):
    print('\033[1;31;35m[Warning]#102 in line {}, position {}: Type <void> should not be used.\n{}'.format(*node['debug_pos'],getErrorCodeLine(*node['debug_pos'], node['cont'])))
#工作函数
def emit(expr, t1, t2, s1):
    global nextquad
    nextquad += 1
    mid_code.append((expr,t1,t2,s1))

#回填函数
def backFill(no, tup):
    a = list(mid_code[no-100])
    for i in range(4):
        if tup[i] is not None:
            a[i] = tup[i]
    mid_code[no-100] = (a[0],a[1],a[2],a[3])

var_num = 0
def newVar(type): #新建一个普通变量
    global var_num
    name = 'tmp_' + str(var_num)
    var_num += 1
    ldict['var'].append((name, 4, ldict['nowfunc'], type))
    return name

def maxType(a , b, tostr=True):
    type = ['void', 'int', 'float']
    return type[max(type.index(a), type.index(b))] if tostr else max(type.index(a), type.index(b))

def makelist(i): #生成布尔表达式的链
    return [i]

def mergelist(a, b): #将布尔表达式的两个链合并
    for i in b:
        if i not in a:
            a.append(i)
    return a

def batchlist(li, no):#li：需要串联的链 no：链接上的语句号
    for i in li:
        backFill(i, (None,None,None, no))

def analysis(id, last_oper):
    for lst in prod_actions[last_oper]:
        if lst != 'pass':
            if args.analysis_output: print(lst) #输出当前执行的语句
            lst = re.sub(r'\.(\w+)',lambda x: "['{}']".format(x.group(1)), lst)#翻译 将.val 翻成['val']
            lst = re.sub(r'@l',"grammar_tree[id]", lst) #翻译 将@l 翻成实际左边元素
            lst = re.sub(r'@r(\d+)',lambda x: "grammar_tree[{}]".format(grammar_tree[id]['son'][int(x.group(1))]), lst) #翻译 将@r1 翻译为实际右边元素
            lst = re.sub(r'->','.', lst)#翻译 将-> 翻成.
            try:
                exec(lst)
            except Exception as err:
                print(err)
                return False
    return True

def getVarType(var):
    save = None
    for t in ldict['var']:
        if t[0] == var:
            if t[2] == ldict['nowfunc']:
                return t[3]
            elif t[2] == '$global':
                save = t[3]
    return save

def midCodeSave(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        lst = ['中间代码:\n'] + ['{}: {}\n'.format(i+100, mid_code[i]) for i in range(len(mid_code))] + ['变量表:\n']
        a=[]; cnt=0
        for i,j in enumerate(ldict['var']):
            a.append(cnt)
            cnt += j[1]
        lst += ['{}: {}\n'.format(a[i], j) for i,j in enumerate(ldict['var'])]
        f.writelines(lst)
