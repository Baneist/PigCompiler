int cnt;
/*
该函数为二分查找函数
输入l为左端点
输入r为右端点
*/
int binary_search(int l, int r){
    int mid;
    while(l < r){
        mid = (l + r) / 2;
        if(mid > cnt){
            r = mid;//取左半段
        } else {
            l = mid + 1;//取右半段
        }
    }
    return l;
}

int main(){
    cnt = 25;
    int res;
    res = binary_search(5, 100);
    return res;
}