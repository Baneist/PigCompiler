int ans;
int a[10][10];

int max(int a, int b){
    int ans;
    ans = a;
    if(a < b){
        ans = b;
    }
    return ans;
}
//#include <stdio.h>
//int main(){
void main(void){
    a[0][0] = 1;
    int i;
    int j;
    i = 0;
    j = 0;
    while(i < 10){
        j = 0;
        while(j < 10){
            a[i][j] = i + j;
            if(i + j < 10){
                ans = ans + max(a[i][j], 10);
            } else {
                ans = ans + 15;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    
    return;
    //printf("%d\n", ans);
    //return 0;
}
