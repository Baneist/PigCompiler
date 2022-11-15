int binary_search() {
    cnt = 0;
    ans = 1;
    while(l<r) {
        int c;
        int t;
        if(c>12){
            l=print(r);
        }
        l=l+1;
        cnt=cnt+1;
        ans=ans*cnt;
    }
    return ans;
}