//#include "stdio.h"
int a[2][3];
int b[3][4];

int program(int a,int b,int c){
    int i;
    int j;
    i=0; 
    if(a>(b+c)){
        j=a+(b*c+1);
    } else {
        j=a;
    }
    while(i<=100){
        i=j*2;
        j=i;
    }
    return i;
}

int demo(int a)
{
    a=a+2;
    return a*2;
}

void main(void)
{
    a[0][0]=3;
    a[0][1]=a[0][0]+1;
    a[1][0]=a[0][1]+1;
    a[1][1]=program(a[0][0],a[0][1],demo(a[1][0]));//3,4,10
    return 0;
}
