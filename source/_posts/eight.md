---
title: 八数码的解法
date: 2022-05-17 20:53:34
tags:
    - 八数码
    - 广度优先搜索
    - 启发式搜索
    - 康托展开
categories: 算法
math: true
---



# 广度优先搜索
```cpp
#include <cctype>
#include <iostream>
#include <vector>
#include <array>
#include <set>
#include <queue>

using namespace std;
typedef array<int, 9> eight;
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};
int dr[] = {-3, 3, -1, 1};
int solve(eight st, eight ed){
    set<eight> vis;
    queue<pair<eight, int>> q;
    q.push({st, 0});
    vis.insert(st);
    auto&& check = [&](int pos, int idx) -> bool{
        int x = pos / 3, y = pos % 3;
        return x + dx[idx] >= 0 and x + dx[idx] < 3 and y + dy[idx] >= 0 and y + dy[idx] < 3;
    };
    while(!q.empty()){
        auto it = q.front();
        //for(auto& c: it.first) cout << c << " "; cout << ": " << it.second << "\n";
        q.pop();
        if(it.first == ed) {
            return it.second;
        }
        int pos = 0;
        for(int i = 0; i < 9; ++i){
            if(it.first[i] == 0){
                pos = i;
            }
        }
        for(int i = 0; i < 4; ++i){
            if(check(pos, i)){
                swap(it.first[pos], it.first[pos + dr[i]]);
                if(!vis.count(it.first)){
                    q.push({it.first, it.second + 1});
                    vis.insert(it.first);
                }
                swap(it.first[pos], it.first[pos + dr[i]]);
            }
        }
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    eight ed{1, 2, 3, 8, 0, 4, 7, 6, 5};
    eight st;
    string tmp;
    cin >> tmp;
    for (int i = 0; i < 9; ++i) {
        st[i] = tmp[i] - '0';
    }
    cout << solve(st, ed) << endl;
    return 0;
}
```

# 康托展开 + 广度优先搜索
```cpp
#include <cctype>
#include <iostream>
#include <vector>
#include <array>
#include <set>
#include <queue>
#include <map>

using namespace std;
typedef array<int, 9> eight;
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};
int dr[] = {-3, 3, -1, 1};
int radix[] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320};

int cantor(eight &t) {
    int res = 0;
    for (int i = 0; i < 9; ++i) {
        int cnt = 0;
        for (int j = i + 1; j < 9; ++j) {
            if (t[i] > t[j]) {
                ++cnt;
            }
        }
        res += radix[8 - i] * cnt;
    }
    return res;
}

eight reverse_cantor(int val) {
    eight ret;
    vector<int> vis(9, 0);
    for (int i = 0; i < 9; ++i) {
        int idx = val / radix[8 - i];
        val %= radix[8 - i];
        for (int j = 0; j < 9; ++j) {
            if (vis[j] == 0) {
                if (idx == 0) {
                    vis[j] = 1;
                    ret[i] = j;
                    break;
                }
                --idx;
            }
        }

    }
    return ret;
}

int solve(eight st, eight ed) {
    vector<int> disv(362880, -1);
    queue<int> q;
    int stv = cantor(st);
    int edv = cantor(ed);
    q.push(stv);
    disv[stv] = 0;
    auto &&check = [&](int pos, int idx) -> bool {
        int x = pos / 3, y = pos % 3;
        return x + dx[idx] >= 0 and x + dx[idx] < 3 and y + dy[idx] >= 0 and y + dy[idx] < 3;
    };
    while (!q.empty()) {
        auto it = q.front();
        q.pop();
        if (it == edv) {
            return disv[edv];
        }
        auto &&ita = reverse_cantor(it);
        int pos = 0;
        for (int i = 0; i < 9; ++i) {
            if (ita[i] == 0) {
                pos = i;
            }
        }
        for (int i = 0; i < 4; ++i) {
            if (check(pos, i)) {
                swap(ita[pos], ita[pos + dr[i]]);
                int itav = cantor(ita);
                if (disv[itav] == -1) {
                    disv[itav] = disv[it] + 1;
                    q.push(itav);
                }
                swap(ita[pos], ita[pos + dr[i]]);
            }
        }
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    eight ed{1, 2, 3, 8, 0, 4, 7, 6, 5};
    eight st;
    string tmp;
    cin >> tmp;
    for (int i = 0; i < 9; ++i) {
        st[i] = tmp[i] - '0';
    }
    cout << solve(st, ed) << endl;
    return 0;
}

```