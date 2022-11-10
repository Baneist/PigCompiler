from graphviz import Digraph
from base import grammar_tree
import os

def drawSyntaxTree():
    dot = Digraph(comment='Grammar Tree')
    cnt = 0
    for i in grammar_tree:
        nodeName = 'node'+str(cnt)
        dot.node(nodeName, i['cont'] if len(i['cont']) else i['sym'], fontname="Microsoft YaHei")
        for j in i['son']:
            sonName = 'node'+str(j)
            dot.edge(nodeName, sonName)
        cnt=cnt+1
    dot.render('grammar_tree', view=True, format='png')
    os.remove('grammar_tree')