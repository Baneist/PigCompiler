int binary_search(){
    int cnt;
    int ans;
    int l;
    int r;
    cnt = 0;
    ans = 1;
    while(l<r){
        l=l+1;
        cnt=cnt+1;
        ans=ans*cnt;
    }
    return ans;
}