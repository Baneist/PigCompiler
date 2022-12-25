from base import args, productions, project_set, symbol_list, isTerminalSymbol, action_goto, findSymbolFirst, w_dict, grammar_tree, addGrammarTreeNode, getErrorCodeLine, P2LR0
from analyser import analysis
from copy import deepcopy

def findFirst(sym_list): #找到一个符号串的first集
    f=[]
    for x in sym_list: #依次遍历符号串的每个元素
        nf = findSymbolFirst(x)
        if '@' in nf:#如果存在空集
            nf.remove('@')
            f += nf #将空集删除并将其加入first集，继续遍历
        else:
            f += nf #将其加入first集并终止遍历
            break
    return f #返回计算得到的first集

def findClosure(parent:list)->list: #输入一个项目簇,将其扩充成其closure闭包
    top = 0
    closure_set=deepcopy(parent) #先将闭包初始设置为输入的项目簇
    while top < len(closure_set): #不断对闭包里的每一个元素进行遍历
        nowc = closure_set[top]
        pos = nowc['dot'] #记录当前项目的dot位置
        if pos < len(nowc['right']) and not isTerminalSymbol(nowc['right'][pos]): #如果是非终结符，进行拓展
            follow_symbol = deepcopy(nowc['right'][pos+1:]) if pos < len(nowc) - 1 else [] #构造后面用于求first集的子串
            follow_symbol.append(nowc['accept']) #再将展望串放在最后
            new_accept_set = findFirst(follow_symbol) #计算新的展望串
            for p in productions:
                if p['left'] == nowc['right'][pos]: #求到新拓展项目,添加入closure集中
                    for nas in new_accept_set: #遍历展望串各元素，都要添加入closure集
                        newp = deepcopy(p)
                        newp['dot'], newp['accept'] = 0, nas
                        if not newp in closure_set:#进行元组去重，避免重复元素添加
                            closure_set.append(newp)
        top += 1
    return closure_set

def findGoto(proj, sym)->list: #通过输入的项目集和sym找其goto后的closure集
    c = [] #设置初始goto集为空
    for p in proj: #对于输入的每一个串,都尝试能否接受sym符号
        if p['dot'] != len(p['right']) and p['right'][p['dot']] == sym:
            np = deepcopy(p)
            np['dot'] += 1
            c.append(np) #如果可以接受,将其接受后的新串加入goto集中
    return findClosure(c) #计算计算后的goto集的闭包

debug_ = []

def initProjectSet():
    rset = ['']
    start = deepcopy(productions[0])
    start['dot'], start['accept'] = 0, '#'#生成初始集合
    c = findClosure([start]) #求解初始集合的闭包并加入有效项目集中
    project_set.append(c)
    top = 0 #递归调用计算
    while top < len(project_set): #采用广度优先搜索方式进行搜索
        for x in symbol_list: #对每一个正在被搜索的状态集：
            next_set = findGoto(project_set[top], x)
            if len(next_set) > 0 and not next_set in project_set:#将新构造的集合放入项目簇中
                project_set.append(next_set); rset.append(rset[top]+x);
            if len(next_set) > 0: debug_.append("#{}=<{},{}>:{}\n".format(project_set.index(next_set), top, x,next_set))
            if len(next_set) > 0 and project_set.index(next_set) == 120: print(next_set)
            if len(next_set) > 0:
                t = action_goto.get((top, x))
                if t is not None:
                    print("工程错误: 移进项目冲突,状态号为#{} #{},接受字符为 {} .\n".format(t[0], project_set.index(next_set), x))
                action_goto[(top,x)] = ['g' if not isTerminalSymbol(x) else 's', project_set.index(next_set)] #如果x不是终结符，那么填goto集, 否则填在移进集
        for wt in project_set[top]:
            if wt['dot'] == len(wt['right']):#遍历next集中的规约项目
                ns = {'left':wt['left'], 'right':wt['right']} #将action_goto集的accept位设为规约
                t = action_goto.get((top, wt['accept']))
                if t is None:#正确填入
                    action_goto[(top, wt['accept'])] = ['r', productions.index(ns)] if ns['left'] != '<开始>' else ['acc']
                elif t[0] == 'r': #两个规约项目冲突：
                    raise Exception("工程错误: 规约项目冲突,接受字符为 {} .\n{}\n{}".format(wt['accept'], productions[t[1]], ns))
                else:
                    #action_goto[(top, wt['accept'])] = ['r', productions.index(ns)] if ns['left'] != '<开始>' else ['acc']
                    #print("工程错误: 现状态#{} 规约与移进状态#{}冲突\n#{} :接受字符为{}.\n{}\n{}".format(top, t[1],rset[top],wt['accept'], ns, P2LR0(project_set[t[1]])))
                    pass
        top += 1 #选取下一个集合进行操作

def GParser():
    initProjectSet() #初始化项目集，构建action和goto表
    input_st = [['#', 'INPUT_END', w_dict[-1][2]]] + w_dict[::-1] #设置输入机内序列
    state_st, sym_st, id_st, son_st = [0], ['#'], [], [] #设置工作栈
    last_oper = -1
    t_cnt = 1 #轮次记录变量
    try:
        while len(input_st) > 0:
            ns = (state_st[-1], input_st[-1][0]) #记录当前状态的元组
            t = action_goto.get(ns) #从action和goto表中查找该元组
            if args.debug: print('#######\n当前轮次:{}\n当前符号栈:{},当前状态栈:{}\n当前读入字符:{},转移方程为:{}, t={}'.format(t_cnt,sym_st,state_st,input_st[-1][0], ns, t))
            if t is None: #如果未找到，说明该串存在语法错误
                raise Exception('\033[1;31;31m[Error]#201 in line {}, position {}: Unexpected word \'{}\' after \'{}\'.\n{}'.format(*input_st[-1][2], input_st[-1][1], sym_st.pop(), getErrorCodeLine(input_st[-1][2][0], input_st[-1][2][1]-1,input_st[-1][1])))
            if t[0] == 's' or t[0] == 'g': #移进或者goto,两者代码相同
                it = input_st.pop()
                sym_st.append(it[0]) #将符号提取出符号栈中
                state_st.append(t[1]) #将当前的状态提取出放入状态栈
                id_st.append(addGrammarTreeNode(sym_st[-1], son_st, it[1], (it[2][0], it[2][1]-1) )) #存放语法树节点
                son_st = []
                if last_oper != -1:#如果该节点是规约而来
                    if not analysis(id_st[-1], last_oper): return False
                    last_oper = -1
            elif t[0] == 'r': #规约
                last_oper = t[1]
                for i in range(len(productions[t[1]]['right'])): #如果不是从空串规约而来，设置子节点
                    sym_st.pop() #将被规约的子节点弹出
                    state_st.pop()
                    son_st.append(id_st.pop()) #并将其放入孩子栈中
                son_st.reverse()
                if len(productions[t[1]]['right']) == 0: #如果是空串,额外添加ε
                    son_st.append(addGrammarTreeNode('@', [], 'ε', (0,0)))
                input_st.append([productions[t[1]]['left'], '', (grammar_tree[son_st[0]]['debug_pos'][0],0)]) #将规约完的节点添加到input串中
            else:#规约成功 acc
                print("\033[1;32;32m[Info]Garmmar analysis success!\033[0m")
                break
            t_cnt += 1
    except Exception as err:#异常处理
        print(str(err))
        return False
    return True