import re
from base import JudgeReverseWord, isSymbol, w_dict

l_cnt, w_ptr, w_str, word, w_type = 0,0,'','',0

def preProcessComment(str): #预处理注释
    str = re.sub('//[^\n]*\n', '\n', str) #处理单行注释
    str = re.sub('/\\*(.|\r|\n)*?\\*/[\x20]*', '\n', str) #处理多行注释
    return str #返回去除注释后的字符串

def getWorkString(str): #整行读取输入并返回分割后的字符串
    global w_ptr, l_cnt, w_str
    l_cnt += 1
    ret = re.search('.*\n', str[w_ptr:])
    w_ptr, w_str = ret.end() + w_ptr, ret.group()
    return False if w_ptr == len(str) else True

def dealWorkString(): #词法分析
    global l_cnt, w_ptr, w_str, word, w_type
    ptr = 0
    lw = len(w_str)
    while ptr < lw:
        ptr = ptr + re.search('[\x20\r\n]*', w_str[ptr:]).end() #过滤无用空格和回车
        if ptr == lw:
            return True
        if w_str[ptr].isdigit(): #处理数字
            ret = re.search('\\d+(\\.\\d+)?(e(\\+|-)?\\d+)?', w_str[ptr:])
            word = ret.group()
            if w_str[ptr+ret.end()].isalpha() or w_str[ptr+ret.end()]=='_':#数字匹配失败 抛出异常
                raise Exception('[Error]#101 in line {}, position {}: illegal num {}.'.format(l_cnt, ptr, word + w_str[ptr+ret.end()]))
            if '.' not in word and 'e' not in word:
                w_type = '$digit_int'
            else:
                w_type = '$digit_int'
        elif w_str[ptr].isalpha() or w_str[ptr] == '_': #处理单词
            ret = re.search('\\w*', w_str[ptr:])
            word = ret.group()
            w_type = '$identifier' if JudgeReverseWord(word) == -1 else JudgeReverseWord(word)
        else: #处理符号
            eptr = ptr + 1
            has_re = False 
            while (not has_re and isSymbol(w_str[eptr - 1])) or JudgeReverseWord(w_str[ptr:eptr]) != -1: #匹配最长的是保留字的词
                if JudgeReverseWord(w_str[ptr:eptr]) != -1:
                    has_re = True
                eptr += 1
            word = w_str[ptr:eptr-1]
            if not has_re: #初始匹配失败 当前符号本身就不是关键字 抛出异常
                raise Exception('[Error]#102 in line {}, position {}: illegal word {}.'.format(l_cnt, ptr, word))
            w_type = JudgeReverseWord(word)
        ptr += len(word)
        w_dict.append([w_type, word, (l_cnt, ptr)])
        
def Lexer(i_str): #词法分析器入口函数，输出结果会放到base的w_dict中
    i_str = preProcessComment(i_str + '\r\n')
    while getWorkString(i_str): #不断获取工作串
        try:
            dealWorkString() #进行分词解析
        except Exception as err:
            print(str(err))
            return False
    print("[Info]Lexical analysis success!")
    return True