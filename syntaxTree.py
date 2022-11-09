from graphviz import Digraph
from base import grammar_tree

cnt = 0

dot = Digraph(comment='The Synatx Tree')

def drawSyntaxTree():
    global cnt
    for i in grammar_tree:
        nodeName = 'node'+str(cnt)
        dot.node(nodeName, i['sym'], fontname="Microsoft YaHei")
        for j in i['son']:
            sonName = 'node'+str(j)
            dot.edge(nodeName, sonName)
        cnt=cnt+1
    print(dot.source)
    dot.render('round-table.gv', view=True, format='png')