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

# 字符串哈希
```cpp

namespace string_hash{
unsigned BKDR(const std::string& str){
    unsigned seed = 131; // 31 131 1313 13131 131313 etc..
    unsigned hash = 0;
    for(auto c: str){
        hash = hash * seed + c;
    }
    return (hash & 0x7FFFFFFF);
}
unsigned AP(const std::string& str){
    unsigned hash = 0;
    for(int i = 0; i < str.length(); ++i){
        if(i & 1){
            hash ^= (~((hash << 11) ^ str[i] ^ (hash >> 5)));
        }else{
            hash ^= ((hash << 7) ^ str[i] ^ (hash >> 3));
        }
    }
    return (hash & 0x7FFFFFFF);
}
unsigned DJB(const std::string& str){
    unsigned hash = 5381;
    for(auto c: str){
        hash += (hash << 5) + c;
    }
    return (hash & 0x7FFFFFFF);
}
unsigned JS(const std::string& str){
    unsigned hash = 1315423911;
    for(auto c: str) hash ^= ((hash << 5) + c + (hash >> 2));
    return (hash & 0x7FFFFFFF);
}
unsigned SDBM(const std::string& str){
    unsigned hash = 0;
    for(auto c: str) hash = c + (hash << 6) + (hash << 16) - hash;
    return (hash & 0x7FFFFFFF);
}
unsigned PJW(const std::string& str){
    auto bits_in_unsigned_int = (unsigned)(sizeof(unsigned) * 8);
    auto three_quarters = (unsigned)(bits_in_unsigned_int * 3 / 4);
    auto one_eighth = (unsigned)(bits_in_unsigned_int / 8);
    unsigned high_bits = (unsigned)(0xFFFFFFFF) << (bits_in_unsigned_int - one_eighth);
    unsigned hash = 0;
    unsigned test = 0;
    for(auto c: str){
        hash = (hash << one_eighth) + c;
        if((test = hash & high_bits) != 0){
            hash = (hash ^ (test >> three_quarters)) & (~high_bits);
        }
    }
    return (hash & 0x7FFFFFFF);
}
unsigned ELF(const std::string& str){
    unsigned hash = 0, x = 0;
    for(auto c: str){
        hash = (hash << 4) + c;
        if((x = hash & 0xF0000000ll) != 0){
            hash ^= (x >> 24);
            hash &= (~x);
        }
    }
    return (hash & 0x7FFFFFFF);
}
}
```

# AC 自动机
```cpp

namespace ac_automaton{
template<int CHILD_CNT=26>
struct Node{
    int cnt;
    vector<shared_ptr<Node>> next;
    weak_ptr<Node> fail;
    explicit Node(shared_ptr<Node> root = nullptr): cnt(0), next(CHILD_CNT, root), fail(root){}
};
template<typename Iterator, int CHILD_CNT=26>
class AC{
    using T = typename remove_reference<decltype(*declval<Iterator>())>::type;
    using ACNode = Node<CHILD_CNT>;
public:
    explicit AC(): root(shared_ptr<ACNode>(new ACNode())){
        root->fail = root;
        for(auto& nex: root->next){
            nex = root;
        }
    }
    void insert(Iterator sBegin, Iterator sEnd, function<int(T)> func){
        auto ptr = root;
        for(Iterator sPtr = sBegin; sPtr != sEnd; ++sPtr){
            int to = func(*sPtr);
            if(ptr->next[to] == root){
                ptr->next[to] = shared_ptr<ACNode>(new ACNode(root));
            }
            ptr = ptr->next[to];
        }
        ptr->cnt++;
    }
    void build(){
        queue<shared_ptr<ACNode>> Q;
        for(int i = 0; i < CHILD_CNT; ++i){
            if(root->next[i] != root){
                Q.push(root->next[i]);
            }
        }
        while(!Q.empty()){
            auto ptr = Q.front();
            Q.pop();
            for(int i = 0; i < CHILD_CNT; ++i){
                if(ptr->next[i] != root){
                    ptr->next[i]->fail = ptr->fail.lock()->next[i];
                    Q.push(ptr->next[i]);
                }else{
                    ptr->next[i] = ptr->fail.lock()->next[i];
                }
            }
        }
    }
    int query(Iterator qBegin, Iterator qEnd, function<int(T)> func){
       int ans = 0;
       auto ptr = root;
       for(auto qPtr = qBegin; qPtr != qEnd; ++qPtr){
           ptr = ptr->next[func(*qPtr)];
           for(auto tPtr = ptr; tPtr != root and tPtr->cnt != -1; tPtr = tPtr->fail.lock()){
               ans += tPtr->cnt;
               tPtr->cnt = -1;
           }
       }
       return ans;
    }
private:
    shared_ptr<ACNode> root;
};
}
```