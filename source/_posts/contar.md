---
title: 康托展开
date: 2022-05-10 17:55:58
tags: 
    - 康托展开
    - 算法
    - 数论
categories: 算法
---


参考：[康拓展开_维基百科](https://zh.wikipedia.org/wiki/%E5%BA%B7%E6%89%98%E5%B1%95%E5%BC%80)

康拓展开是一个全排列到一个自然数的双射，常用于构建hash表时的空间压缩。
康拓展开的实质是计算**当前排列在所有由小到大全排列中的顺序**，因此是可逆的。

### 公式

$$X=a_0(n-1)! + a_{1}(n-2)! + \dots + a_{n-1} \cdot 0!$$
其中，$a_i$为整数，并且$0 \leq a_i < i, 1 \leq i \leq n$
$a_i$的意义参见举例中的解释部分

### 举例
例如，`3 5 7 4 1 2 9 6 8` 展开为 `98884`。因为`X=2*8!+3*7!+4*6!+2*5!+0*4!+0*3!+2*2!+0*1!+0*0!=98884`。

解释：
排列的第一位是3，比3小的数有两个，以这样的数开始的排列有8!个，因此第一项为2\*8!
排列的第二位是5，比5小的数有1、2、3、4，由于3已经出现，因此共有3个比5小的数，这样的排列有7!个，因此第二项为3\*7!
以此类推，直至0\*0!

### 参考模板

```cpp
/**
 * @brief 康拓展开
 * @param t 排列，这里设定排列的长度是9
 * @return Contar值
 * @author dianhsu
 **/
int radix[] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320};
template<int LEN=9>
int Contar(int* t){
    int ret = 0;
    for(int i = 0; i < LEN; ++i){
        int tmp = 0;
        for(int j = i + 1; j < LEN; ++j){
            if(t[i] > t[j]){
                ++tmp;
            }
        }
        ret += radix[LEN - 1 - i] * tmp;
    }
    return ret;
}
```

既然康托展开是一个双射，那么一定可以通过康托展开值求出原排列，即可以求出 $n$ 的全排列中第 $x$ 大排列。

```cpp
/**
 * @brief 康拓展开的逆运算
 * @param contar_val Contar 值
 * @param t 返回的Contar序列
 * @author dianhsu
 * */
int radix[] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320};
template<int LEN=9>
void ReverseContar(int contar_val, int* t){
    int vis[LEN];
    memset(vis, 0, sizeof vis);
    for(int i = 0; i < LEN; ++i){
        int idx = contar_val / radix[LEN - 1 - i];
        contar_val = contar_val % radix[LEN - 1 - i];
        for(int j = 0; j < LEN; ++j){
            if(vis[j] == 0){
                if(idx == 0){
                    vis[j] = 1;
                    t[i] = j;
                    break;
                }else{
                    --idx;
                }
            }
        }
    }
}
```