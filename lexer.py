import re
from base import JudgeReverseWord, isSymbol, w_dict, s_code, getErrorCodeLine, args

l_cnt, w_ptr, w_str, word, w_type = 0,0,'','',0

def preProcessComment(str): #预处理注释
    str = re.sub('//[^\n]*\n', '\n', str) #处理单行注释
    str = re.sub('/\\*(.|\r|\n)*?\\*/[\x20]*', '\n', str) #处理多行注释
    return str #返回去除注释后的字符串

def getWorkString(str): #整行读取输入并返回分割后的字符串
    global w_ptr, l_cnt, w_str
    if w_ptr == len(str):#w_ptr: 指向当前工作位置的指针
        return False
    l_cnt += 1 #行计数器
    ret = re.search('.*\n', str[w_ptr:]) #找第一个出现的回车字符串，从此处切分
    w_ptr, w_str = ret.end() + w_ptr, ret.group() #设置新的工作串和工作指针
    return True

def dealWorkString(): #词法分析
    global l_cnt, w_ptr, w_str, word, w_type
    ptr = 0 #句子的工作指针
    lw = len(w_str) #工作串的长度
    while ptr < lw: #当仍然有剩余的工作串
        ptr = ptr + re.search('[\x20\r\n]*', w_str[ptr:]).end() #过滤无用空格和回车
        if ptr == lw:
            return True
        if w_str[ptr].isdigit(): #处理数字
            ret = re.search('\\d+(\\.\\d+)?(e(\\+|-)?\\d+)?', w_str[ptr:])
            word = ret.group()
            if w_str[ptr+ret.end()].isalpha() or w_str[ptr+ret.end()]=='_':#数字匹配失败 抛出异常
                raise Exception('\033[1;31;31m[Error]#101 in line {}, position {}: illegal num {}.\n{}'.format(l_cnt, ptr, word + w_str[ptr+ret.end()], getErrorCodeLine(l_cnt,ptr,word + w_str[ptr+ret.end()])))
            if '.' not in word and 'e' not in word: #根据其值区分整形数和浮点数
                w_type = '$digit_int'
                word = int(word)
            else:
                w_type = '$digit_int'#由于还没有实现浮点数，先当作整形数
                word = int(word)
        elif w_str[ptr].isalpha() or w_str[ptr] == '_': #处理单词
            ret = re.search('\\w*', w_str[ptr:])
            word = ret.group()
            w_type = '$identifier' if JudgeReverseWord(word) == -1 else JudgeReverseWord(word) #判断其是否为保留字
        else: #处理符号
            eptr = ptr + 1 #从下一个符号开始判断
            has_re = False 
            while (not has_re and isSymbol(w_str[eptr - 1])) or JudgeReverseWord(w_str[ptr:eptr]) != -1: #匹配最长的是保留字的词
                if JudgeReverseWord(w_str[ptr:eptr]) != -1:
                    has_re = True
                eptr += 1 
            word = w_str[ptr:eptr - 1]
            if not has_re: #初始匹配失败 当前符号本身就不是关键字 抛出异常
                raise Exception('\033[1;31;31m[Error]#102 in line {}, position {}: illegal word {}.\n,{}'.format(l_cnt, ptr, word, getErrorCodeLine(l_cnt,ptr,word)))
            w_type = JudgeReverseWord(word)
        ptr += len(str(word))
        w_dict.append([w_type, word, (l_cnt, ptr)]) #将完成分割的词语放入输出序列中
        
def Lexer(i_str): #词法分析器入口函数，输出结果会放到base的w_dict中
    global s_code
    i_str = preProcessComment(i_str + '\r\n')#预处理，去除注释
    s_code += i_str.split('\n')
    #print('去除注解的源程序列表:', i_str)
    while getWorkString(i_str): #不断获取工作串
        try:
            dealWorkString() #进行分词解析
        except Exception as err: #捕获异常并进行异常输出
            print(str(err))
            return False
    if args.debug: print('单词机内表示序列:', w_dict) #词法分析器输出
    print("\033[1;32;32m[Info]Lexical analysis success!\033[0m")
    return True