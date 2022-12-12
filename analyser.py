from base import prod_actions, productions, grammar_tree
import re

mid_code = []
nextquad = 100

def emit(expr, t1, t2, s1):
    mid_code.append((expr,t1,t2,s1))

def makelist(i):
    return [i]

def analysis(id, last_oper):
    global nextquad
    node = grammar_tree[id]
    for lst in prod_actions[last_oper]:
        if lst != 'pass':
            lst = re.sub(r'\.(\w+)',lambda x: "['{}']".format(x.group(1)), lst)#翻译 将.val 翻成['val']
            lst = re.sub(r'@l',"node", lst) #翻译 将@l 翻成实际左边元素
            lst = re.sub(r'@r(\d+)',lambda x: "grammar_tree[{}]".format(node['son'][int(x.group(1))]), lst) #翻译 将@r1 翻译为实际右边元素
            print(lst)
            exec(lst)
    return True