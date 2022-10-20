#include "Parser.h"
#include <fstream>

int main(int argv, const char *argc[]){
    std::ifstream t("test.c");
    std::string str((std::istreambuf_iterator<char>(t)), std::istreambuf_iterator<char>());
    Parser parser(str);
    return 0;
}