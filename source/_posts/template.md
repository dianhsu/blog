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
    explicit DSU(int size_): sz(size_), fa(size_, 0), cnt(size_, 1) {
        iota(fa.begin(), fa.end(), 0);
    }
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