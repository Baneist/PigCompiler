int test(int x, int y){
    x = x + y;
    return 1;
}

void main(void){
    int x;
    int y;
    x = 0;
    y = 1;
    x = test(y);
}