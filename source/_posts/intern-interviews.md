---
title: 2022春天的实习面试经历
date: 2022-05-11 01:12:11
tags:
---

> 目前已经接到微软的实习offer，所以将之前的面试内容都贴在这里了

## 2022.02.28 微软实习正式批一面
- 面试时长：约45分钟
- 面试经过：
    1. 面试官自我介绍
    2. 我的自我介绍
    3. 根据简历上面问了一下项目和本科毕业之后的经历
    4. 写了一道算法题：数组中的逆序对数目（归并排序，平衡树，树状数组或线段树）
    参考：[数组中的逆序对](https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/)
        ```cpp
        #include <bits/stdc++.h>

        using namespace std;

        int handle(vector<int>& vec){
            int ret = 0;
            int sz = vec.size();
            if(sz <= 1) return 0;
            int mid = sz / 2;
            vector<int> vec1, vec2;
            vec1.insert(vec1.end(), vec.begin(), vec.begin() + mid);
            vec2.insert(vec2.end(), vec.begin() + mid, vec.end());
            ret += handle(vec1);
            ret += handle(vec2);
            vec.clear();
            int pos1 = 0, pos2 = 0;
            while(pos1 < vec1.size() or pos2 < vec2.size()){
                if(pos1 < vec1.size() and pos2 < vec2.size()){
                    if(vec1[pos1] > vec2[pos2]){
                        ret += vec1.size() - pos1;
                        vec.push_back(vec2[pos2++]);
                    }else{
                        vec.push_back(vec1[pos1++]);
                    }
                }else if(pos1 < vec1.size()){
                    vec.push_back(vec1[pos1++]);
                }else if(pos2 < vec2.size()){
                    ret += vec1.size() - pos1;
                    vec.push_back(vec2[pos2++]);
                }
            }
            return ret;
        }
            
        int main(){
            vector<int> arr{7,6,8,3,5};
            int ans = handle(arr);
            cout << ans << endl;
            vector<int> brr{9,8,7,6,5,4,3,2,1};
            vector<int> crr{1,2,3,4,5,6,7,8,9};
            vector<int> drr{1, 1};
            cout << handle(brr) << endl;
            cout << handle(crr) << endl;
            cout << handle(drr) << endl;
            return 0;
        }
        ```
   5. 场景题：考虑在一个短链接生成系统中，如何设计短链接生成。
   6. 反问：简历有没有什么问题
## 2022.03.01 字节跳动飞书实习一面
- 面试时长：约28分钟
- 面试经过：
  1. 自我介绍
  2. 问了一下之前在百度实习的项目的内容
  3. C++的面向对象的特点
  4. 多态的实现形式
  5. 讲一讲Python语言和C++语言的区别
  6. 三次握手的过程
  7. 保证TCP传输的可靠性的实现
  8. 浏览器输入网址之后的过程
  9. C++虚函数，纯虚函数，虚析构函数
  10. C++的vector的底层实现
  11. 智能指针（用过，但是不太熟。直接说没怎么用）
  12. 线程和进程
  13. 虚拟内存
  14. 进程调度的状态
  15. 写个代码：给定一个query字符串，和pattern字符串，问能不能在pattern字符串中插入若干个小写字母，使得query串和pattern串一致。
   
    | query         | pattern | 结果    |
    | ------------- | ------- | ------- |
    | `FoolBar`     | `FB`    | `true`  |
    | `FoolBarTest` | `FB`    | `false` |
    | `FoolBar`     | `FBa`   | `true`  |
    | `FoolBar`     | `FaB`   | `false` |

    ```cpp
    #include <bits/stdc++.h>

    using namespace std;

    bool match(string query, string pattern){
        int n = query.size(), m = pattern.size();
        int i = 0, j = 0;
        while(i < n or j < m){
            if(i < n and j < m){
                if(query[i] == pattern[j]){
                    i++;
                    j++;
                }else if(islower(query[i])){
                    ++i;
                }else{
                    return false;
                }
            }else if(j < m){
                return false;
            }else if(i < n){
                if(isupper(query[i]))
                    return false;
                ++i;
            }
        }
        return true;
    }
    int main(){
        cout << match("FoolBar", "FB") << endl;
        cout << match("FoolBarTest", "FB") << endl;
        cout << match("FoolBar", "FBa") << endl;
        cout << match("FoolBar", "FaB") << endl;
        return 0;
    }
    ```

  16. 反问：没什么问题
## 2022.03.04 微软实习正式批三面
> 备注：一面和二面是平行的，一面通过之后就没有二面了。
- 面试时长：约36分钟
- 面试经过：
  1. 我的自我介绍
  2. 问了下在百度实习的情况
  3. 写一道算法题
   类似的题目：[单字符重复子串的最大长度](https://leetcode-cn.com/problems/swap-for-longest-repeated-character-substring/)
        ```cpp
        /*

        Given an array with around 100K elements, each element is within [0,100K ], how to get maxsubsequencelength with same value if you have a opportunity to swap two elements?

        2 2 3 1 4 5 1 1 0 1 7 => 4

        */
        #include <bits/stdc++.h>
        using namespace std;
        typedef pair<int, int> PII;
        int solve(vector<int> arr){
            if(arr.size() == 0) return 0;
            map<int, vector<PII>> mp;
            int n = arr.size();
            int cur = 0;
            for(int i = 0; i < n; ++i){
                if(arr[i] != arr[cur]){
                    // cur, i - 1
                    if(mp.count(arr[cur])) mp[arr[cur]].push_back({cur, i - 1});
                    else mp[arr[cur]] = {PII{cur, i - 1}};
                    cur = i;
                }
            }
            if(cur < n){
                mp[arr[cur]].push_back({cur, n - 1});
            }
            int ans = 1;
            for(auto& [_, vec]: mp){
                if(vec.size() == 1){
                    auto& it = vec.front();
                    ans = max(ans, it.second - it.first + 1);
                }else if(vec.size() == 2){
                    auto& it1 = vec[0];
                    auto& it2 = vec[1];
                    if(it1.second + 2 == it2.first){
                        ans = max(ans, it2.second - it2.first + 1 + it1.second - it1.first + 1);
                    }else{
                        ans = max(ans, it1.second - it1.first + 2);
                        ans = max(ans, it2.second - it2.first + 2);
                    }
                }else{
                    int m = vec.size();
                    ans = max(ans, vec[0].second - vec[0].first + 2);
                    for(int i = 1; i < m; ++i){
                        ans = max(ans, vec[i].second - vec[i].first + 2);
                        if(vec[i - 1].second + 2 == vec[i].first){
                            ans = max(ans, vec[i].second - vec[i].first + 1 + vec[i - 1].second - vec[i - 1].first + 1 + 1);
                        }
                    }
                }
            }
            return ans;
        }

        int main(){
            cout << solve({2, 2, 3, 1, 4, 5, 1, 1, 0, 1, 7}) << endl;
            cout << solve({2, 2, 2, 1, 2, 2, 2}) << endl;
            cout << solve({2, 2, 1, 2, 2, 2}) << endl;
            cout << solve({2, 1, 2, 2, 1, 2, 2, 2}) << endl;
            cout << solve({2}) << endl;
            cout << solve({}) << endl;
            return 0;
        }
        ```
  4. 有三枚硬币，指定一种得到1/7概率的情况。
  5. 反问：部门情况
## 2022.03.08 字节跳动飞书实习二面
- 面试时长：约60分钟
- 面试经过：
  1. 自我介绍
  2. 介绍下在百度实习的项目
  3. 介绍下去年做的项目
  4. 讲讲几种设计模式
  5. 写个单例
        ```cpp
        class Config{
        private:
            Config(): ptr(nullptr){}
            void update(string s){
                delete ptr;
                ptr = new string(s);
            }
            string query(){
                if(ptr == nullptr) ptr = new string("123");
                return *ptr;
            }
        };

        static int val = 0;
        int query(){
            return val;
        }
        void update(int x){
            val = x;
        }
        ```

  6. 说一下数据库的隔离模式
  7. 开放性问题：讲一下如何考虑操作系统拷贝一个文件
  8. 开放性问题：word文档如何单词纠错
  9. 算法题：[一维接雨水](https://leetcode-cn.com/problems/trapping-rain-water/)
        ```cpp
        class Solution {
        public:
            int trap(vector<int>& height) {
                vector<int> st1, st2;
                vector<int> pref(height.size());
                int n = height.size();
                pref[0] = height[0];
                for(int i = 1; i < n; ++i){
                    pref[i] = pref[i - 1] + height[i];
                }
                for(int i = 0; i < n; ++i){
                    while(!st2.empty() and height[i] >= height[st2.back()]) st2.pop_back();
                    st2.push_back(i);
                }
                for(int i = n - 1; i >= 0; --i){
                    while(!st1.empty() and height[i] >= height[st1.back()]) st1.pop_back();
                    st1.push_back(i);
                }
                reverse(st1.begin(), st1.end());
                reverse(st2.begin(), st2.end());
                int ans = 0;
                for(int i = 1; i < st1.size(); ++i){
                    int curp = st1[i], prep = st1[i - 1];
                    int ts = height[prep] * (curp - prep - 1) - (pref[curp - 1] - pref[prep]);
                    ans += ts;
                }
                for(int i = 1; i < st2.size(); ++i){
                    int curp = st2[i], prep = st2[i - 1];
                    int ts = height[prep] * (prep - curp - 1) - (pref[prep - 1] - pref[curp]);
                    ans += ts;
                }
                int tl = st1.back(), tr = st2.back();
                ans += (tr - tl) * height[tl] - (pref[tr] - pref[tl]);
                return ans;
            }
        };
        ```
  10. 反问：部门情况和面试流程
## 2022.03.10 蚂蚁集团大安全技术部实习一面
> 备注：电话面试，感觉闲聊为主
- 面试时长：约25分钟
- 面试过程：
  1. 面试官自我介绍
  2. 我的自我介绍
  3. 询问百度实习经过
  4. 一顿闲聊
  5. 重载函数的规则和底层实现
  6. const关键字
  7. malloc、free和new、delete
  8. delete和delete []
  9. 函数的调用约定（参数的入栈顺序）
  10. vector扩容
  11. 什么情况下vector的迭代器会失效（扩容和删除元素）
  12. 动态库和静态库（没写过）
  13. 跨平台开发
  14. 本科和研究生之间的gap
  15. 有空去做下笔试（补充，3月14日完成笔试）
  16. 反问：没啥问题
  17. 面试官再介绍了一下蚂蚁和阿里
## 2022.03.14 字节跳动飞书实习三面
- 面试时长：22分钟
- 面试经过：
    hr面，主要了解下个人情况和职业规划等。
    本来是视频面，因为通讯不好，改成电话面试。
## 2022.03.16 美团实习一面
> 备注：主动终止流程

## 2022.03.29 Hulu实习一面
- 面试时长：60分钟
- 面试经过：
    1. C++虚函数是怎么实现的
    2. struct和class区别
    3. C和C++区别
    4. 除了面向过程和面向对象，你还知道其他编程思想吗
    5. 说一下inline
    6. 选个项目讲一下
    7. 写个题吧
        给定一个正整数$n$，计算出满足一下条件的整数$n$的个数：$1 < k < n$，并且$k$和$k + 1$具有相同个数的的正因数。
        比如$14$的正因数有$(1, 2, 7, 14)$，$15$的正因数有$(1, 3, 5, 15)$， $k=14$满足条件。$(3 \leq n \leq 10^7)$
        ```cpp
        // 面试的时候只想到基于调和级数的O(n*log(n))的算法，这里补充一下O(n)的算法
        // 基于线性筛，http://oi-wiki.com/math/number-theory/sieve/#_10
        #include <vector>
        #include <iostream>
        using namespace std;
        vector<int> SieveOfEuler(int n){
            vector<int> ret(n + 1, 0); //约数个数
            vector<int> vis(n + 1, 0); //是否访问标记
            vector<int> prime; // 质数表
            vector<int> num(n + 1, 0); // 最小质数因子出现次数
            ret[1] = 1;
            for(int i = 2; i <= n; ++i){
                if(!vis[i]){
                    vis[i] = 1;
                    prime.push_back(i);
                    ret[i] = 2;
                    num[i] = 1;
                }
                for(auto& it: prime){
                    if(n / it < i) break;
                    vis[it * i] = 1;
                    if(i % it == 0){
                        num[i * it] = num[i] + 1;
                        ret[i * it] = ret[i] / num[i * it] * (num[i * it] + 1);
                        break;
                    }else{
                        num[i * it] = 1;
                        ret[i * it] = ret[i] * 2;
                    }
                }
            }
            return ret;
        }
        int main(){
            int n = 1e7;
            auto&& res = SieveOfEuler(n);
            int ans = 0;
            for(int i = 1; i <= n; ++i){
                if(res[i] == res[i - 1]){
                    ++ans;
                }
            }
            cout << ans << endl;
            return 0;
        }
        ```
    8. 面试官介绍了一下部门情况

## 2022.04.11 Hulu实习二面
- 面试时间：60分钟
- 面试经过：
    1. 自我介绍一下
    2. 讲一下之前的百度实习项目
    3. 先写个题吧
        ```cpp
        // 有两个没有刻度的水桶和一个蓄水量无限的水池，一个容量为x升，
        // 另一个容量为y升，每次取水/倒水视为一次操作，现需要量出z升水
        // Q1：能否实现
        // Q2：最少需要多少次操作
        #include <iostream>
        #include <vector>
        #include <queue>
        #include <map>
        #include <algorithm>
        #include <numeric>

        using namespace std;
        typedef tuple<int, int, int> TII;

        int solve(int x, int y, int z) {
            if (z % gcd(x, y) != 0) return -1; // 不可实现
            queue<tuple<int, int, int>> Q;
            map<tuple<int, int, int>, int> mp;
            tuple<int, int, int> ini{0, 0, 0};
            mp[ini] = 0;
            Q.push(ini);
            while (!Q.empty()) {
                TII it = Q.front();
                Q.pop();
                if (get<2>(it) == z) {
                    return mp[it];
                }
                auto[tx, ty, tz] = it;
                TII nex1{x, ty, tz};    // 将水从池子中灌入到x容器中
                TII nex2{tx, y, tz};    // 将水从池子中灌入到y容器中
                TII nex3{min(tx + ty, x), max(0, tx + ty - x), tz}; // 将水从y容器灌入到x容器中
                TII nex4{max(tx + ty - y, 0), min(tx + ty, y), tz}; // 将水从x容器灌入到y容器中
                TII nex5{tx, 0, tz};    // 清空y容器
                TII nex6{0, ty, tz};    // 清空x容器
                TII nex7{0, ty, tz + tx};   // 将水从x容器中灌入到z
                TII nex8{tx, 0, tz + ty};   // 将水从y容器中灌入到z
                vector<TII> nexs{nex1, nex2, nex3, nex4, nex5, nex6, nex7, nex8};
                for (auto &nx: nexs) {
                    if (!mp.count(nx) and get<2>(nx) <= z) {
                        mp[nx] = mp[it] + 1;
                        Q.push(nx);
                    }
                }
            }
            return -1;
        }

        int main() {
            cout << solve(1, 2, 3) << endl;
            cout << solve(2, 2, 1) << endl;
            cout << solve(2, 2, 2) << endl;
            cout << solve(2, 2, 0) << endl;
            cout << solve(3, 1, 2) << endl;
            return 0;
        }
        ```
    4. 那就再写个题吧
        ```cpp
        // 在电影院中有一排座位，0代表空，1代表已经有人在座位上了，现在又来了2个人，因为疫情需要，把它安排某个没人的座位上，使任意两人直接距离最大，返回其中最短的距离。(座位足够的情况下)

        // 以下是面试的时候和面试官讨论的情况：
        // 所有区间两边都有人 - 要么做一个区间，要么两个不同区间
        // 有1-2个一边没有人的区间
        // 只有一个空区间
        #include <string>
        #include <iostream>
        using namespace std;
        // 求左右端点都是1的最小的区间和最大三个区间的长度
        tuple<int, int, int, int> subSolve(const string& str){
            assert(str.front() == '1' and str.back() == '1');
            int cur = 0;
            int max1 = 0, max2 = 0, max3 = 0;
            int ans = INT_MAX;
            auto&& update = [&](int val){
                if(val > max1){
                    max3 = max2;
                    max2 = max1;
                    max1 = val;
                }else if(val > max2){
                    max3 = max2;
                    max2 = max1;
                }else if(val > max3){
                    max3 = val;
                }
            };
            for(int i = 1; i < (int)str.size(); ++i){
                if(str[i] == '1'){
                    if(i - cur > 1){
                        update(i - cur);
                    }
                    ans = min(ans, i - cur);
                    cur = i;
                }
            }
            return {ans, max1, max2, max3};
        }
        int solve(string str){
            if(str.front() == '1' and str.back() == '1'){ // 左右端点都是1的情况
                auto [minv, mx1, mx2, mx3] = subSolve(str);
                return min(minv, max(mx1 / 3, mx2 / 2));
            }else if(str.front() == '1'){   // 左端点是1的情况
                auto rPos = str.find_last_of('1');
                if(rPos == 0){
                    return (int)(str.size() - 3 - rPos) / 2 + 1;
                }else{
                    auto [minv, mx1, mx2, mx3] = subSolve(str.substr(0, rPos + 1));
                    int len = str.size() - 1 - rPos;
                    int tmpv = solve(str.substr(0, rPos + 1));
                    int ttv = min(len - 1, min(minv, mx1 / 2));
                    return min(minv, max((int)(str.size() - 3 - rPos) / 2 + 1, max(tmpv, ttv)));
                }
            }else if(str.back() == '1'){    // 右端点是1的情况，翻转一下字符串，就得到了上面的一种情况
                reverse(str.begin(), str.end());
                return solve(str);
            }else{  // 左右端点都是0的情况
                auto lPos = str.find_first_of('1');
                if(lPos == string::npos){   // 没有1的情况
                    return str.size() - 1;
                }else{  // 有1的情况
                    int rPos = str.find_last_of('1');
                    int candinate = min(str.size() - rPos - 1, lPos);
                    auto tmp = max(solve(str.substr(0, rPos + 1)), solve(str.substr(lPos)));
                    if(lPos != rPos){
                        auto [minv, x1, x2, x3] = subSolve(str.substr(lPos, rPos - lPos + 1));
                        candinate = min(candinate, minv);
                    }
                    return max(candinate, tmp);
                }
            }
        }

        int main(){
            cout << solve("1000100001") << endl;
            cout << solve("10000000000000100101") << endl;
            cout << solve("1000001001") << endl;
            cout << solve("0000010001") << endl;
            cout << solve("000000000010001") << endl;
            cout << solve("000100000000000000000") << endl;
            return 0;
        }
        ```
### 2022.05.06 Hulu实习二面
- 面试时间: 90分钟
- 面试经过:
    1. 自我介绍
    2. 聊一下百度实习的Contributions
    3. 问了一下简历上第二个项目的情况
    4. 了解Redis吗
    5. 问了一下消息队列的熟悉情况
    6. 最后还有很多时间，写个算法题：[八数码](https://www.acwing.com/problem/content/181/)
        这个题通常有三种解法：1，朴素BFS；2.双向BFS；3.A*算法。其中可以用康托展开来保存访问状态。（再也不敢说康托展开是useless了）
        然后面试的时候，凭着对康托展开微弱的印象，现场手搓，果然搓不出来（寄）。
        然后A*又忘记怎么求八数码的估价。
        然后一紧张，忘记能双向BFS优化一下。
        最后面试官说时间不多了，10分钟写完bfs草草下机（寄）。
## 最后补充一下笔试情况
- 微软：3道编程题，全部完成。代码细节可以优化，时间复杂度无法优化。
- 字节跳动：内推免笔试
- 美团：5道编程题，第二题只过了55%，其余都做出来了
- 阿里巴巴：3道编程题，全部做出来了
- 亚马逊：3道编程题，全部做出来了
- Hulu：3道编程题，全部做出来了