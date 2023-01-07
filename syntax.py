from graphviz import Digraph
from base import grammar_tree
import os

def drawSyntaxTree():
    dot = Digraph(comment='Grammar Tree') #生成语法图
    cnt = 0 #初始化节点统计变量
    for i in grammar_tree: #对所有语法树中的节点
        nodeName = 'node'+str(cnt) #设置节点名字
        #dot.node(nodeName, i['cont'] if len(i['cont']) else i['sym'], fontname="Microsoft YaHei") #添加节点
        show = ( i['cont'] if (i['sym'][0] == '$') else i['sym'] ) + '\n'
        for t in i.keys(): #绘制抽象语法树
            if t != 'sym' and t != 'son' and t != 'debug_pos' and ( t != 'cont' or t == 'cont' and len(i[t])):
                show += t + ' = ' + str(i[t]) + '\n'
        dot.node(nodeName, show, fontname="Microsoft YaHei") #添加节点
        for j in i['son']: #设置孩子节点名
            sonName = 'node'+str(j)
            dot.edge(nodeName, sonName) #画自己到孩子节点的边
        cnt=cnt+1
    dot.render('grammar_tree', view=True, format='png') #生成图片
    os.remove('grammar_tree') #删除中间文件