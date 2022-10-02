#ifndef PARSER_H
#define PARSER_H

#include <string>
#include <map>

class Parser {
public:
    enum {
        ERROR_SYMBOL_NOT_REVERSE_WORD
    };
    static const int TYPE_NORMAL_WORD = 100, TYPE_NUM_INT = 101;

private:
    std::map<std::string, int> reserve_word_map;
    std::string work_str, input_str, word;
    int w_ptr, word_type, now_line;

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