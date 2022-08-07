---
title: 算法模板
date: 2022-05-10 16:36:14
tags: [算法, 数学, 图论, 几何, 字符串]
categories: 算法
math: true
index_img: https://cdn.dianhsu.com/blog%2Ffd68b9d44d2dc4cf3606a9e01cdca850634b8d4f.jpeg
---

算法竞赛编程模板，主要用于线上比赛，可以直接从这里复制代码提交到OJ平台，代码风格主要是函数式和面向对象。

## 字符串
### KMP字符串匹配
```cpp
class KMP {
public:
    /**
     * @brief 统计目标串中有多少个模式串
     * @param target 目标字符串
     * @param pattern 模式字符串
     * */
    static int solve(string& target, string& pattern) {
        int ans = 0;
        int idxTarget = 0, idxPattern = 0;
        vector<int> next(std::move(_prefix(pattern)));
        while (idxTarget < target.length()) {
            while (idxPattern != -1 and pattern[idxPattern] != target[idxTarget]) {
                idxPattern = next[idxPattern];
            }
            ++idxTarget; ++idxPattern;
            if (idxPattern >= pattern.length()) {
                ++ans;
                idxPattern = next[idxPattern];
            }
        }
        return ans;
    }
private:
    static vector<int> _prefix(const string& pattern) {
        int i = 0, j = -1;
        vector<int> ret(pattern.length() + 1, -1);
        while (i < pattern.length()) {
            while (j != -1 and pattern[i] != pattern[j]) j = ret[j];
            if (pattern[++i] == pattern[++j]) {
                ret[i] = ret[j];
            } else {
                ret[i] = j;
            }
        }
        return ret;
    }
};
```
### Manacher算法
```cpp
class Manacher {
public:
    static std::string forward(const std::string& s) {
        std::string Ma = "^#";
        for (auto it: s) {
            Ma += it;
            Ma += '#';
        }
        Ma += '$';
        int len = Ma.length();
        std::vector<int> Mp(len, 0);
        int mx = 0, id = 0;
        int maxPos = 0;
        for (int i = 1; i < len - 1; ++i) {
            Mp[i] = mx > i ? std::min(Mp[(id << 1) - i], mx - i) : 1;
            while (Ma[i + Mp[i]] == Ma[i - Mp[i]]) Mp[i]++;
            if (Mp[i] > Mp[maxPos]) {
                maxPos = i;
            }
            if (i + Mp[i] > mx) {
                mx = i + Mp[i];
                id = i;
            }
        }
        std::string ret;
        for (int i = maxPos - Mp[maxPos] + 1; i < maxPos + Mp[maxPos]; ++i) {
            if (isalnum(Ma[i])) {
                ret += Ma[i];
            }
        }
        return ret;
    }
};

```
### 字符串Hash
```cpp
class StringHash{
public:
    static unsigned BKDR(const std::string& str){
        unsigned seed = 131; // 31 131 1313 13131 131313 etc..
        unsigned hash = 0;
        for(auto c: str){
            hash = hash * seed + c;
        }
        return (hash & 0x7FFFFFFF);
    }
    static unsigned AP(const std::string& str){
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
    static unsigned DJB(const std::string& str){
        unsigned hash = 5381;
        for(auto c: str){
            hash += (hash << 5) + c;
        }
        return (hash & 0x7FFFFFFF);
    }
    static unsigned JS(const std::string& str){
        unsigned hash = 1315423911;
        for(auto c: str) hash ^= ((hash << 5) + c + (hash >> 2));
        return (hash & 0x7FFFFFFF);
    }
    static unsigned SDBM(const std::string& str){
        unsigned hash = 0;
        for(auto c: str) hash = c + (hash << 6) + (hash << 16) - hash;
        return (hash & 0x7FFFFFFF);
    }
    static unsigned PJW(const std::string& str){
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
    static unsigned ELF(const std::string& str){
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
};
```
### AC自动机(AC Automaton)

提供插入、构建、查询三个方法。

```cpp
namespace Automaton {
struct ACNode{
    vector<int> nex;
    int fail;
    int cnt;
    ACNode() : nex(26, 0), cnt(0), fail(0) { }
};
class AC{
public:
    AC(): nodes(1) { }
    void insert(const string& arg){
        int cur = 0;
        for(auto& c: arg){
            int to = c - 'a';
            if(!nodes[cur].nex[to]){
                nodes[cur].nex[to] = (int)nodes.size();
                nodes.emplace_back();
            }
            cur = nodes[cur].nex[to];
        }
        nodes[cur].cnt++;
    }
    void build(){
        queue<int> Q;
        for(int i = 0; i < 26; ++i) {
            if(nodes[0].nex[i]){
                Q.push(nodes[0].nex[i]);
            }
        }
        while(!Q.empty()){
            int cur = Q.front();
            Q.pop();
            for(int i = 0; i < 26; ++i){
                if(nodes[cur].nex[i]){
                    nodes[nodes[cur].nex[i]].fail = nodes[nodes[cur].fail].nex[i];
                    Q.push(nodes[cur].nex[i]);
                }else{
                    nodes[cur].nex[i] = nodes[nodes[cur].fail].nex[i];
                }
            }
        }
    }
    int query(const string& arg){
        int cur = 0, ans = 0;
        for(auto& c: arg){
            cur = nodes[cur].nex[c - 'a'];
            for(int j = cur; j and nodes[j].cnt != -1; j = nodes[j].fail){
                ans += nodes[j].cnt;
                nodes[j].cnt = -1;
            }
        }
        return ans;
    }
private:
    vector<ACNode> nodes;
};
}
```


### 后缀数组
```cpp
class SuffixArray {
private:
    void radixSort(int n, int m, int w, vector<int>& sa, vector<int>& rk, vector<int>& bucket, vector<int>& idx) {
        fill(all(bucket), 0);
        for (int i = 0; i < n; ++i) idx[i] = sa[i];
        for (int i = 0; i < n; ++i) ++bucket[rk[idx[i] + w]];
        for (int i = 1; i < m; ++i) bucket[i] += bucket[i - 1];

        for (int i = n - 1; i >= 0; --i) sa[--bucket[rk[idx[i] + w]]] = idx[i];
        fill(all(bucket), 0);
        for (int i = 0; i < n; ++i) idx[i] = sa[i];
        for (int i = 0; i < n; ++i) ++bucket[rk[idx[i]]];
        for (int i = 1; i < m; ++i) bucket[i] += bucket[i - 1];
        for (int i = n - 1; i >= 0; --i) sa[--bucket[rk[idx[i]]]] = idx[i];
    }
public:
    SuffixArray(const string& s) :
        n(s.length() + 1),
        m(max((int) s.length() + 1, 300)),
        rk(2, vector<int>((s.length() + 1) << 1)),
        bucket(max((int) s.length() + 1, 300)),
        idx(s.length() + 1),
        sa(s.length() + 1),
        ht(s.length()) {

        for (int i = 0; i < n; ++i) ++bucket[rk[0][i] = s[i]];
        for (int i = 1; i < m; ++i) bucket[i] += bucket[i - 1];
        for (int i = n - 1; i >= 0; --i) sa[--bucket[rk[0][i]]] = i;
        int pre = 1;
        int cur = 0;
        for (int w = 1; w < n; w <<= 1) {
            swap(cur, pre);
            radixSort(n, m, w, sa, rk[pre], bucket, idx);
            for (int i = 1; i < n; ++i) {
                if (rk[pre][sa[i]] == rk[pre][sa[i - 1]] and rk[pre][sa[i] + w] == rk[pre][sa[i - 1] + w]) {
                    rk[cur][sa[i]] = rk[cur][sa[i - 1]];
                } else {
                    rk[cur][sa[i]] = rk[cur][sa[i - 1]] + 1;
                }
            }
        }
        for (int i = 0, k = 0; i < n - 1; ++i) {
            if (k) --k;
            while (s[i + k] == s[sa[rk[cur][i] - 1] + k]) ++k;
            ht[rk[cur][i] - 1] = k;
        }
    }
    vector<int> sa;
    vector<int> ht;
private:
    int n, m;
    vector<vector<int>> rk;
    vector<int> bucket, idx;
};
```
## 图论

### 并查集（DSU）
> 能Copy的时候，就不用手搓了

```cpp
class DSU{
public:
    explicit DSU(int size_): sz(size_), fa(size_, 0), cnt(size_, 1) {}
    int tf(int x){
        return x == fa[x] ? x : fa[x] = tf(fa[x]);
    }
    bool mg(int x, int y){
        int tx = tf(x), ty = tf(y);
        if(tx != ty){
            if(cnt[tx] >= cnt[ty]){ // 启发式合并
                fa[ty] = tx;
                cnt[tx] += cnt[ty];
            }else{
                fa[tx] = ty;
                cnt[ty] += cnt[tx];
            }
            return true;
        }
        return false;
    }
    pair<int, int> operator [] (const int idx) {
        return {tf(idx), cnt[tf(idx)]};
    }
    int size(){
        return sz;
    }
private:
    int sz;
    vector<int> fa, cnt;
};

```

### 网络流

#### 最大流(Dinic)
```cpp
template<typename cap_t>
class Dinic{
public:
    explicit Dinic(int n): node_cnt(n), g(n){}
    int add_edge(int from, int to, cap_t cap){
        int m = int(pos.size());
        pos.emplace_back(from, int(g[from].size()));
        int from_id = int(g[from].size());
        int to_id = int(g[to].size());
        if(from == to) to_id++;
        g[from].push_back(PrivateEdge{to, to_id, cap});
        g[to].push_back(PrivateEdge{from, from_id, 0});
        return m;
    }
    struct Edge{
        int from, to;
        cap_t cap, flow;
    };
    Edge getEdge(int idx){
        auto _e = g[pos[idx].first][pos[idx].second];
        auto _re = g[_e.to][_e.rev];
        return Edge{pos[idx].first, _e.to, _e.cap + _re.cap, _re.cap};
    }
    std::vector<Edge> getEdges(){
        std::vector<Edge> result;
        for(int i = 0; i < pos.size(); ++i){
            result.push_back(getEdge(i));
        }
        return result;
    }
    cap_t flow(int st, int ed){
        return flow(st, ed, std::numeric_limits<cap_t>::max());
    }
    cap_t flow(int st, int ed, cap_t flow_limit){
        std::vector<int> level(node_cnt);
        std::queue<int> que;
        auto&& bfs = [&](){
            std::fill(level.begin(), level.end(), -1);
            level[st] = 0;
            while(!que.empty()){
                que.pop();
            }
            que.push(st);
            while(!que.empty()){
                int v = que.front();
                que.pop();
                for(PrivateEdge& e: g[v]){
                    if(e.cap == 0 or level[e.to] >= 0) continue;
                    level[e.to] = level[v] + 1;
                    if(e.to == ed) continue;
                    que.push(e.to);
                }
            }
        };
        auto&& dfs = [&](auto&& self, int v, cap_t up){
            if(v == st) return up;
            cap_t res = 0;
            int level_v = level[v];
            for(int idx = 0; idx < int(g[v].size()); ++idx){
                PrivateEdge& edge = g[v][idx];
                if(level_v <= level[edge.to] or g[edge.to][edge.rev].cap == 0) continue;
                cap_t delta = self(self, edge.to, std::min(up - res, g[edge.to][edge.rev].cap));
                if(delta <= 0) continue;
                g[v][idx].cap += delta;
                g[edge.to][edge.rev].cap -= delta;
                res += delta;
                if(res == up) return res;
            }
            level[v] = node_cnt;
            return res;
        };
        cap_t ans = 0;
        while (ans < flow_limit){
            bfs();
            if(level[ed] == -1) break;
            cap_t delta = dfs(dfs, ed, flow_limit - ans);
            if(!delta) break;
            ans += delta;
        }
        return ans;
    }
private:
    struct PrivateEdge{
        int to, rev;
        cap_t cap;
    };
    int node_cnt;
    std::vector<std::pair<int, int>> pos;
    std::vector<std::vector<PrivateEdge>> g;
};
```

#### 最小费用流(Dinic)
> Atcoder

```cpp
template <class Cap, class Cost> struct mcf_graph {
public:
    mcf_graph() {}
    explicit mcf_graph(int n) : _n(n) {}

    int add_edge(int from, int to, Cap cap, Cost cost) {
        assert(0 <= from && from < _n);
        assert(0 <= to && to < _n);
        assert(0 <= cap);
        assert(0 <= cost);
        int m = int(_edges.size());
        _edges.push_back({from, to, cap, 0, cost});
        return m;
    }

    struct edge {
        int from, to;
        Cap cap, flow;
        Cost cost;
    };

    template <class E> struct csr {
        std::vector<int> start;
        std::vector<E> elist;
        explicit csr(int n, const std::vector<std::pair<int, E>>& edges)
            : start(n + 1), elist(edges.size()) {
            for (auto e : edges) {
                start[e.first + 1]++;
            }
            for (int i = 1; i <= n; i++) {
                start[i] += start[i - 1];
            }
            auto counter = start;
            for (auto e : edges) {
                elist[counter[e.first]++] = e.second;
            }
        }
    };

    edge get_edge(int i) {
        int m = int(_edges.size());
        assert(0 <= i && i < m);
        return _edges[i];
    }
    std::vector<edge> edges() { return _edges; }

    std::pair<Cap, Cost> flow(int s, int t) {
        return flow(s, t, std::numeric_limits<Cap>::max());
    }
    std::pair<Cap, Cost> flow(int s, int t, Cap flow_limit) {
        return slope(s, t, flow_limit).back();
    }
    std::vector<std::pair<Cap, Cost>> slope(int s, int t) {
        return slope(s, t, std::numeric_limits<Cap>::max());
    }
    std::vector<std::pair<Cap, Cost>> slope(int s, int t, Cap flow_limit) {
        assert(0 <= s && s < _n);
        assert(0 <= t && t < _n);
        assert(s != t);

        int m = int(_edges.size());
        std::vector<int> edge_idx(m);

        auto g = [&]() {
            std::vector<int> degree(_n), redge_idx(m);
            std::vector<std::pair<int, _edge>> elist;
            elist.reserve(2 * m);
            for (int i = 0; i < m; i++) {
                auto e = _edges[i];
                edge_idx[i] = degree[e.from]++;
                redge_idx[i] = degree[e.to]++;
                elist.push_back({e.from, {e.to, -1, e.cap - e.flow, e.cost}});
                elist.push_back({e.to, {e.from, -1, e.flow, -e.cost}});
            }
            auto _g = csr<_edge>(_n, elist);
            for (int i = 0; i < m; i++) {
                auto e = _edges[i];
                edge_idx[i] += _g.start[e.from];
                redge_idx[i] += _g.start[e.to];
                _g.elist[edge_idx[i]].rev = redge_idx[i];
                _g.elist[redge_idx[i]].rev = edge_idx[i];
            }
            return _g;
        }();

        auto result = slope(g, s, t, flow_limit);

        for (int i = 0; i < m; i++) {
            auto e = g.elist[edge_idx[i]];
            _edges[i].flow = _edges[i].cap - e.cap;
        }

        return result;
    }

private:
    int _n;
    std::vector<edge> _edges;

    // inside edge
    struct _edge {
        int to, rev;
        Cap cap;
        Cost cost;
    };

    std::vector<std::pair<Cap, Cost>> slope(csr<_edge>& g,
        int s,
        int t,
        Cap flow_limit) {
        // variants (C = maxcost):
        // -(n-1)C <= dual[s] <= dual[i] <= dual[t] = 0
        // reduced cost (= e.cost + dual[e.from] - dual[e.to]) >= 0 for all edge

        // dual_dist[i] = (dual[i], dist[i])
        std::vector<std::pair<Cost, Cost>> dual_dist(_n);
        std::vector<int> prev_e(_n);
        std::vector<bool> vis(_n);
        struct Q {
            Cost key;
            int to;
            bool operator<(Q r) const { return key > r.key; }
        };
        std::vector<int> que_min;
        std::vector<Q> que;
        auto dual_ref = [&]() {
            for (int i = 0; i < _n; i++) {
                dual_dist[i].second = std::numeric_limits<Cost>::max();
            }
            std::fill(vis.begin(), vis.end(), false);
            que_min.clear();
            que.clear();

            // que[0..heap_r) was heapified
            size_t heap_r = 0;

            dual_dist[s].second = 0;
            que_min.push_back(s);
            while (!que_min.empty() || !que.empty()) {
                int v;
                if (!que_min.empty()) {
                    v = que_min.back();
                    que_min.pop_back();
                } else {
                    while (heap_r < que.size()) {
                        heap_r++;
                        std::push_heap(que.begin(), que.begin() + heap_r);
                    }
                    v = que.front().to;
                    std::pop_heap(que.begin(), que.end());
                    que.pop_back();
                    heap_r--;
                }
                if (vis[v]) continue;
                vis[v] = true;
                if (v == t) break;
                // dist[v] = shortest(s, v) + dual[s] - dual[v]
                // dist[v] >= 0 (all reduced cost are positive)
                // dist[v] <= (n-1)C
                Cost dual_v = dual_dist[v].first, dist_v = dual_dist[v].second;
                for (int i = g.start[v]; i < g.start[v + 1]; i++) {
                    auto e = g.elist[i];
                    if (!e.cap) continue;
                    // |-dual[e.to] + dual[v]| <= (n-1)C
                    // cost <= C - -(n-1)C + 0 = nC
                    Cost cost = e.cost - dual_dist[e.to].first + dual_v;
                    if (dual_dist[e.to].second - dist_v > cost) {
                        Cost dist_to = dist_v + cost;
                        dual_dist[e.to].second = dist_to;
                        prev_e[e.to] = e.rev;
                        if (dist_to == dist_v) {
                            que_min.push_back(e.to);
                        } else {
                            que.push_back(Q{dist_to, e.to});
                        }
                    }
                }
            }
            if (!vis[t]) {
                return false;
            }

            for (int v = 0; v < _n; v++) {
                if (!vis[v]) continue;
                // dual[v] = dual[v] - dist[t] + dist[v]
                //         = dual[v] - (shortest(s, t) + dual[s] - dual[t]) +
                //         (shortest(s, v) + dual[s] - dual[v]) = - shortest(s,
                //         t) + dual[t] + shortest(s, v) = shortest(s, v) -
                //         shortest(s, t) >= 0 - (n-1)C
                dual_dist[v].first -= dual_dist[t].second - dual_dist[v].second;
            }
            return true;
        };
        Cap flow = 0;
        Cost cost = 0, prev_cost_per_flow = -1;
        std::vector<std::pair<Cap, Cost>> result = {{Cap(0), Cost(0)}};
        while (flow < flow_limit) {
            if (!dual_ref()) break;
            Cap c = flow_limit - flow;
            for (int v = t; v != s; v = g.elist[prev_e[v]].to) {
                c = std::min(c, g.elist[g.elist[prev_e[v]].rev].cap);
            }
            for (int v = t; v != s; v = g.elist[prev_e[v]].to) {
                auto& e = g.elist[prev_e[v]];
                e.cap += c;
                g.elist[e.rev].cap -= c;
            }
            Cost d = -dual_dist[s].first;
            flow += c;
            cost += c * d;
            if (prev_cost_per_flow == d) {
                result.pop_back();
            }
            result.push_back({flow, cost});
            prev_cost_per_flow = d;
        }
        return result;
    }
};
```
### Tarjan
> 解决关键边和关键点很好用

```cpp
const int maxn = 100100;
int dfn[maxn], low[maxn];
int tim;
int vis[maxn];
int sd[maxn];
std::stack<int> st;
vector<vector<int>> g;
void tarjan(int cur){
    dfn[cur] = low[cur] = ++tim; 
    vis[cur] = 1;
    st.push(cur);
    for(auto& nex: g[cur]){
        if(!dfn[nex]){
            tarjan(nex);
            low[cur] = min(low[cur], low[nex]);
        }else if(vis[nex]){
            low[cur] = min(low[cur], dfn[nex]);
        }
    }
    if(dfn[cur] == low[cur]){
        while(!st.empty()){
            auto pos = st.top();
            st.pop();
            vis[pos] = 0;
            sd[pos] = cur;
            if(pos == cur) break;
        }
    }
}

```
## 数学

### 模数(int)
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

### 素数筛
#### 单个正整数判断是不是质数
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
#### 埃拉托斯特尼筛法
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
#### 线性筛（欧式筛）
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

#### 奇数筛
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

### 类欧几里得算法
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

### 拓展欧几里得

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
### 欧拉函数
#### 单个欧拉函数
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

#### 批量求欧拉函数（线性筛）
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

#### 筛法求约数个数（线性筛）
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

### 中国剩余定理 & 扩展中国剩余定理
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

### 乘法逆元
#### 扩展欧几里得算法
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
#### 快速幂算法

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

#### 批量乘法逆元
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

### 阶乘逆元（求组合数）

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
### 卢卡斯定理
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

### BSGS
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

### exBSGS
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

### Cayley 公式（Caylay's formula）

完全图 $K_n$ 有 $n^{n - 2}$ 棵生成树。


### 莫比乌斯函数（线性筛）
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

### 杜教筛
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

### 康拓展开
#### 正向

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

#### 反向
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

### Miller Rabin & Pollard Rho
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
### 线性代数
#### 矩阵
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

#### 高斯消元
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


#### 线性基
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

### 自适应辛普森

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

### 多项式
#### 快速傅立叶变换
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
## 计算几何

### 极角排序

```cpp

struct Point{
    ll x, y;
    Point() = default;
    Point(int argx, int argy): x(argx), y(argy){}
    bool up() const{
        return y > 0 or (y == 0 and x >= 0);
    }
};
ll det(const Point& a, const Point& b) {
    return a.x * b.y - b.x * a.y;
}
 
ll dot(const Point& a, const Point& b) {
    return a.x * b.x + a.y * b.y;
}
 
bool cmp(const Point& a, const Point& b) {
    if (a.up() ^ b.up()) return a.up() > b.up();
    return det(a, b) > 0;
}
 
bool same(const Point& a, const Point& b) {
    ll d = det (a, b);
    if (d > 0) return true;
    if (d < 0) return false;
    return dot (a, b) > 0;
}

```

### 凸包

```cpp
// 基本数据类型，面积和边长的数据
template<typename T, typename AFT>
class Andrew{
    typedef pair<T, T> PTT;
    PTT reduce(PTT a, PTT b){
        return PTT{a.first - b.first, a.second - b.second};
    }
    T cross(PTT a, PTT b){
        return a.first * b.second - a.second * b.first;
    }
    T area(PTT a, PTT b, PTT c){
        return cross(reduce(b , a), reduce(c , a));
    }
    AFT dist(PTT a, PTT b){
        AFT dx = a.first - b.first;
        AFT dy = a.second - b.second;
        return sqrt(dx * dx + dy * dy);
    }
public:
    Andrew()= default;
    Andrew(const vector<PTT>& argv): vec(argv){}
    void addPoint(PTT p){
        vec.push_back(p);
    }
    // 边长， 面积， 按节点顺序的边缘节点序列（第一个点和最后一个点是一样的）
    // 注意：如果考虑凸包上点的数目最少，需要将while循环允许面积等于0
    tuple<T, T, vector<PTT>> run(){
        sort(vec.begin(), vec.end());
        vector<int> st;
        // vis是用来记录第一遍访问的节点，而不是最终在凸包上面的点
        vector<bool> vis(vec.size(), false);
        for(int i = 0; i < vec.size(); ++i){
            while(st.size() >= 2 and area(vec[*next(st.rbegin(), 1)], vec[*st.rbegin()], vec[i]) < 0){
                if(area(vec[*next(st.rbegin(), 1)], vec[*st.rbegin()], vec[i]) < 0){
                    vis[st.back()] = false;
                }
                st.pop_back();
            }
            st.push_back(i);
            vis[st.back()] = true;
        }
        vis[0] = false;
        for(int i = (int)vec.size() - 1; i >= 0; --i){
            if(vis[i]) continue;
            while(st.size() >= 2 and area(vec[*next(st.rbegin(), 1)], vec[*st.rbegin()], vec[i]) < 0){
                st.pop_back();
            }
            st.push_back(i);
        }
        AFT dis = 0;
        AFT ars = 0;
        vector<PTT> res;
        for(auto& it: st) res.push_back(vec[it]);
        for(int i = 1; i < st.size(); ++i){
            dis += dist(vec[st[i - 1]], vec[st[i]]);
            ars += area(vec[0], vec[st[i - 1]], vec[st[i]]);
        }
        return {dis, ars, res};
    }
private:
    vector<PTT> vec;
};

```

### 方阵的三维操作模板
> 翻转，旋转和转置
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
```

## 数据结构

### 线段树

```cpp
// Luogu P3373
template<typename T = int>
inline T read() {
    T ret;
    cin >> ret;
    return ret;
}

template<class Fun>
class Y_combinator {
private:
    Fun fun_;
public:
    template<class F>
    Y_combinator(F&& fun) : fun_(static_cast<F&&>(fun)) {}
    template<class... Args>
    decltype(auto) operator () (Args&&...args) const {
        return fun_(*this, static_cast<Args&&>(args)...);
    }
};
template<class T> Y_combinator(T)->Y_combinator<T>;

#define MID ((l + r) >> 1)
#define LEFT (cur << 1)
#define RIGHT ((cur << 1) | 1)

int main(int argc, char* argv[]) {
    fastIO();
    int n, m;
    cin >> n >> m;
    vector<ll> arr{0};
    for (int i = 0; i < n; ++i) {
        arr.push_back(read<ll>());
    }
    vector<ll> lazy((n << 2) + 10);
    vector<ll> node((n << 2) + 10);
    Y_combinator(
        [&](auto&& build, int cur, int l, int r) -> void {
            if (l == r) {
                node[cur] = arr[l];
            } else {
                build(LEFT, l, MID);
                build(RIGHT, MID + 1, r);
                node[cur] = node[LEFT] + node[RIGHT];
            }
        }
    )(1, 1, n);
    auto&& lazyUpdate = [&](int cur, int l, int r) -> void {
        if (lazy[cur] != 0) {
            node[LEFT] += lazy[cur] * (MID - l + 1);
            node[RIGHT] += lazy[cur] * (r - MID);
            lazy[LEFT] += lazy[cur];
            lazy[RIGHT] += lazy[cur];
            lazy[cur] = 0;
        }
    };
    auto&& update = Y_combinator(
        [&](auto&& update, int cur, int l, int r, int s, int e, ll v) {
            if (s > r or e < l) return;
            if (s <= l and r <= e) {
                node[cur] += (r - l + 1) * v;
                lazy[cur] += v;
            } else {
                lazyUpdate(cur, l, r);
                update(LEFT, l, MID, s, e, v);
                update(RIGHT, MID + 1, r, s, e, v);
                node[cur] = node[LEFT] + node[RIGHT];
            }
        }
    );
    auto&& query = Y_combinator(
        [&](auto&& query, int cur, int l, int r, int s, int e)->ll {
            if (s > r or e < l) return 0;
            if (s <= l and e >= r) {
                return node[cur];
            }
            lazyUpdate(cur, l, r);
            ll ret = query(LEFT, l, MID, s, e);
            ret += query(RIGHT, MID + 1, r, s, e);
            return ret;
        }
    );
    while (m--) {
        int q, x, y, k;
        cin >> q >> x >> y;
        if (q == 1) {
            cin >> k;
            update(1, 1, n, x, y, k);
        } else {
            cout << query(1, 1, n, x, y) << endl;
        }
    }
    return 0;
}
```

### ST表（稀疏表）(C++17)

```cpp
template<typename iter, typename BinOp>
class SparseTable {
    using T = typename remove_reference<decltype(*declval<iter>())>::type;
    vector<vector<T>> arr;
    BinOp binOp;
public:
    SparseTable(iter begin, iter end, BinOp binOp) : arr(1), binOp(binOp) {
        int n = distance(begin, end);
        arr.assign(32 - __builtin_clz(n), vector<T>(n));
        arr[0].assign(begin, end);
        for (int i = 1; i < arr.size(); ++i) {
            for (int j = 0; j < n - (1 << i) + 1; ++j) {
                arr[i][j] = binOp(arr[i - 1][j], arr[i - 1][j + (1 << (i - 1))]);
            }
        }
    }
    T query(int lPos, int rPos) {
        int h = floor(log2(rPos - lPos + 1));
        return binOp(arr[h][lPos], arr[h][rPos - (1 << h) + 1]);
    }
};
```

### 树状数组

```cpp
template<typename T>
struct FenWick {
    int N;
    vector<T> arr;
    FenWick(int sz): N(sz), arr(sz + 1, 0) {}
    void update(int pos, T val) {
        for (; pos <= N;pos |= (pos + 1)) {
            arr[pos] += val;
        }
    }
    // 获取 [1, pos] 的和
    T get(int pos) {
        T ret = 0;
        for (; pos > 0; --pos) {
            ret += arr[pos];
            pos &= (pos + 1);
        }
        return ret;
    }
    // 获取 [l, r] 的和
    T query(int l, int r) {
        return get(r) - get(l - 1);
    }
};
```
### 珂朵莉树
```cpp
namespace Chtholly{
struct Node{
    int l, r;
    mutable int v;
    Node(int il, int ir, int iv): l(il), r(ir), v(iv){}
    bool operator < (const Node& arg) const{
        return l < arg.l;
    }
};
class Tree{
protected:
    auto split(int pos){
        if(pos > _sz) return odt.end();
        auto it = --odt.upper_bound(Node{pos, 0, 0});
        if(it->l == pos) return it;
        auto tmp = *it;
        odt.erase(it);
        odt.insert({tmp.l, pos - 1, tmp.v});
        return odt.insert({pos, tmp.r, tmp.v}).first;
    }  
public:
    Tree(int sz, int ini = 1): _sz(sz), odt({Node{1, sz, ini}}) {}
    virtual void assign(int l, int r, int v){
        auto itr = split(r + 1), itl = split(l);
        // operations here
        odt.erase(itl, itr);
        odt.insert({l, r, v});
    }
protected:
    int _sz;
    set<Node> odt;
};
}

```

### Splay树
> https://loj.ac/p/104
> 有误，暂未修

```cpp
#include <vector>
#include <array>
#include <iostream>
#include <cassert>
using namespace std;
template<typename T>
class SplayTree{
public:
    struct Node{
        Node *parent{};
        std::array<Node*, 2> child{};
        T val;
        // cnt: repeat of current element, sz: element count of child tree, sum: repeats of child tree
        size_t cnt, sz, sum;
        explicit Node(T value_arg): val(value_arg), cnt(1), sz(1), sum(1){}
        bool side() const{
            return parent->child[1] == this;
        }
        // maintain information of current element
        void maintain(){
            if(!this) return;
            this->sum = this->cnt;
            this->sz = 1;
            if(this->child[0]) {
                this->sum += this->child[0]->sum;
                this->sz += this->child[0]->sz;
            }
            if(this->child[1]) {
                this->sum += this->child[1]->sum;
                this->sz += this->child[1]->sz;
            }
        }
        // left rotate and right rotate
        void rotate(){
            const auto p = parent;
            const bool i = side();
            if(p->parent){
                p->parent->attach(p->side(), this);
            }else{
                parent = nullptr;
            }
            p->attach(i, child[!i]);
            attach(!i, p);
            p->maintain();
            maintain();
        }
        void splay(){
            for(;parent;rotate()){
                if(parent->parent){
                    (side() == parent->side() ? parent: this)->rotate();
                }
            }
        }
        // attach node new_ as the node's side child
        void attach(bool side, Node* const new_){
            if(new_) new_->parent = this;
            child[side] = new_;
        }
    };
    struct iterator{
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = T;
        using pointer = T*;
        using reference = T&;
        using difference_type = long long;
    public:
        Node* node;
        void operator--(){ advance<false>();}
        void operator++(){ advance<true>();}
        const T& operator*(){return node->val;}
        explicit iterator(Node* node_arg): node(node_arg){}
        bool operator==(const iterator oth) const{
            return node == oth.node;
        }
        bool operator != (const iterator oth) const{
            return *this != oth;
        }
    private:
        template<bool dir> void advance(){
            if(node->child[dir]){
                node = extremum<!dir>(node->child[dir]);
                return;
            }
            for(;node->parent and node->side() == dir; node = node->parent);
            node = node->parent;
        }
    };

    template<bool i> static Node* extremum(Node* x){
        assert(x);
        for(;x->child[i]; x = x->child[i]);
        return x;
    }
    Node* rt{};
    explicit SplayTree()= default;
    ~SplayTree(){ destroy(rt);}
    void insert(const T& arg){
        if(!rt){
            rt = new Node(arg);
            rt->maintain();
            return;
        }
        Node* cur = rt, *f = nullptr;
        while(true){
            if(cur->val == arg){
                cur->cnt++;
                cur->maintain();
                f->maintain();
                cur->splay();
                rt = cur;
                break;
            }
            f = cur;
            cur = cur->child[cur->val < arg];
            if(!cur){
                Node* tmp = new Node(arg);
                f->child[f->val < arg] = tmp;
                tmp->parent = f;
                tmp->maintain();
                f->maintain();
                tmp->splay();
                rt = tmp;
                break;
            }
        }
    }

    // size, sum
    std::pair<size_t, size_t> rank(const T& arg){
        std::pair<size_t, size_t> res{0, 0};
        Node* cur = rt;
        while(cur){
            if(arg < cur->val){
                cur = cur->child[0];
            }else{
                if(cur->child[0]) {
                    res.first += cur->child[0]->sz;
                    res.second += cur->child[0]->sum;
                }
                res.first ++;
                res.second += cur->cnt;
                if(arg == cur->val){
                    cur->splay();
                    rt = cur;
                    break;
                }
                cur = cur->child[1];
            }
        }
        return res;
    }
    template<bool unique = false>
    iterator kth(size_t k){
        assert(k <= (rt != nullptr ? (unique ? rt->sz : rt->sum) : 0));
        Node* cur = rt;
        while(true){
            if(cur->child[0] and k <= (unique ? cur->child[0]->sz : cur->child[0]->sum)){
                cur = cur->child[0];
            }else{
                if(cur->child[0]) k -= (unique ? cur->child[0]->sz : cur->child[0]->sum);
                if(k <= cur->cnt){
                    cur->splay();
                    rt = cur;
                    return iterator{cur};
                }
                k -= (unique ? 1 : cur->cnt);
                cur = cur->child[1];
            }
        }
    }
    static void destroy(Node* const node){
        if(!node) return;
        for(Node* const child: node->child){
            destroy(child);
        }
        delete node;
    }
    bool empty() const{
        return rt == nullptr;
    }
    size_t sum() const{
        return (rt == nullptr ? 0 : rt->sum);
    }
    size_t size() const{
        return (rt == nullptr ? 0 : rt->sz);
    }

    template<bool side = false>
    iterator begin(){
        return iterator{extremum<side>(rt)};
    }
    iterator rend(){
        return iterator{nullptr};
    }
    iterator end(){
        return iterator{nullptr};
    }
    iterator find(const T& key){
        Node* cur = rt;
        while(cur and key != cur->val){
            const auto nex = cur->child[key > cur->val];
            if(!nex) {
                cur->splay();
                rt = cur;
            }
            cur = nex;
        }
        return iterator{cur};
    }
    iterator lower_bound(const T& key){
        Node* cur = rt;
        Node* ret = nullptr;
        while(cur){
            if(cur->val > key){
                ret = cur;
                cur = cur->child[0];
            }else if(cur->val == key){
                ret = cur;
                break;
            }else{
                cur = cur->child[1];
            }
        }
        if(ret){
            ret->splay();
            rt = ret;
        }
        return iterator{ret};
    }
    Node* join(Node* const arg1, Node* const arg2){
        if(!arg1){
            arg2->parent = nullptr;
            return arg2;
        }
        arg1->parent = nullptr;
        Node* const mx = extremum<true>(arg1);
        mx->splay();
        rt = mx;
        assert(mx->child[1] == nullptr);
        mx->child[1] = arg2;
        mx->parent = nullptr;
        if(arg2) arg2->parent = mx;
        mx->maintain();
        return mx;
    }
    void erase(const iterator itr){
        if(!itr.node) return;
        Node* x = itr.node;
        x->splay();
        rt = x;
        rt = join(x->child[0], x->child[1]);
    }
    void extract(const iterator itr){
        if(!itr.node) return;
        if(itr.node->cnt == 1) erase(itr);
        else{
            itr.node->cnt--;
            itr.node->splay();
            rt = itr.node;
        }
    }
};
typedef pair<int, int> PII;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    SplayTree<int> st;
    int n;
    cin >> n;
    while(n--){
        int op;
        cin >> op;
        if(op == 1){
            int tv;
            cin >> tv;
            st.insert(tv);
        }else if(op == 2){
            int tv;
            cin >> tv;
            st.extract(st.find(tv));
        }else if(op == 3){
            int tv;
            cin >> tv;
            auto itr = st.find(tv);
            auto res = st.rank(tv);
            cout << res.second - (itr.node->cnt) + 1 << endl;
        }else if(op == 4){
            int tv;
            cin >> tv;
            auto itr = st.kth(tv);
            cout << itr.node->val << endl;
        }else if(op == 5){
            int tv;
            cin >> tv;
            auto itr = st.lower_bound(tv);
            if(itr == st.end()) itr = st.begin<true>();
            else --itr;
            cout << itr.node->val << endl;
        }else{
            int tv;
            cin >> tv;
            auto itr = st.lower_bound(tv);
            if(itr.node->val == tv) ++itr;
            cout << itr.node->val << endl;
        }
    }
    return 0;
}
```
### AVL树
```cpp
/**
 * @brief AVL 树
 * @author dianhsu
 * @date 2021/05/25
 * @ref https://zh.wikipedia.org/wiki/AVL树
 * */
#include <bits/stdc++.h>

template<class T>
struct AVLNode {
    T data;
    AVLNode<T> *leftChild;
    AVLNode<T> *rightChild;
    int height;

    AVLNode(T data): data(data), height(1), leftChild(nullptr), rightChild(nullptr) { }

    ~AVLNode() {
        delete leftChild;
        delete rightChild;
    }
};

template<class T>
class AVL {
public:
    AVL() {
        root = nullptr;
    }

    ~AVL() {
        delete root;
    }

    /**
     * @brief 将结点插入到AVL树中
     * @param val 需要插入的值
     * @note 如果发现这个树中已经有这个值存在了，就不会进行任何操作
     * */
    void insert(T val) {
        _insert(&root, val);
    }

    /**
     * @brief 检查结点是否在AVL树中
     * @param val 需要检查的值
     * */
    bool exist(T val) {
        auto ptr = &root;
        while (*ptr != nullptr) {
            if (val == (*ptr)->data) {
                return true;
            } else if (val < (*ptr)->data) {
                *ptr = (*ptr)->leftChild;
            } else {
                *ptr = (*ptr)->rightChild;
            }
        }
        return false;
    }

    /**
     * @brief 找到值为val的结点
     * @param val 目标值
     * @return 返回值为指向该结点的指针的地址
     */
    AVLNode<T> **find(T val) {
        auto ptr = &root;
        while ((*ptr) != nullptr) {
            if (val == (*ptr)->data) {
                break;
            } else if (val < (*ptr)->data) {
                *ptr = (*ptr)->leftChild;
            } else {
                *ptr = (*ptr)->rightChild;
            }
        }
        return ptr;
    }

    /**
     * @brief 删除结点
     * @note 首先找到结点，然后将结点旋转到叶子结点，然后回溯检查树的平衡性
     * @param val 需要删除的结点的值
     * @note 这个地方需要递归寻找该值的结点，因为需要回溯更新平衡树
     * */
    void remove(T val) {
        _remove(&root, val);
    }


private:
    void _remove(AVLNode<T> **ptr, T val) {
        if (*ptr == nullptr) {
            return;
        }
        if ((*ptr)->data == val) {
            _rotateNodeToLeaf(ptr);
        } else if ((*ptr)->data < val) {
            _remove(&((*ptr)->rightChild), val);
        } else {
            _remove(&((*ptr)->leftChild), val);
        }
        // 完了之后回溯，重新平衡二叉树
        _balance(ptr);
        _updateHeight(*ptr);
    }

    /**
     * @brief 将一个结点旋转到叶子结点
     * @param ptr 将要被旋转至叶子的结点的指针的地址
     * @note 旋转的时候，将当前结点旋转到高度比较小的一边。
     */
    void _rotateNodeToLeaf(AVLNode<T> **ptr) {
        // 当前结点已经是叶子结点了
        if ((*ptr)->leftChild == nullptr and (*ptr)->rightChild == nullptr) {
            *ptr = nullptr;
            return;
        }
        int leftHeight = (*ptr)->leftChild != nullptr ? (*ptr)->leftChild->height : 0;
        int rightHeight = (*ptr)->rightChild != nullptr ? (*ptr)->rightChild->height : 0;
        // 左边高度比较小，左旋
        if (leftHeight <= rightHeight) {
            _leftRotate(ptr);
            _rotateNodeToLeaf(&((*ptr)->leftChild));
        } else {
            // 右旋
            _rightRotate(ptr);
            _rotateNodeToLeaf(&((*ptr)->rightChild));
        }
        _balance(ptr);
        _updateHeight(*ptr);
    }

    /**
     * @brief 插入结点
     *
     * */
    void _insert(AVLNode<T> **ptr, T val) {
        if (*ptr == nullptr) {
            *ptr = new AVLNode<T>(val);
            return;
        }
        if (val < (*ptr)->data) {
            _insert(&((*ptr)->leftChild), val);
        } else if (val > (*ptr)->data) {
            _insert(&((*ptr)->rightChild), val);
        } else {
            // 如果当前平衡二叉树中已经存在这个结点了，不做任何处理
            return;
        }
        _balance(ptr);
        _updateHeight(*ptr);
    }

    /**
     * @brief 平衡结点
     *
     * */
    void _balance(AVLNode<T> **ptr) {
        if (*ptr == nullptr) return;
        int leftHeight = (*ptr)->leftChild != nullptr ? (*ptr)->leftChild->height : 0;
        int rightHeight = (*ptr)->rightChild != nullptr ? (*ptr)->rightChild->height : 0;
        if (abs(leftHeight - rightHeight) <= 1) return;

        if (leftHeight < rightHeight) {
            auto rightElement = (*ptr)->rightChild;
            int rightElementLeftHeight = rightElement->leftChild != nullptr ? rightElement->leftChild->height : 0;
            int rightElementRightHeight = rightElement->rightChild != nullptr ? rightElement->rightChild->height : 0;
            if (rightElementLeftHeight < rightElementRightHeight) {
                // RR
                _leftRotate(ptr);
            } else {
                // RL
                _rightRotate(&((*ptr)->rightChild));
                _leftRotate(ptr);
            }
        } else {
            auto leftElement = (*ptr)->leftChild;
            int leftElementLeftHeight = leftElement->leftChild != nullptr ? leftElement->leftChild->height : 0;
            int leftElementRightHeight = leftElement->rightChild != nullptr ? leftElement->rightChild->height : 0;
            if (leftElementLeftHeight > leftElementRightHeight) {
                // LL
                _rightRotate(ptr);
            } else {
                // LR
                _leftRotate(&((*ptr)->leftChild));
                _rightRotate(ptr);
            }
        }
    }

    /**
     * @brief 右旋
     *
     * */
    void _rightRotate(AVLNode<T> **ptr) {
        auto tmp = (*ptr)->leftChild;
        (*ptr)->leftChild = tmp->rightChild;
        tmp->rightChild = *ptr;
        _updateHeight(tmp);
        _updateHeight(*ptr);
        *ptr = tmp;
    }

    /**
     * @brief 左旋
     * */
    void _leftRotate(AVLNode<T> **ptr) {
        auto tmp = (*ptr)->rightChild;
        (*ptr)->rightChild = tmp->leftChild;
        tmp->leftChild = *ptr;
        _updateHeight(tmp);
        _updateHeight(*ptr);
        *ptr = tmp;
    }

    void _updateHeight(AVLNode<T> *ptr) {
        if (ptr == nullptr) return;
        int leftHeight = ptr->leftChild != nullptr ? ptr->leftChild->height : 0;
        int rightHeight = ptr->rightChild != nullptr ? ptr->rightChild->height : 0;
        ptr->height = std::max(leftHeight, rightHeight) + 1;
    }

    AVLNode<T> *root;
};

int main() {
    auto avl = new AVL<int>();
    int n = 20;
    std::random_device rd{};
    std::mt19937 gen{rd()};
    std::normal_distribution<> d{100, 100};
    std::uniform_int_distribution<int> u(0, INT_MAX >> 1);
    std::vector<int> vec;
    for (int i = 0; i < n; ++i) {
        vec.push_back((int) std::round(d(gen)));
        //vec.push_back(i);
    }
    for (auto it : vec) {
        avl->insert(it);
    }
    avl->remove(15);
    avl->remove(32);
    avl->remove(31);
    std::cout << *avl << std::endl;
    delete avl;
    return 0;
}
```

## Tricks
### Fast I/O
```cpp
template<typename T = int>
inline T fRead() {
    T x = 0, w = 1; char c = getchar();
    while (c < '0' || c>'9') { if (c == '-') w = -1; c = getchar(); }
    while (c <= '9' && c >= '0') { x = (x << 1) + (x << 3) + c - '0'; c = getchar(); }
    return w == 1 ? x : -x;
}
template<typename T = int>
inline T cRead() {
    T ret;
    cin >> ret;
    return ret;
}
template<typename T = int>
inline void fWrite(T x){
    if(x < 0){
        x = -x;
        putchar('-');
    }
    if(x >= 10) fWrite(x / 10);
    putchar(x % 10 + '0');
}
template<typename T = int>
inline void cWrite(T x){
    cout << x;
}
```
### Y combinator (C++17)

```cpp
template<class Fun>
class Y_combinator {
private:
    Fun fun_;
public:
    template<class F>
    Y_combinator(F&& fun) : fun_(static_cast<F&&>(fun)) {}
    template<class... Args>
    decltype(auto) operator () (Args&&...args) const {
        return fun_(*this, static_cast<Args&&>(args)...);
    }
};
template<class T> Y_combinator(T)->Y_combinator<T>;
```
### Numeric Binary Search
```cpp
int lower_bound(int target, vector<int>& vec){
    int pos = -1;
    for(int i = (32 - __builtin_clz(vec.size())); i; i >>= 1){
        if(pos + i < vec.size() and vec[pos + i] < target){
            pos += i;
        }
    }
    return pos + 1;
}
```
### Least Power of 2 and Greater Power of 2
```cpp
int leastPowerOfTwo(int val){
    return 32 - __builtin_clz(val - 1);
}
int greaterPowerOfTwo(int val){
    return 32 - __builtin_clz(val);
}
```