---
title: LCP 58. 积木拼接
date: 2022-05-13 14:25:24
tags: 
    - LeetCode
    - LC春季赛
    - 立体几何
index_img: https://cdn.dianhsu.top/blog/505102-anime-series-love-live.jpeg
categories: LeetCode
---




欢迎各位勇者来到力扣城，本次试炼主题为「积木拼接」。
勇者面前有 `6` 片积木（厚度均为 1），每片积木的形状记录于二维字符串数组 `shapes` 中，`shapes[i]` 表示第 `i` 片积木，其中 `1` 表示积木对应位置无空缺，`0` 表示积木对应位置有空缺。

<!-- more -->
例如 `["010","111","010"]` 对应积木形状为
![image.png](https://pic.leetcode-cn.com/1616125620-nXMCxX-image.png)

拼接积木的规则如下：
- 积木片可以旋转、翻面
- 积木片边缘必须完全吻合才能拼接在一起
- **每片积木片 `shapes[i]` 的中心点在拼接时必须处于正方体对应面的中心点**

例如 `3*3`、`4*4` 的积木片的中心点如图所示（红色点）：
![middle_img_v2_c2d91eb5-9beb-4c06-9726-f7dae149d86g.png](https://pic.leetcode-cn.com/1650509082-wObiEp-middle_img_v2_c2d91eb5-9beb-4c06-9726-f7dae149d86g.png){:height="150px"}


请返回这 6 片积木能否拼接成一个**严丝合缝的正方体**且每片积木正好对应正方体的一个面。

**注意：**
- 输入确保每片积木均无空心情况（即输入数据保证对于大小 `N*N` 的 `shapes[i]`，内部的 `(N-2)*(N-2)` 的区域必然均为 1）
- 输入确保每片积木的所有 `1` 位置均连通

**示例 1：**
>输入：`shapes = [["000","110","000"],["110","011","000"],["110","011","110"],["000","010","111"],["011","111","011"],["011","010","000"]]`
>
>输出：`true`
>
>解释：
![cube.gif](https://pic.leetcode-cn.com/1616125823-hkXAeN-cube.gif)

**示例 2：**
>输入：`shapes = [["101","111","000"],["000","010","111"],["010","011","000"],["010","111","010"],["101","111","010"],["000","010","011"]]`
>
>输出：`false`
>
>解释： 
>由于每片积木片的中心点在拼接时必须处于正方体对应面的中心点，积木片 `["010","011","000"]` 不能作为 `["100","110","000"]` 使用，因此无法构成正方体


**提示：**
- `shapes.length == 6`
- `shapes[i].length == shapes[j].length`
- `shapes[i].length == shapes[i][j].length`
- `3 <= shapes[i].length <= 10`


> https://leetcode.cn/problems/De4qBB/


这个题目比较困难的地方就是记录方阵的翻转、旋转状态

# 方阵的翻转，旋转和转置模板

为了能够高效的表示当前方阵的状态，我们用方阵的四个角点表示方阵当前的状态。

比如一个$3 \times 3$的方阵，我们用`array<pair<int, int>, 4>`来存放这个方阵的四个角，依次分别是：左上角$(0, 0)$、右上角$(0, y)$、左下角$(x, 0)$和右下角$(x, y)$。
## 翻转操作
```
110    上下进行翻转    000
010  ------------->  010
000                  110
```
那么他四个点的坐标就是
```
(0,0)  (0,3)      上下进行翻转      (3,0)  (3,3) 
                ------------->
(3,0)  (3,3)                      (0,0)  (0,3)
```
对应代码：
```cpp
void mirror(int dr = 1){
    if(dr == 1){
        // 左右翻转
        swap(vec[0], vec[1]);
        swap(vec[2], vec[3]);
    }else{
        // 上下翻转
        swap(vec[0], vec[2]);
        swap(vec[1], vec[3]);
    }
}
```
## 转置操作
```
110      转置方阵     100
010  ------------->  110
000                  000
```
那么他四个点的坐标就是
```
(0,0)  (0,3)        转置方阵       (0,0)  (3,0) 
                ------------->
(3,0)  (3,3)                      (0,3)  (3,3)
```
对应代码：
```cpp
void transpose(int dr = 1){
    if(dr == 1){
        // 沿着y = x 翻转
        swap(vec[1], vec[2]);
    }else{
        // 沿着x + y = n 翻转
        swap(vec[0], vec[3]);
    }
}
```
## 旋转操作
```
110   顺时针旋转90度   001
010  ------------->  011
000                  000
```
那么他四个点的坐标就是
```
(0,0)  (0,3)     顺时针旋转90度     (3,0)  (0,0) 
                ------------->
(3,0)  (3,3)                      (3,3)  (0,3)
```
对应代码（旋转可以用转置+翻转来实现）：
```cpp
void rotate(int dr = 1){
    transpose();
    if(dr == 1){
        // 顺时针
        mirror(1);
    }else{
        // 逆时针
        mirror(0);
    }
}
```


可以从上面看出来，对图形的操作，就可以表示为对四个角的二维方阵的操作。

因为翻转之后，我们需要知道新的图形的x，y的坐标轴的变化，比如
```
(0,0)  (0,3)     顺时针旋转90度     (3,0)  (0,0) 
                ------------->
(3,0)  (3,3)                      (3,3)  (0,3)
```
这个图形旋转之前的坐标轴的单位变化分别是$dx = (1, 0)$和$dy = (0, 1)$，顺时针旋转90度之后的单位变化$dx = (0, 1)$，$dy = (-1, 0)$。
为了方便记录当前的单位变化$dx$和$dy$，我们在每次翻转、旋转和转置的时候，重新计算一次$dx$和$dy$。计算的代码如下：
```cpp
void update(){
    int xlim = abs(vec[2].first - vec[0].first) + abs(vec[2].second - vec[0].second);
    int ylim = abs(vec[1].first - vec[0].first) + abs(vec[1].second - vec[0].second);
    assert(xlim > 0 and ylim > 0);
    dx = Point{(vec[2].first - vec[0].first) / xlim, (vec[2].second - vec[0].second) / xlim};
    dy = Point{(vec[1].first - vec[0].first) / ylim, (vec[1].second - vec[0].second) / ylim};
}
```
那么最终，我们就可以通过左上角的坐标，和单位坐标的变化$dx$和$dy$，来映射得到原始的坐标。
代码如下所示：
```cpp
Point mapping(Point p){
    return {vec[0].first + dx.first * p.first + dy.first * p.second, vec[0].second + dx.second * p.first + dy.second * p.second};
}
```
那么最终完整的矩阵模板：
```cpp
class Rectangle{
public:
    typedef pair<int, int> Point;
    Rectangle(int sx, int sy) : dx({1, 0}), dy({0, 1}), vec({Point{0, 0}, Point{0, sy - 1}, Point{sx - 1, 0}, Point{sx - 1, sy - 1}}){}
    void mirror(int dr = 1){
        if(dr == 1){
            // 左右翻转
            swap(vec[0], vec[1]);
            swap(vec[2], vec[3]);
        }else{
            // 上下翻转
            swap(vec[0], vec[2]);
            swap(vec[1], vec[3]);
        }
        update();
    }
    void transpose(int dr = 1){
        if(dr == 1){
            // 沿着y = x 翻转
            swap(vec[1], vec[2]);
        }else{
            // 沿着x + y = n 翻转
            swap(vec[0], vec[3]);
        }
        update();
    }
    void rotate(int dr = 1){
        transpose();
        if(dr == 1){
            // 顺时针
            mirror(1);
        }else{
            // 逆时针
            mirror(0);
        }
        update();
    }
    Point mapping(Point p){
        return {vec[0].first + dx.first * p.first + dy.first * p.second, vec[0].second + dx.second * p.first + dy.second * p.second};
    }
    // 当前状态下，x轴的方向和y轴的方向
    Point dx, dy;
    // 当前状态下的方阵四个角点的坐标
    array<Point, 4> vec;
private:
    void update(){
        int xlim = abs(vec[2].first - vec[0].first) + abs(vec[2].second - vec[0].second);
        int ylim = abs(vec[1].first - vec[0].first) + abs(vec[1].second - vec[0].second);
        assert(xlim > 0 and ylim > 0);
        dx = Point{(vec[2].first - vec[0].first) / xlim, (vec[2].second - vec[0].second) / xlim};
        dy = Point{(vec[1].first - vec[0].first) / ylim, (vec[1].second - vec[0].second) / ylim};
    }

};
```
# 本题的实现
## 前置内容
我们首先设计了6个位置，就是立方体的展开图。如下所示：
```
      00000             
      00000             
      00000             
      00000             
      00000             

11111 22222 33333 44444 
11111 22222 33333 44444 
11111 22222 33333 44444 
11111 22222 33333 44444 
11111 22222 33333 44444 

55555                   
55555                   
55555                   
55555                   
55555                   
```
我们把位置按照这个形状进行设计，是因为可以和方便的计算他的相邻边。具体可看后面相邻边的数字变化。

然后定义每个矩阵的边的顺序【0，1，2，3】，依次是【上，右，下，左】。
比如0号位置的下方和2号位置的上方相邻，就构成一个边的四元组「0号位置，2号位置，下方，上方」，[0, 2, 2, 0]。
比如0号位置的左边和1号位置的上方相邻，就构成一个边的四元组「0号位置，1号位置，左边，上方」，[0, 1, 3, 0]。

那么写出0号位置所相邻边的四元组：
```
[0, 1, 3, 0]
[0, 2, 2, 0]
[0, 3, 1, 0]
[0, 4, 0, 0]
```
然后是5号位置相邻边的四元组：
```
[5, 1, 0, 2]
[5, 2, 1, 2]
[5, 3, 2, 2]
[5, 4, 3, 2]
```
然后就是其他四条边：
```
[1, 2, 1, 3]
[2, 3, 1, 3]
[3, 4, 1, 3]
[4, 1, 1, 3]
```

为了按照顺序获取方阵的四条边，我们先定义了个方阵，然后逆时针旋转四次，每次旋转，获取一次当前位置的第一条边。
```cpp
Rectangle rec(sz, sz);
vector<Rectangle> recd;
for(int i = 0; i < 4; ++i){
    recd.push_back(rec);
    rec.rotate(0);
}
```

## 题目思路
我们本题使用搜索检查每个位置是否满足。首先固定第一个方阵，我们把它固定放在0位置。然后每个位置尝试将其他的方阵旋转或者翻转放入。
对于立体图形的边，我们要求不能相邻的边在同一个位置具有相同的元素。
对于立体图形的角，我们要求不能两个边同时出现$1$，为了避免三个相邻面共享的同一个角都是0，我们一开始就先计算1个总个数，要求1个总个数刚刚好。
完整代码如下：
```cpp
class Rectangle{
public:
    typedef pair<int, int> Point;
    Rectangle(int sx, int sy) : dx({1, 0}), dy({0, 1}), vec({Point{0, 0}, Point{0, sy - 1}, Point{sx - 1, 0}, Point{sx - 1, sy - 1}}){}
    void mirror(int dr = 1){
        if(dr == 1){
            // 沿着x轴翻转
            swap(vec[0], vec[1]);
            swap(vec[2], vec[3]);
        }else{
            // 沿着y轴翻转
            swap(vec[0], vec[2]);
            swap(vec[1], vec[3]);
        }
        update();
    }
    void transpose(int dr = 1){
        if(dr == 1){
            // 沿着y = x 翻转
            swap(vec[1], vec[2]);
        }else{
            // 沿着x + y = n 翻转
            swap(vec[0], vec[3]);
        }
        update();
    }
    void rotate(int dr = 1){
        transpose();
        if(dr == 1){
            // 顺时针
            mirror(1);
        }else{
            // 逆时针
            mirror(0);
        }
        update();
    }
    Point mapping(Point p){
        return {vec[0].first + dx.first * p.first + dy.first * p.second, vec[0].second + dx.second * p.first + dy.second * p.second};
    }
    Point dx, dy;
    array<Point, 4> vec;
private:
    void update(){
        int xlim = abs(vec[2].first - vec[0].first) + abs(vec[2].second - vec[0].second);
        int ylim = abs(vec[1].first - vec[0].first) + abs(vec[1].second - vec[0].second);
        assert(xlim > 0 and ylim > 0);
        dx = Point{(vec[2].first - vec[0].first) / xlim, (vec[2].second - vec[0].second) / xlim};
        dy = Point{(vec[1].first - vec[0].first) / ylim, (vec[1].second - vec[0].second) / ylim};
    }

};
class Solution {
public:
    bool composeCube(vector<vector<string>>& shapes) {
        int sz = shapes[0].size();
        int cnt = sz * sz * 2 + (sz - 1) * (sz - 2) * 4;
        for(auto& vec: shapes) {
            for(auto& row: vec){
                for(auto& c: row){
                    if(c == '1') --cnt;
                }
            }
        }
        if(cnt != 0) return false;
        typedef Rectangle::Point Point;
        Rectangle rec(sz, sz);
        vector<Rectangle> recd;
        for(int i = 0; i < 4; ++i){
            recd.push_back(rec);
            //recd.back().debug();
            rec.rotate(0);
        }
        vector<Rectangle> recs(6, Rectangle{sz, sz});
        auto&& isCon = [&](int x, int y, int sx, int sy){
            for(int i = 0; i < sz; ++i){
                auto px = recd[sx].mapping({0, i});
                auto py = recd[sy].mapping({0, sz - 1 - i});
                auto ppx = recs[x].mapping(px);
                auto ppy = recs[y].mapping(py);
                if(i == 0 or i == sz - 1){
                    if(shapes[x][ppx.first][ppx.second] == shapes[y][ppy.first][ppy.second] and shapes[y][ppy.first][ppy.second] == '1'){
                        return false;
                    }
                }else if(shapes[x][ppx.first][ppx.second] == shapes[y][ppy.first][ppy.second]){
                    return false;
                }
            }
            return true;
        };
        auto&& show = [&](int i, int x, int y){
            return recs[i].mapping({x, y});
        };
        vector<int> idx(6);
        vector<vector<int>> dr = {{-1, 0, -1, -1}, {1, 2, 3, 4}, {5, -1, -1, -1}};
        auto&& print = [&](int q){
            for(int i = 0; i < 3; ++i){
                for(int j = 0; j < sz; ++j){
                    for(int k = 0; k < 4; ++k){
                        for(int l = 0; l < sz; ++l){
                            if(dr[i][k] < 0) cout << " ";
                            else if(dr[i][k]  > q) cout << "?";
                            else{
                                auto rt = show(idx[dr[i][k]], j, l);
                                cout << shapes[idx[dr[i][k]]][rt.first][rt.second];
                            }
                        }
                        cout << " ";
                    }
                    cout << endl;
                }
                cout << endl;
            }
        };
        auto&& check = [&](int sz){

            bool ok = true;
            for(int i = 0; i < 4 and i + 1 <= sz and ok; ++i){
                if(!isCon(idx[0], idx[i + 1], 3 - i, 0)){
                    ok = false;
                }
            }
            for(int i = 0; i < 4 and i + 1 <= sz and (i + 1) % 4 + 1 <= sz and ok; ++i){
                if(!isCon(idx[i + 1], idx[(i + 1) % 4 + 1], 1, 3)) ok = false;
            }
            if(sz == 5){
                for(int i = 0; i < 4 and ok; ++i){
                    if(!isCon(idx[5], idx[i + 1], i, 2)) ok = false;
                }
            }

//            if(ok){
//                print(sz);
//                cout << "ok" << endl;
//            }

            return ok;
        };
        idx[0] = 0;
        vector<int> vis(6, 0);
        vis[0] = 1;
        auto&& dfs = [&](auto&& self, int cur) -> bool{
            if(cur >= 6) {
                return true;
            }
            for(int i = 1; i < 6; ++i){
                if(vis[i] == 0){
                    idx[cur] = i;
                    vis[i] = 1;
                    for(int m = 0; m < 2; ++m){
                        for(int r = 0; r < 4; ++r){
                            if(check(cur)) {
                                if(self(self, cur + 1)) return true;
                            }
                            recs[i].rotate();
                        }
                        recs[i].mirror();
                    }
                    vis[i] = 0;
                }
            }
            return false;
        };
        if(dfs(dfs, 1)) return true;
        recs[0].mirror();
        if(dfs(dfs, 1)) return true;
        return false;
    }
};
```

最后打印一下第一个样例的匹配情况：
```
// 样例1
    000         
    110         
    000         

001 011 011 011 
011 010 110 111 
010 000 011 011 

001             
011             
001   
```
