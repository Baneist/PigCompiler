from base import productions, project_set, symbol_list, isTerminalSymbol, action_goto, findSymbolFirst, w_dict, grammar_tree, addGrammarTreeNode
from copy import deepcopy

def findFirst(sym_list):
    f=[]
    for x in sym_list:
        nf = findSymbolFirst(x)
        if '@' in nf:#如果存在空集
            nf.remove('@')
            f += nf
        else:
            f += nf
            break
    return f

def findClosure(parent:list)->list:
    top = 0
    closure_set=deepcopy(parent)
    while top < len(closure_set):
        nowc = closure_set[top]
        pos = nowc['dot']
        if pos < len(nowc['right']) and not isTerminalSymbol(nowc['right'][pos]):#如果是非终结符，进行拓展
            follow_symbol = deepcopy(nowc['right'][pos+1:]) if pos < len(nowc) - 1 else []#后面用于求first集的子串
            follow_symbol.append(nowc['accept'])
            new_accept_set = findFirst(follow_symbol)
            for p in productions:
                if p['left'] == nowc['right'][pos]:#求到新拓展项目,添加入closure集中
                    for nas in new_accept_set:
                        newp = deepcopy(p)
                        newp['dot'] = 0
                        newp['accept'] = nas
                        if not newp in closure_set:#去重
                            closure_set.append(newp)
        top += 1
    return closure_set

def findGoto(proj, sym)->list:
    c = []
    for p in proj:
        if p['dot'] != len(p['right']) and p['right'][p['dot']] == sym:
            np = deepcopy(p)
            np['dot'] += 1
            c.append(np)
    return findClosure(c)

def initProjectSet():
    start = deepcopy(productions[0])
    start['dot'], start['accept'] = 0, '#'#生成初始集合
    c = findClosure([start])
    project_set.append(c)
    top = 0 #递归调用计算
    while top < len(project_set):
        for x in symbol_list:
            next_set = findGoto(project_set[top], x)
            if len(next_set) > 0 and not next_set in project_set:#将新构造的集合放入项目簇中
                project_set.append(next_set)
            #if len(next_set) > 0: 调试语句
            #    print("#{}=<{},{}>:".format(project_set.index(next_set), top, x), next_set)
            if len(next_set) > 0:
                if not isTerminalSymbol(x):
                    action_goto[(top,x)] = ['g', project_set.index(next_set)]
                else: #处理移进项目
                    action_goto[(top, x)] = ['s', project_set.index(next_set)]
        for wt in project_set[top]:
            if wt['dot'] == len(wt['right']):#处理规约项目
                ns = {'left':wt['left'], 'right':wt['right']}
                action_goto[(top, wt['accept'])] = ['r', productions.index(ns)] if ns['left'] != '<开始>' else ['acc']
        top += 1   

def Parser():
    initProjectSet()
    input_st = ['#'] + w_dict[::-1]
    state_st, sym_st, id_st, son_st = [0], ['#'], [], []
    try:
        while len(input_st) > 0:
            ns = (state_st[len(state_st)-1], input_st[len(input_st)-1][0])#当前状态的元组
            t = action_goto.get(ns)
            if not t:
                raise Exception('[Error]#201 in line {}, position {}: Unexpected word \'{}\' after \'{}\'.'.format(*input_st[len(input_st)-1][2], input_st[len(input_st)-1][1], sym_st.pop()))
            if t[0] == 's' or t[0] == 'g': #移进或者goto,两者代码相同
                sym_st.append(input_st.pop()[0])
                state_st.append(t[1])
                id_st.append(addGrammarTreeNode(sym_st[-1], son_st))
                son_st = []
            elif t[0] == 'r': #规约
                #print("规约:", productions[t[1]])
                for i in range(len(productions[t[1]]['right'])): #如果不是从空串规约而来，设置子节点
                    sym_st.pop()
                    state_st.pop()
                    son_st.append(id_st.pop())
                if len(productions[t[1]]['right']) == 0: #如果是空串,额外添加ε
                    son_st.append(addGrammarTreeNode('ε', []))
                input_st.append([productions[t[1]]['left']])
            else:#规约成功 acc
                print("[Info] Garmmar analysis success!")
                break
    except Exception as err:
        print(str(err))
        return False
    return True