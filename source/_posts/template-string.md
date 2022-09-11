---
title: 字符串模板
math: true
date: 2022-09-11 12:11:54
categories:
    - 模板
tags:
    - CPP
    - 模板
    - 字符串
index_img: https://cdn.dianhsu.com/img/2022-09-11-13-27-46.jpeg
---
字符串，就是由字符连接而成的序列。
# KMP

```cpp
template<typename RandomAccessIterator>
vector<int> preKmp(RandomAccessIterator pBegin, RandomAccessIterator pEnd, bool accelerate = false){
    vector<int> fall(distance(pBegin, pEnd) + 1, -1);
    int i = 0, j = -1;
    while(i + pBegin != pEnd){
        while(j != -1 and *(pBegin + i) != *(pBegin + j)) j = fall[j];
        ++i, ++j;
        if(accelerate){
             // 这里的优化，如果一直不匹配会得到 fall[fall[...fall[i]...]]
             if(i < distance(pBegin, pEnd) and j < distance(pBegin, pEnd) and *(pBegin + i) == *(pBegin + j)) fall[i] = fall[j];
             else fall[i] = j;
        }else{
            fall[i] = j;
        }
    }
    return fall;
}
template<typename RandomAccessIterator>
int kmp(RandomAccessIterator tBegin, RandomAccessIterator tEnd, RandomAccessIterator pBegin, RandomAccessIterator pEnd, vector<int>& fall){
    int i = 0, j = 0;
    int ans = 0;
    while(tBegin + i < tEnd){
        while(j != -1 and *(pBegin + j) != *(tBegin + i)) j = fall[j];
        ++i, ++j;
        if(j >= distance(pBegin, pEnd)){
            ++ans;
            cout << i - distance(pBegin, pEnd) + 1 << "\n";
            j = fall[j];
        }
    }
    return ans;
}
template<typename RandomAccessIterator>
int kmp(RandomAccessIterator tBegin, RandomAccessIterator tEnd, RandomAccessIterator pBegin, RandomAccessIterator pEnd, bool accelerate = false){
    auto&& fall = preKmp(pBegin, pEnd, accelerate);
    return kmp(tBegin, tEnd, pBegin, pEnd, fall);
}
```

# Z Function（拓展KMP）

```cpp
template<typename RandomAccessIterator>
vector<int> zFunction(RandomAccessIterator pBegin, RandomAccessIterator pEnd){
    int n = distance(pBegin, pEnd);
    vector<int> z(n);
    for(int i = 1, l = 0, r = 0; i < n; ++i){
        if(i <= r and z[i - l] < r - i + 1){
            z[i] = z[i - l];
        }else{
            z[i] = max(0, r - i + 1);
            while(i + z[i] < n and *(pBegin + z[i]) == *(pBegin + i + z[i])) ++z[i];
        }
        if(i + z[i] - 1 > r){
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}
```

# Manacher

```cpp
enum Separator {
    Start,
    Mid,
    End
};

template<typename RandomAccessIterator>
pair<RandomAccessIterator, RandomAccessIterator> manacher(RandomAccessIterator sBegin, RandomAccessIterator sEnd) {
    vector<any> ma;
    ma.reserve(distance(sBegin, sEnd) * 2 + 10);
    ma.emplace_back(Start);
    ma.emplace_back(Mid);
    for (auto ptr = sBegin; ptr != sEnd; ++ptr) {
        ma.push_back(ptr);
        ma.emplace_back(Mid);
    }
    ma.emplace_back(End);
    int len = (int)ma.size();
    vector<int> mp(len, 0);
    int mx = 0, id = 0;
    int maxPos = 0;
    for (int i = 1; i < len - 1; ++i) {
        mp[i] = mx > i ? std::min(mp[(id << 1) - i], mx - i) : 1;
        while (ma[i + mp[i]].type() == ma[i - mp[i]].type() and
               (ma[i + mp[i]].type() == typeid(RandomAccessIterator) ?
                (*any_cast<RandomAccessIterator>(ma[i + mp[i]]) ==
                 *any_cast<RandomAccessIterator>(ma[i - mp[i]])) :
                (any_cast<Separator>(ma[i + mp[i]])) ==
                any_cast<Separator>(ma[i - mp[i]]))) {
            ++mp[i];
        }
        if(mp[i] > mp[maxPos]) maxPos = i;
        if(i + mp[i] > mx){
            mx = i + mp[i];
            id = i;
        }
    }
    pair<RandomAccessIterator, RandomAccessIterator> ret;
    int l = maxPos - mp[maxPos] + 1, r = maxPos + mp[maxPos] - 1;
    if(l & 1) ++l;
    if(r & 1) --r;
    return {sBegin + (l - 1) / 2, sBegin + (r + 1) / 2};
}
```