---
title: 万物皆数
math: true
date: 2022-08-27 13:31:59
categories:
    - 模板
tags:
    - 模板
    - CPP
    - 数学
index_img: https://cdn.dianhsu.com/img/2022-08-27-13-28-19.jpeg
---


# 模数(int)
```cpp
class MInt{
public:
    static int selfPow(int base, int p){
        int ret = 1;
        while(p){
            if(p & 1) ret = (ret * 1ll * base) % MOD;
            p >>= 1;
            base = (base * 1ll * base) % MOD;
        }
        return ret;
    }
    MInt(): val(0) {}
    MInt(int tv): val(tv) {}
    MInt operator + (const MInt& arg) const { return MInt((val * 1ll + arg.val) % MOD); }
    MInt operator - (const MInt& arg) const { return MInt((val * 1ll + MOD - arg.val) % MOD); }
    MInt operator * (const MInt& arg) const { return MInt((val * 1ll * arg.val) % MOD); }
    MInt operator / (const MInt& arg) const { return MInt((val * 1ll * selfPow(arg.val, MOD - 2)) % MOD); }
    MInt operator + (const int argv) const { return MInt((val * 1ll + argv) % MOD); }
    MInt operator - (const int argv) const { return MInt((val * 1ll + MOD - argv) % MOD); }
    MInt operator * (const int argv) const { return MInt((val * 1ll * argv) % MOD); }
    MInt operator / (const int argv) const { return MInt((val * 1ll * selfPow(argv, MOD - 2)) % MOD); }
    MInt& operator += (const MInt& arg){
        this->val = (this->val * 1ll + arg.val) % MOD;
        return *this;
    }
    MInt& operator -= (const MInt& arg){
        this->val = (this->val * 1ll + MOD - arg.val) % MOD;
        return *this;
    }
    MInt& operator *= (const MInt& arg){
        this->val = (this->val * 1ll * arg.val) % MOD;
        return *this;
    }
    MInt& operator /= (const MInt& arg){
        this->val = (this->val * 1ll * selfPow(arg.val, MOD - 2)) % MOD;
        return *this;
    }
    MInt& operator += (const int argv){
        this->val = (this->val * 1ll + argv) % MOD;
        return *this;
    }
    MInt& operator -= (const int argv){
        this->val = (this->val * 1ll + MOD - argv) % MOD;
        return *this;
    }
    MInt& operator *= (const int argv){
        this->val = (this->val * 1ll * argv) % MOD;
        return *this;
    }
    MInt& operator /= (const int argv){
        this->val = (this->val * 1ll * selfPow(argv, MOD - 2)) % MOD;
        return *this;
    }
    MInt& operator = (const MInt& arg){
        this->val = arg.val % MOD;
        return *this;
    }
    MInt& operator = (const int argv){
        this->val = argv % MOD;
        return *this;
    }
    bool operator == (const int argv) const{
        return val == argv;
    }
    
    friend MInt operator + (const int argv, const MInt& arg){
        return MInt((arg.val * 1ll + argv) % MOD);
    }
    friend MInt operator - (const int argv, const MInt& arg){
        return MInt((argv * 1ll + MOD - arg.val) % MOD);
    }
    friend MInt operator * (const int argv, const MInt& arg){
        return MInt((arg.val * 1ll * argv) % MOD);
    }
    friend MInt operator / (const int argv, const MInt& arg){
        return MInt((argv * 1ll * MInt::selfPow(arg.val, MOD - 2))% MOD);
    }
    friend istream& operator >> (istream& its, MInt& arg){
        its >> arg.val;
        return its;
    }
    friend ostream& operator << (ostream& ots, const MInt& arg){
        ots << arg.val;
        return ots;
    }
    friend int abs(const MInt& arg){
        return abs(arg.val);
    }
private:
    int val;
};
```

# 素数筛
## 单个正整数判断是不是质数
```cpp
bool isPrime(int x){
    if(x <= 1) return false;
    int cur = 2;
    while(cur * cur <= x){
        if(x % cur != 0){
            return false;
        }
        ++cur;
    }
    return true;
}
```
## 埃拉托斯特尼筛法
```cpp
template<int N>
vector<int> SieveOfEratosthenes() {
    vector<int> prime;
    bitset<N + 1> notPrime;
    notPrime[0] = notPrime[1] = 1;
    for (int i = 2; i <= N; ++i) {
        if (!notPrime[i]) {
            prime.push_back(i);
            if ((long long) i * i <= N) {
                for (int j = i * i; j <= N; j += i) {
                    notPrime[j] = 1;
                }
            }
        }
    }
    return prime;
}

```
## 线性筛（欧式筛）
```cpp
template<int N>
vector<int> SieveOfEuler() {
    vector<int> prime;
    bitset<N + 1> notPrime;
    for (int i = 2; i <= N; ++i) {
        if (!notPrime[i]) {
            prime.push_back(i);
        }
        for (auto it : prime) {
            if ((long long) it * i <= N) {
                notPrime[it * i] = 1;
                if (i % it == 0) {
                    break;
                }
            }else{
                break;
            }
        }
    }
    return prime;
}
```

## 奇数筛
```cpp
template<int N>
vector<int> OddFilter() {
    if (N < 2) return {};
    vector<int> prime{2};
    bitset<N + 1> notPrime;
    notPrime[0] = notPrime[1] = 1;
    for (int i = 3; i * i <= N; i += 2) {
        if (!notPrime[i]) {
            for (int j = i; j * i <= N; j += 2) {
                notPrime[j * i] = 1;
            }
        }
    }
    for (int i = 3; i <= N; i += 2) {
        if (!notPrime[i]) {
            prime.push_back(i);
        }
    }
    return prime;
}
```

# 类欧几里得算法
$$
    f(N, a, b, c) = \sum_{i = 0}^N \lfloor \frac{a \times i + b}{c} \rfloor \\
    g(N, a, b, c) = \sum_{i = 0}^N \lfloor \frac{a \times i + b}{c} \rfloor ^2 \\
    h(N, a, b, c) = \sum_{i = 0}^N i \times \lfloor \frac{a \times i + b}{c} \rfloor
$$

```cpp
#include <iostream>
#include <algorithm>

using namespace std;

const int MOD = 998244353;
int qPow(int b, int p){
    int ret = 1;
    while(p){
        if(p & 1) ret = 1ll * ret * b % MOD;
        b = 1ll * b * b % MOD;
        p >>= 1;
    }
    return ret;
}
const int inv2 = qPow(2, MOD - 2);
const int inv6 = qPow(6, MOD - 2);
template<typename T>
tuple<T, T, T> euclidean(T n, T a, T b, T c){
    T ac = a / c, bc = b / c, m = (a * n + b) / c, n1 = n + 1, n21 = n * 2 + 1;
    if(a == 0){
        return {
            bc * n1 % MOD, 
            bc * n % MOD * n1 % MOD * inv2 % MOD,
            bc * bc % MOD * n1 % MOD
        };
    }
    if(a >= c or b >= c){
        T f = n * n1 % MOD * inv2 % MOD * ac % MOD + bc * n1 % MOD;
        T g = ac * n % MOD * n1 % MOD * n21 % MOD * inv6 % MOD + bc * n % MOD * n1 % MOD * inv2 % MOD;
        T h = ac * ac % MOD * n % MOD * n1 % MOD * n21 % MOD * inv6 % MOD + bc * bc % MOD * n1 % MOD + ac * bc % MOD * n % MOD * n1 % MOD;
        f %= MOD, g %= MOD, h %= MOD;
        auto [tf, tg, th] = euclidean(n, a % c, b % c, c);
        h += th + 2 * bc % MOD * tf % MOD + 2 * ac % MOD * tg % MOD;
        g += tg;
        f += tf;
        return {f % MOD, g % MOD, h % MOD};
    }
    auto [tf, tg, th] = euclidean(m - 1, c, c - b - 1, a);
    T f = (n * m % MOD + MOD - tf) % MOD;
    T g = (n * m % MOD * n1 % MOD + MOD - th + MOD - tf) % MOD * inv2 % MOD;
    T h = (n * m % MOD * (m + 1) % MOD + 2 * (MOD - tg) + 2 * (MOD - tf) + MOD - f) % MOD;
    return {f, g, h};
}
typedef long long ll;
int main(){
    int t;
    cin >> t;
    while(t--){
        ll n, a, b, c;
        cin >> n >> a >> b >> c;
        auto [f, g, h] = euclidean(n, a, b, c);
        cout << f << " " << h << " " << g << endl;
    }
    return 0;
}

```

# 拓展欧几里得

```cpp
template<typename T>
T exgcd(T a, T b, T& x, T& y){
    if(b == 0){
        x = 1;
        y = 0;
        return a;
    }
    T d = exgcd(b, a % b, y, x);
    y -= (a / b) * x;
    return d;
}
```
# 欧拉函数
## 单个欧拉函数
```cpp
int euler_phi(int n) {
  int ans = n;
  for (int i = 2; i * i <= n; i++)
    if (n % i == 0) {
      ans = ans / i * (i - 1);
      while (n % i == 0) n /= i;
    }
  if (n > 1) ans = ans / n * (n - 1);
  return ans;
}
```

## 批量求欧拉函数（线性筛）
```cpp
vector<int> eularFunction(int n){
    vector<int> isPrime(n + 1, 1), phi(n + 1, 0);
    vector<int> prime;
    int cnt = 0;
    isPrime[1] = 0;
    phi[1] = 1;
    for(int i = 2; i <= n; ++i){
        if(isPrime[i]){
            prime.push_back(i);
            phi[i] = i - 1;
        }
        for(auto it: prime){
            if(i * it > n) break;
            isPrime[i * it] = 0;
            if(i % it){
                phi[i * it] = phi[i] * phi[it];
            }else{
                phi[i * it] = phi[i] * it;
                break;
            }
        }
    }
    return phi;
}
```

## 筛法求约数个数（线性筛）
```cpp
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
```

# 中国剩余定理 & 扩展中国剩余定理
```cpp
template<typename T>
T exgcd(T a, T b, T& x, T& y){
    if(b == 0){
        x = 1, y = 0;
        return a;
    }
    T d = exgcd(b, a % b, y, x);
    y -= (a / b) * x;
    return d;
}
template<typename T>
T mul(T b, T n, T p){
    T ans = 0;
    while(n){
        if(n & 1) ans = (ans + b % p) % p;
        b = (b + b) % p;
        n >>= 1;
    }
    return ans;
}
template<typename T>
T crt(vector<pair<T, T>>& args){
    T M = 1, ans = 0, x, y;
    for(auto& it: args) M *= it.first;
    for(auto& it: args){
        T b = M / it.first;
        exgcd(it.first, b, x, y);
        y = (y % it.first + it.first) % it.first;
        ans = (ans + mul(mul(it.second, b, M), y, M)) % M;
    }
    return ans;
}
template<typename T>
bool excrt(pair<T, T>& res, vector<pair<T, T>>& args){
    res = args.front();
    for(int i = 1; i < args.size(); ++i){
        T c = (args[i].second - res.second % args[i].first + args[i].first) % args[i].first;   
        T x, y;
        T v = exgcd(res.first, args[i].first, x, y);
        if(c % v) return false;
        x = mul(x, c / v, args[i].first / v);
        res.second = (res.second + x * res.first);
        res.first *= args[i].first / v;
        res.second = (res.second % res.first + res.first) % res.first;
    }
    return true;
}
```

# 乘法逆元
## 扩展欧几里得算法
```cpp
template<typename T>
T exgcd(T a, T b, T& x, T& y){
    if(b == 0){
        x = 1, y = 0;
        return a;
    }
    T d = exgcd(b, a % b, y, x);
    y -= (a / b) * x;
    return d;
}
```
## 快速幂算法

```cpp
template<typename T>
T qPow(T b, T n, T p){
    T res = 1;
    while(n){
        if(n & 1) res = res * b % p;
        b = b * b % p;
        n >>= 1;
    }
    return res;
}
```

## 批量乘法逆元
> MOD需要是质数
```cpp
vector<int> reverse(int n, int MOD){
    std::vector<int> inv(n + 1, 1);
    for (int i = 2; i <= n; ++i) {
        inv[i] = (long long) (MOD - MOD / i) * inv[MOD % i] % MOD;
    }
    return inv;
}
```

# 阶乘逆元（求组合数）

```cpp
template<typename T = long long, int P = 1000000007>
class Combination{
public:
    Combination(int n): div(n + 1, 1), mul(n + 1, 1){
        for(int i = 1; i <= n; ++i) mul[i] = mul[i - 1] * i % P;
        div[n] = qPow(mul[n], P - 2);
        for(int i = n - 1; i > 0; --i) div[i] = div[i + 1] * (i + 1) % P;
    }
    T operator () (int n, int m){
        if(m < 0) return 0;
        if(m > n) return 0;
        return mul[n] * div[m] % P * div[n - m] % P;
    }
    
private:
    T qPow(T b, T n){
        T ret = 1;
        while(n){
            if(n & 1) ret = ret * b % P;
            b = b * b % P;
            n >>= 1;
        }
        return ret;
    }
    vector<T> div, mul;
};
```
# 卢卡斯定理
对于质数$p$，有
$$
    \binom{n}{m} \bmod p = \binom{\lfloor n / p \rfloor}{\lfloor m / p \rfloor} \cdot \binom{\lfloor n \bmod p \rfloor}{\lfloor m \bmod p \rfloor} \bmod p 
$$
```cpp
template<typename T>
T lucas(T n, T m, T p, const function<T(T, T)>& C){
    if(m == 0) return 1;
    T c = C(n % p, m % p);
    T res = (c * lucas(n / p, m / p, p, C)) % p;
    return res;
}
```

# BSGS
在$a$和$p$互质的情况下，求解
$$
    a ^ x \equiv b \bmod p
$$
```cpp
template<typename T>
T qPow(T b, T n, T p){
    T ret = 1;
    while(n){
        if(n & 1) ret = ret * b % p;
        b = b * b % p;
        n >>= 1;
    }
    return ret;
}
template<typename T>
T BSGS(T a, T b, T p, T c = 1){
    map<T, T> mp;
    T t = (T)sqrt(p) + 1;
    b %= p;
    ll tmp = 1;
    for(int i = 0; i < t; ++i){
        T tv = b * tmp % p;
        mp[tv] = i;
        tmp = (tmp * a) % p;
    }
    a = qPow(a, t, p);
    if(a == 0) return b == 0 ? 1 : -1;
    for(int i = 0; i <= t; ++i){
        ll tv = qPow<T>(a, i, p) * c % p;
        if(mp.count(tv) and i * t - mp[tv] >= 0){
            return i * t - mp[tv];
        }
    }
    return -1;
}
```

# exBSGS
求解
$$
    a ^ x \equiv b \bmod p
$$
```cpp
template<typename T>
T exgcd(T a, T b, T& x, T& y){
    if(b == 0){
        x = 1, y = 0;
        return a;
    }
    T d = exgcd(b, a % b, y, x);
    y -= (a / b) * x;
    return d;
}
template<typename T>
T qPow(T b, T n, T p){
    T ret = 1;
    while(n){
        if(n & 1) ret = ret * b % p;
        b = b * b % p;
        n >>= 1;
    }
    return ret;
}
template<typename T>
T BSGS(T a, T b, T p, T c = 1){
    map<T, T> mp;
    T t = (T)sqrt(p) + 1;
    b %= p;
    ll tmp = 1;
    for(int i = 0; i < t; ++i){
        T tv = b * tmp % p;
        mp[tv] = i;
        tmp = (tmp * a) % p;
    }
    a = qPow(a, t, p);
    if(a == 0) return b == 0 ? 1 : -1;
    for(int i = 0; i <= t; ++i){
        ll tv = qPow<T>(a, i, p) * c % p;
        if(mp.count(tv) and i * t - mp[tv] >= 0){
            return i * t - mp[tv];
        }
    }
    return -1;
}
template<typename T>
T exBSGS(T a, T b, T p){
    a %= p, b %= p;
    if(b == 1 or p == 1) return 0;
    T cnt = 0;
    T d, ad = 1;
    T na = 1;
    while((d = gcd(a, p)) != 1){
        if(b % d) return -1;
        ++cnt;
        b /= d, p /= d;
        ad = ad * (a / d) % p;
        if(ad == b) return cnt;
    }
    T tx, ty;
    T dv = exgcd<T>(ad, p, tx, ty);
    tx = (tx % p + p) % p;
    T ans = BSGS<T>(a, b * tx % p, p);
    if(ans >= 0) ans += cnt;
    return ans;
}
```

# Cayley 公式（Caylay's formula）

完全图 $K_n$ 有 $n^{n - 2}$ 棵生成树。


# 莫比乌斯函数（线性筛）
```cpp
template<int N, typename T = int>
class Mu {
public:
    Mu() : muArr(N + 1), pref(N + 1) {
        bitset<N + 1> notPrime;
        muArr[1] = 1;
        for (int i = 2; i <= N; ++i) {
            if (!notPrime[i]) {
                prime.push_back(i);
                muArr[i] = -1;
            }
            for (auto it : prime) {
                if (N / i >= it) {
                    notPrime[it * i] = 1;
                    if (i % it == 0) {
                        break;
                    } else {
                        muArr[i * it] = -muArr[i];
                    }
                } else {
                    break;
                }
            }
        }
        pref[0] = 0;
        for (int i = 1; i <= N; ++i) {
            pref[i] = pref[i - 1] + muArr[i];
        }
    }

    T& operator[](int i) {
        return muArr[i];
    }

    vector<T> pref;
    vector<T> prime;
private:
    vector<T> muArr;
};
```

# 杜教筛
```cpp
template<int N = 5000000>
struct Du{
  Du(): vis(N + 1, 0), mu(N + 1, 0), musum(N + 1, 0) {
    mu[1] = 1;
    for(int i = 2; i <= N; ++i){
      if(!vis[i]){
        pri.push_back(i);
        mu[i] = -1;
      }
      for(auto& it: pri){
        if(1ll * i * it > N) break;
        vis[i * it] = 1;
        if(i % it){
          mu[i * it] = - mu[i];
        }else{
          mu[i * it] = 0;
          break;
        }
      }
    }
    for(int i = 1; i <= N; ++i) musum[i] = musum[i - 1] + mu[i];
  }
  long long getMuSum(int x){
    if(x <= N) return musum[x];
    if(lazyMu.count(x)) return lazyMu[x];
    long long ret = 1;
    for(long long i = 2, j; i <= x; i = j + 1){
      j = x / (x / i);
      ret -= getMuSum(x / i) * (j - i + 1);
    }
    return lazyMu[x] = ret;
  }
  long long getPhiSum(int x){
    long long ret = 0;
    for(long long i = 1, j; i <= x; i = j + 1){
      j = x / (x / i);
      ret += (getMuSum(j) - getMuSum(i - 1)) * (x / i) * (x / i);
    }
    return (ret - 1) / 2 + 1;
  }
  map<int, long long> lazyMu;
  vector<int> mu, musum, pri;
  vector<bool> vis;
};
```

# 康拓展开
## 正向

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

## 反向
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

# Miller Rabin & Pollard Rho
```cpp
random_device rd;
mt19937_64 gen(rd());
uniform_int_distribution<ll> dis(0);

ll qPow(ll b, ll p, ll mod){
    ll ret = 1;
    while(p){
        if(p & 1) ret = (__int128)ret * b % mod;
        b = (__int128)b * b % mod;
        p >>= 1;
    }
    return ret;
}
bool MillerRabin(ll p){
    if(p < 2) return false;
    if(p < 4) return true;
    ll d = p - 1;
    int r = 0;
    while((d & 1) == 0) ++r, d >>= 1;
    for(ll k = 0; k < 10; ++k){
        ll rv = dis(gen) % (p - 2) + 2;   
        ll x = qPow(rv, d, p);
        if(x == 1 or x == p - 1) continue;
        for(int i = 0; i < r - 1; ++i){
            x = (__int128) x * x % p;
            if(x == p - 1) break;
        }
        if(x != p - 1) return false;
    }

    return true;
}
ll PollardRho(ll n){
    ll c = rand() % (n - 1) + 1;
    ll s = 0, t = 0;
    for(ll goal = 1, val = 1; ; goal *= 2, s = t, val = 1){
        for(ll step = 1; step <= goal; ++step){
            t = ((__int128) t * t + c) % n;
            val = (__int128)val * abs(t - s) % n;
            if(step % 127 == 0){
                ll d = gcd(val, n);
                if(d > 1) return d;
            }
        }
        ll d = gcd(val, n);
        if(d > 1) return d;
    }
}

```
# 线性代数
## 矩阵
>  矩阵模板，搭配模数可以当成矩阵快速幂。
```cpp
template<typename T>
struct Matrix{
    std::vector<T> data;
    int sz;
    // 构造全0矩阵，或者斜对角填上自定义数字
    Matrix(int sz, T v = 0): sz(sz), data(sz * sz, 0){
        int cur = 0;
        do{
            data[cur] = v;
            cur += sz + 1;
        }while(cur < sz * sz);
    }
    //从vector中构造矩阵
    Matrix(int sz, std::vector<T>& arg): sz(sz), data(sz * sz, 0){
        assert(arg.size() >= sz * sz);
        for(int i = 0; i < sz * sz; ++i) data[i] = arg[i];
    }
    //从vector中构造矩阵，右值
    Matrix(int sz, std::vector<T>&& arg): sz(sz), data(sz * sz, 0){
        assert(arg.size() >= sz * sz);
        for(int i = 0; i < sz * sz; ++i) data[i] = arg[i];
    }
    Matrix operator + (const Matrix& arg) const {
        assert(sz == arg.sz);
        Matrix ret(sz);
        for(int i = 0; i < sz * sz; ++i){
            ret.data[i] = data[i] + arg.data[i];
        }
        return ret;
    }
    Matrix operator * (const Matrix& arg) const {
        assert(sz == arg.sz);
        Matrix ret(sz);
        for(int i = 0; i < sz; ++i){
            for(int j = 0; j < sz; ++j){
                for(int k = 0; k < sz; ++k){
                    ret.data[i * sz + j] += data[i * sz + k] * arg.data[k * sz + j];
                }
            }
        }
        return ret;
    }
    Matrix operator - (const Matrix& arg) const {
        assert(sz == arg.sz);
        Matrix ret(sz);
        for(int i = 0; i < sz * sz; ++i) ret.data[i] = data[i] - arg.data[i];
        return ret;
    }
    friend std::ostream & operator << (std::ostream& ots, const Matrix& arg){
        for(int i = 0; i < arg.sz; ++i){
            for(int j = 0; j < arg.sz; ++j){
                if(j) ots << " ";
                ots << arg.data[i * arg.sz + j];
            }
            if(i + 1 != arg.sz) ots << "\n";
        }
        return ots;
    }
};
```

## 高斯消元
```cpp
template<typename T>
struct Gauss{
    Gauss(int argR, int argC): r(argR), c(argC), mat(r, vector<T>(c, 0)), idx(r, 0){
        assert(argC >= argR);
        iota(idx.begin(), idx.end(), 0);
    }
    T& operator () (int row, int col){
        return mat[row][col];
    }
    int r, c;
    friend istream& operator >> (istream& its, Gauss& arg){
        for(int i = 0; i < arg.r; ++i){
            for(int j = 0; j < arg.c; ++j){
                its >> arg(i, j);
            }
        }
        return its;
    }
    friend ostream& operator << (ostream& ots, Gauss& arg){
        for(int i = 0; i < arg.r; ++i){
            for(int j = 0; j < arg.c; ++j){
                ots << arg(arg.idx[i], j);
                if(j + 1 != arg.c) ots << " ";
            }
            if(i + 1 != arg.r) ots << "\n";
        }
        return ots;
    }
    vector<vector<T>> mat;
    vector<int> idx;
    bool elimination(const function<bool(T)>& isZero, const function<T(T)>& inv){
        for(int i = 0; i < r; ++i){
            int cur = i;
            for(int j = i + 1; j < r; ++j){
                if(abs(mat[idx[j]][i]) > abs(mat[idx[cur]][i])){
                    cur = j;
                }
            }
            swap(idx[i], idx[cur]);
            if(isZero(mat[idx[i]][i])) return false;
            T mul = inv(mat[idx[i]][i]);
            for(int j = i; j < c; ++j){
                mat[idx[i]][j] *= mul;
            }
            for(int i1 = 0; i1 < r; ++i1){
                if(i1 == i) continue;
                T cmul = mat[idx[i1]][i];
                for(int j = i; j < c; ++j){
                    mat[idx[i1]][j] -= mat[idx[i]][j] * cmul;
                }
            }
        }
        return true;
    }
};
```


## 线性基
```cpp
struct LBase{
  vector<long long> _data;
  LBase(): _data(64, 0){}
  bool insert(long long x){
    for(int i = 63 - __builtin_clzll(x); i >= 0; --i){
      if((x >> i) & 1){
        if(_data[i]) x ^= _data[i];
        else{
          _data[i] = x;
          break;
        }
      }
    }
    return x > 0;
  }
  LBase& operator += (const LBase& arg){
    for(auto ptr = arg._data.rbegin(); ptr != arg._data.rend(); ++ptr){
      this->insert(*ptr);
    }
    return *this;
  }
  long long query(){
    long long ret = 0;
    for(auto ptr = _data.rbegin(); ptr != _data.rend(); ++ptr){
      if(*ptr){
        if((ret ^ (*ptr)) > ret) ret ^= *ptr;
      }
    }
    return ret;
  }
  int count(){
    int ret = 0;
    for(auto& it: _data) if(it) ++ret;
    return ret;
  }
};
```

# 自适应辛普森

```cpp
template<typename T>
T simpson(T l, T r, const function<T(T)>& f){
  T mid = (l + r) / 2;
  return (r - l) * (f(l) + 4 * f(mid) + f(r)) / 6;
}

template<typename T>
T asr(T l, T r, T delta, T ans, int step, const function<T(T)>& f){
  T mid = (l + r) / 2;
  T fl = simpson<T>(l, mid, f), fr = simpson<T>(mid, r, f);
  if(abs(fl + fr - ans) <= 15 * delta and step < 0){
    return fl + fr + (fl + fr - ans) / 15;
  }
  return asr(l, mid, delta / 2, fl, step - 1, f) + asr(mid, r, delta / 2, fr, step - 1, f);
}
template<typename T = double>
T adaptiveSimpson(T l, T r, T delta, const function<T(T)>& f){
  return asr<T>(l, r, delta, simpson<T>(l, r, f), 12, f);
}
```

# 多项式
## 快速傅立叶变换
```cpp
template<typename T>
void butterflyDiagram(vector<complex<T>>& vec){
    assert(__builtin_popcount(vec.size()) == 1);
    vector<int> rev(vec.size());
    for(int i = 0; i < vec.size(); ++i){
        rev[i] = rev[i >> 1] >> 1;
        if(i & 1){
            rev[i] |= (vec.size() >> 1);
        }
    }
    for(int i = 0; i < vec.size(); ++i){
        if(i < rev[i]){
            swap(vec[i], vec[rev[i]]);
        }
    }
}
// on == 1 时是 DFT，on == -1 时是 IDFT
template<typename T>
void fft(vector<complex<T>>& vec, int on){
    assert(__builtin_popcount(vec.size()) == 1);
    butterflyDiagram(vec);
    for(int h = 1; h < vec.size(); h <<= 1){
        complex<T> wn(cos(M_PI / h), sin(on * M_PI / h));
        for(int j = 0; j < vec.size(); j += h * 2){
            complex<T> w(1, 0);
            for(int k = j; k < j + h; ++k){
                assert(k < vec.size() and h + k < vec.size());
                auto u = vec[k];
                auto t = w * vec[k + h];
                vec[k] = u + t;
                vec[k + h] = u - t;
                w *= wn;
            }
        }
    }
    if(on == -1){
        for(auto& it: vec){
            it.real(it.real() / vec.size());
        }
    }
}
```
