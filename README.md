# PigComplier
同济大学编译原理( CS100395 ) 实验设计. 一个类C编译器

添加了详尽的注释，供23届以后采用Python作为开发语言，试图简化代码实现、加快开发的同学参考。

代码结构：

base.py：共享变量定义，初始化工作

- base.json：存放产生式和语义动作

main.py：主程序入口

- lexer.py：语法分析
- gparser.py：词法分析
- syntax.py：语法树绘制（需安装dot库）
- analyser.py：语义分析与中间代码生成
- generator.py：目标代码生成

采用命令行交互的方式，具体用法请使用 pcc -h 查看
