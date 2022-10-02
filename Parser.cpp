#include <iostream>
#include <regex>
#include "Parser.h"
using namespace std;

//保留字字典
const std::string reserve_word_list[] = {",", "!=", "==", "<",  "<=", "=",  ">", ">=", "=", 
                          "*",  "+", "-", "/",  ";", "(",  ")", "{",  "}",
                          "else", "if", "int", "float", "return", "void", "while"};

void Parser::throwError(int e_ptr, int err_code, string err_description){
    printf("#in Line %d-%d: %s", now_line, e_ptr, work_str.c_str());
    printf("#Error %d: %s", 100+err_code, err_description.c_str());  
    exit(0);
}

Parser::Parser(std::string str) : w_ptr(0), now_line(0) {
    input_str = str + "\r\n";
    preProcessComment();
    initReserveWord();
    while(getWorkString())
        if(!dealWorkString())
            exit(0);
}

void Parser::initReserveWord(){
    
    int begin_word_code = 60;
    for(auto str : reserve_word_list)
        reserve_word_map[str] = begin_word_code++;
}

/*
作用：判断str是否为保留字
输入：str
输出：如果不是返回100，否则返回保留字代码
*/
int Parser::isReserveWord(const string &str){
    auto iter = reserve_word_map.find(str);
    if(iter == reserve_word_map.end())
        return TYPE_NORMAL_WORD;
    return iter->second;
}

std::string Parser::getReserveWord(int id){
    if(id == TYPE_NORMAL_WORD)
        return "";
    return reserve_word_list[id];
}

void Parser::preProcessComment(){
    input_str = regex_replace(input_str, regex("(//[^\n]*\n)"), "\n");
    input_str = regex_replace(input_str, regex("(/\\*(.|\r|\n)*\\*/)"), " "); //匹配注释
}

bool Parser::getWorkString(){ //从字符串中读取一整行的输入，并且去掉前缀空格
    now_line++;
    while(input_str[w_ptr] == ' ')
        w_ptr++;
    int e_ptr = w_ptr;
    while(input_str[e_ptr] != '\n')
        e_ptr++;
    work_str = input_str.substr(w_ptr, e_ptr - w_ptr + 1);
    if((w_ptr = e_ptr + 1) == input_str.size())
        return false;
    return true;
}

/*
词语分割系列函数
输入：当前位置
输出：将分割后的词放入word字符串中
*/
bool Parser::dealDigit(int e_ptr){
    int ptr = 1;
    while(isdigit(work_str[e_ptr + ptr]))
        ptr++;
    word = work_str.substr(e_ptr, ptr);
    word_type = TYPE_NUM_INT;
    return true;
}

bool Parser::dealWord(int e_ptr){
    int ptr = 1;
    while(isdigit(work_str[e_ptr + ptr]) || isalpha(work_str[e_ptr + ptr]) || work_str[ptr] == '_')
        ptr++;
    word = work_str.substr(e_ptr, ptr);
    word_type = isReserveWord(word);
    return true;
}

bool Parser::dealSymbol(int e_ptr){
    int ptr = 0;
    while(!isdigit(work_str[e_ptr + ptr]) && !isalpha(work_str[e_ptr + ptr]) //匹配最长的保留字
        && !(work_str[e_ptr + ptr] == '_' || work_str[e_ptr + ptr] == '\r' || work_str[e_ptr + ptr] == '\n' || work_str[e_ptr + ptr] == ' ')){
            ptr++;
            if(isReserveWord(work_str.substr(e_ptr, ptr)) != TYPE_NORMAL_WORD && isReserveWord(work_str.substr(e_ptr, ptr + 1)) == TYPE_NORMAL_WORD)
                break;
        }
    word = work_str.substr(e_ptr, ptr);
    if((word_type = isReserveWord(word)) == TYPE_NORMAL_WORD){
        throwError(e_ptr, ERROR_SYMBOL_NOT_REVERSE_WORD, word + " is not a reverse symbol.");
        return false;
    }
    return true;
}

bool Parser::dealWorkString(){
    int ptr = 0;
    while(ptr < work_str.size()){
        while(work_str[ptr] == '\r' || work_str[ptr] == '\n' || work_str[ptr] == ' ') //读取无意义的前缀
            if(ptr == work_str.size() - 1)
                return true;
            else
                ptr++; 
        if(isdigit(work_str[ptr])) //当前词为常数
            dealDigit(ptr);
        else if(isalpha(work_str[ptr]) || work_str[ptr] == '_') //当前词为标识符或者保留字
            dealWord(ptr);
        else //处理非词语类保留字
            dealSymbol(ptr);
        ptr += word.size();

        //输出方法 具体怎么写进文件里还没想好
        cout << word_type << " " << word << endl;
    }
    return true;
}