#ifndef PARSER_H
#define PARSER_H

#include <string>
#include <map>

class Parser {
public:
    enum { //Parser出错编号从101开始
        ERROR_SYMBOL_NOT_REVERSE_WORD = 101,
        ERROR_ILLEGAL_NUM
    };
    enum {
        TYPE_NORMAL_WORD = 100,
        TYPE_NUM_INT,
        TYPE_NUM_FLOAT
    };

private:
    std::map<std::string, int> reserve_word_map;
    std::string work_str, input_str, word;
    int w_ptr, word_type, now_line;
    bool success;

private:
    void throwError(int e_ptr, int err_code, std::string err_description);
    void initReserveWord();
    void preProcessComment();//预处理注释
    bool getWorkString();
    bool dealWorkString();
    bool dealDigit(int e_ptr);
    bool dealWord(int e_ptr);
    bool dealSymbol(int e_ptr);

public:
    Parser(std::string str);
    int isReserveWord(const std::string &str);
    std::string getReserveWord(int id);

public:
    void start();
};

#endif