# PigComplier
同济大学编译原理( CS100395 ) 实验设计. 一个类C编译器（仅实现到中间代码生成）.

代码结构：

base.py：共享变量定义，初始化工作

main.py：主程序入口

- lexer.py：语法分析

- gparser.py：词法分析
- syntax.py：语法树绘制（需安装dot库）
- analyser.py：语义分析与中间代码生成
