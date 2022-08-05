---
title: 八股文收集
math: true
date: 2022-07-23 09:41:22
categories:
    - 面试
tags:
    - C++
    - 操作系统
    - 计算机网络
    - Redis
    - 数据库原理
    - 软件设计模式
    - 计算机组成原理
    - 编译原理
index_img: https://cdn.dianhsu.com/img/2022-07-23-11-46-55.jpeg
---

# C++
## 智能指针

## 虚函数
### 虚函数，纯虚函数和虚析构函数 [^1]

- C++中的虚函数的作用主要是实现了多态的机制。关于多态，简而言之就是用父类型的指针指向其子类的实例，然后通过父类的指针调用实际子类的成员函数。这种技术可以让父类的指针有“多种形态”，这是一种泛型技术。如果调用非虚函数，则无论实际对象是什么类型，都执行基类类型所定义的函数。非虚函数总是在编译时根据调用该函数的对象，引用或指针的类型而确定。如果调用虚函数，则直到运行时才能确定调用哪个函数，运行的虚函数是引用所绑定或指针所指向的对象所属类型定义的版本。虚函数必须是基类的非静态成员函数。虚函数的作用是实现动态联编，也就是在程序的运行阶段动态地选择合适的成员函数，在定义了虚函数后，可以在基类的派生类中对虚函数重新定义，在派生类中重新定义的函数应与虚函数具有相同的形参个数和形参类型。以实现统一的接口，不同定义过程。如果在派生类中没有对虚函数重新定义，则它继承其基类的虚函数。
    ```cpp
    class Person{
        public:
            //虚函数
            virtual void GetName(){
                cout<<"PersonName:xiaosi"<<endl;
            };
    };
    class Student:public Person{
        public:
            void GetName(){
                cout<<"StudentName:xiaosi"<<endl;
            };
    };
    int main(){
        //指针
        Person *person = new Student();
        //基类调用子类的函数
        person->GetName();//StudentName:xiaosi
    }
    ```
  虚函数（Virtual Function）是通过一张虚函数表（Virtual Table）来实现的。简称为V-Table。在这个表中，主是要一个类的虚函数的地址表，这张表解决了继承、覆盖的问题，保证其容真实反应实际的函数。这样，在有虚函数的类的实例中这个表被分配在了这个实例的内存中，所以，当我们用父类的指针来操作一个子类的时候，这张虚函数表就显得由为重要了，它就像一个地图一样，指明了实际所应该调用的函数。

- 纯虚函数是在基类中声明的虚函数，它在基类中没有定义，但要求任何派生类都要定义自己的实现方法。在基类中实现纯虚函数的方法是在函数原型后加`=0`（`virtual void GetName() = 0`）。在很多情况下，基类本身生成对象是不合情理的。例如，动物作为一个基类可以派生出老虎、孔雀等子类，但动物本身生成对象明显不合常理。为了解决上述问题，将函数定义为纯虚函数，则编译器要求在派生类中必须予以重写以实现多态性。同时含有纯虚拟函数的类称为抽象类，它不能生成对象。这样就很好地解决了上述两个问题。将函数定义为纯虚函数能够说明，该函数为后代类型提供了可以覆盖的接口，但是这个类中的函数绝不会调用。声明了纯虚函数的类是一个抽象类。所以，用户不能创建类的实例，只能创建它的派生类的实例。必须在继承类中重新声明函数（不要后面的＝0）否则该派生类也不能实例化，而且它们在抽象类中往往没有定义。定义纯虚函数的目的在于，使派生类仅仅只是继承函数的接口。纯虚函数的意义，让所有的类对象（主要是派生类对象）都可以执行纯虚函数的动作，但类无法为纯虚函数提供一个合理的缺省实现。所以类纯虚函数的声明就是在告诉子类的设计者，“你必须提供一个纯虚函数的实现，但我不知道你会怎样实现它”。
    ```cpp
    //抽象类
    class Person{
        public:
            //纯虚函数
            virtual void GetName()=0;
    };
    class Student:public Person{
        public:
            Student(){
            };
            void GetName(){
                cout<<"StudentName:xiaosi"<<endl;
            };
    };
    int main(){
        Student student;
    }
    ```

### 引入虚函数带来的问题[^4]
虚函数影响效率有两点原因，第一，Cache命中率不够好，一般函数可能编译后的指令就在当前函数地址附近，这样很可能在调用前目标函数代码已经被载入指令cache. 但是虚拟函数不在cache中的概率高。而且一调函数就可能在cache中载入虚函数表，如果这个虚函数又调用其它的虚函数，那么可能又得载入到cache中导致cache被占用，指令和数据的cache命中率下降。 第二点编译器不好优化。因为编译器只知道你要调用的是一个不确定的地址处的函数，没法知道更多细节，也就没法替你做更多优化。

## C++协程

## C++14/17/20新特性
### C++14新特性 [^2]
#### 函数返回值类型推导
C++14 对函数返回类型推导规则做了优化，先看一段代码：
```cpp
#include <iostream>

using namespace std;

auto func(int i){
    return i;
}

int main(){
    cout << func(4) << endl;
    return 0;
}
```

使用C++11编译：
```bash
~/test$ g++ test.cc -std=c++11
test.cc:5:16: error: ‘func’ function uses ‘auto’ type specifier without trailing return type
 auto func(int i) {
                ^
test.cc:5:16: note: deduced return type only available with -std=c++14 or -std=gnu++14
```
上面的代码使用 C\+\+11 是不能通过编译的，通过编译器输出的信息也可以看见这个特性需要到 C\+\+14 才被支持。

返回值类型推导也可以用在模板中：
```cpp
#include <iostream>
using namespace std;

template<typename T>
auto func(T t){ return t; }

int main(){
    cout << func(4) << endl;
    cout << func(3.4) << endl;
    return 0;
}
```
**注意**
1. 函数内如果有多个return语句，它们必须返回相同类型，否则编译失败。
    ```cpp
    auto func(bool flag){
        if(flag) return 1;
        else return 2.3; // error
    }
    // inconsistent deduction for auto return type: 'int' and then 'double'
    ```
2. 如果return语句返回初始化列表，返回值类型推导也失败。
    ```cpp
    auto func(){
        return {1, 2, 3};   // error returning initializer list
    }
    ```
3. 如果函数是虚函数，不能使用返回类型推导。
    ```cpp
    struct A{
        // error: virtual function cannot have deduced return type
        virtual auto func() { return 1; }
    }
    ```
4. 返回类型推导可以在前向声明中，但是在使用他们之前，翻译单元中必须能够得到函数定义。
    ```cpp
    auto f();       // declared, not yet defined.
    auto f() { return 42; }     // defined, return type is int

    int main(){
        cout << f() << endl;
    }
    ```
5. 返回类型推导可以用在递归函数中，但是递归调用必须以至少一个返回语句作为先导，以便编译器推导出返回类型。
    ```cpp
    auto sum(int i){
        if(i == 1) return i;
        else return sum(i - 1) + i;
    }
    ```

#### lambda参数auto
在C++11中，lambda表达式参数需要使用具体的类型声明：
```cpp
auto f = [](int a) { return a; }
```
在C++14中，对此进行优化，lambda表达式参数可以直接是auto：
```cpp
auto f = [](auto a){ return a; }
cout << f(1) << endl;
cout << f(2.3f) << endl;
```

#### 变量模板
C++14支持变量模板：
```cpp
template<class T>
constexpr T pi = T(3.1415926535897932385L);
int main(){
    cout << pi(int) << endl;
    cout << pi(double) << endl;
}
```

#### 别名模板
C++14 也支持别名模板
```cpp
template<typename T, typename U>
struct A{
    T t;
    U u;
};

template<typename T>
using B = A<T, int>;

int main(){
    B<double> b;
    b.t = 10;
    b.u = 20;
    cout << b.t << endl;
    cout << b.u << endl;
    return 0;
}
```

#### constexpr的限制
C\+\+14 相较于 C\+\+11 对 constexpr 减少了一些限制：
1. C\+\+11 中constexpr函数可以递归使用，在 C\+\+14 中可以使用局部变量和循环
   ```cpp
   constexpr int factorial(int n){  // C++14 和 C++11 均可
        return n <= 1 ? 1 : (n * factorial(n - 1));
   }
   ```
   在 C++14 中可以这样做：
   ```cpp
   constexpr int factorial(int n){  // C++11 中不可以， C++14 中可以
        int ret = 0;
        for(int i = 0; i < n; ++i){
            ret += i;
        }
        return ret;
   }
   ```
2. C++11 中 constexpr 函数必须把所有的东西都放在一个单独的return语句中，而constexpr则无此限制：
   ```cpp
   constexpr int func(bool flag){   // C++14 和 C++11 均可
        return 0;
   }
   ```
   在 C++14 中可以这样：
   ```cpp
   constexpr int func(bool flag){   // C++11 中不可以， C++14 中可以
        if(flag) return 1;
        else return 0;
   }
   ```

#### \[\[deprecated\]\] 标记
C++14 中增加了 deprecated 标记，修饰类、变量、函数等，当程序中使用了被其修饰的代码的时候，编译时会产生警告，用来提示开发者该标记修饰的内容将来可能会被移除，尽量不要使用。
```cpp
struct [[deprecated]] A {};

int main(){
    A a;
    return 0;
}
```

当编译时，会出现如下警告：
```bash
~/test$ g++ test.cc -std=c++14
test.cc: In function ‘int main()’:
test.cc:11:7: warning: ‘A’ is deprecated [-Wdeprecated-declarations]
     A a;
       ^
test.cc:6:23: note: declared here
 struct [[deprecated]] A {
```

#### 二进制字面量与整形字面量分隔符
C++14 引入了二进制字面量，也引入了分隔符。
```cpp
int a = 0b0001'0010'1010;
double b = 3.14'1234'1234'1234;
```

#### std::make_unique
我们都知道 C\+\+11 中有std::make_shared，却没有std::make_unique，在 C\+\+14 中已经完善。
```cpp
struct A {};
std::unique_ptr<A> ptr = std::make_unique<A>();
```

#### std::make_timed_mutex 与 std::shared_lock
C++14 通过 std::make_timed_mutex 与 std::shared_lock 来实现读写锁，保证多个线程可以同时读，写操作不可以同时和读操作一起进行。
实现方式如下：
```cpp
struct ThreadSafe{
    mutable std::make_timed_mutex mutex_;
    int value_;
    ThreadSafe(){
        value_ = 0;
    }
    int get() const {
        std::shared_lock<std::shared_timed_mutex> loc(mutex_);
        return value_;
    }
    void increase() {
        std::unique_lock<std::shared_timed_mutex> lock(mutex_);
        value_ += 1;
    }
}
```
timed锁可以带来超时时间。

#### std::integer_sequence :star:
```cpp
template<typename T, T... ints>
void print_sequence(std::integer_sequence<T, ints...> int_seq){
    std::cout << "the sequence of size " << int_seq.size() << ": ";
    ((std::cout << ints << " "), ...);
    stdcout << "\n";
}
```
std::integer_sequence 和 std::tuple 的配合使用：
```cpp
template <std::size_t... Is, typename F, typename T>
auto map_filter_tuple(F f, T& t){
    return std::make_tuple(f(std::get<Is>(t))...);
}
template <std::size_t... Is, typename F, typename T>
auto map_filter_tuple(std::index_sequence<Is...>, F f, T& t){
    return std::make_tuple(f(std::get<Is>(t))...);
}
template <typename S, typename F, typename T>
auto map_filter_tuple(F&& f, T& t){
    return map_filter_tuple(S{}, std::forward<F>(f), t);
}
```

#### std::exchange
```cpp
// exchange 的实现
template<class T, class U = T>
constexpr T exchange(T& obj, U&& new_value){
    T old_value = std::move(obj);
    obj = std::forward<T>(new_value);
    return old_value;
}
// new_value 的值给了 obj，而没有对 new_value 赋值。
int main(){
    std::vector<int> v;
    std::exchange(v, {1, 2, 3, 4});
    cout << v.size() << endl;
    for(int a: v){
        cout << a << " ";
    }
    return 0;
}
```

#### std::quoted
C++14 引入 std::quoted 用于给字符串添加双引号
```cpp
int main(){
    string str = "hello world";
    cout << str << endl;
    cout << std::quoted(str) << endl;
    return 0;
}
```

### C++17新特性 [^3]
#### 构造函数模板推导
在 C++17 前构造一个模板类对象需要指明类型：
```cpp
pair<int, double> p(1, 2.2);    // before C++17
```
C++17 就不需要特殊指定，直接可以推导出类型：
```cpp
pair p(1, 2.2); // C++17 自动推导
vector v = {1, 2, 3};   // C++17
```

#### 结构化绑定 :star:
通过结构化绑定，对于`tuple`、`map` 等类型，获取相应值会方便很多
```cpp
std::tuple<int, double> func(){
    return std::tuple(1, 2.2);
}
int main(){
    auto [i, d] = func();
    cout << i << endl;
    cout << d << endl;
}
```

```cpp
void f(){
    map<int, string> m = {{0, "a"}, {1, "b"}};
    for(const auto& [i, s]: m){
        cout << i << " " << s << endl;
    }
}
int main(){
    std::pair a(1, 2.3f);
    auto [i, f] = a;
    cout << i << endl;
    cout << f << endl;
    return 0;
}
```

引用的结构化绑定还可以改变对象的值
```cpp
int main(){
    std::pair a(1, 2.3f);
    auto& [i, f] = a;
    i = 2;
    cout << a.first << endl;
}
```
*注意结构化绑定不能应用于constexpr*
```cpp
constexpr auto [x, y] = std::pair(1, 2.3f); // compile error, C++20 可以
```
结构化绑定不仅可以绑定 pair 和 tuple ，还可以绑定数组和结构体等。
```cpp
int array[3] = {1, 2, 3};
auto [a, b, c] = array;
cout << a << " " << b << " " << c << endl;
// 注意这里的struct的成员一定是要public的
struct Point{
    int x, y;
};
Point func(){
    return {1, 2};
}
const auto [x, y] = func();
```
这里其实可以实现自定义类的结构化绑定，代码如下：
```cpp
// 需要实现相关的tuple_size和tuple_element和get<N>方法。
class Entry{
public:
    void Init(){
        name_ = "name";
        age_ = 10;
    }
    std::string GetName() const { return name_; }
    int GetAge() const { return age_; }
private:
    std::string name_;
    int age_;
}

template <size_t I>
auto get(const Entry& e){
    if constexpr (I == 0) return e.GetName();
    else if constexpr(I == 1) return e.GetAge();
}

namespace std{
    template<> struct tuple_size<Entry> : integral_constant<size_t, 2>{};
    template<> struct tuple_element<0, Entry> { using type = std::string; };
    template<> struct tuple_element<1, Entry> { using type = int; };
}

int main(){
    Entry e;
    e.Init();
    auto [name, age] = e;
    cout << name << " " << age << endl; // name 10
    return 0;
}
```

#### if-switch 语句初始化
C++17 前if语句需要这样写代码：
```cpp
int a = GetValue();
if(a < 101){
    cout << a;
}
```
C++17 之后可以这样：
```cpp
// if (init; condition)

if(int a = GetValue(); a < 101){
    cout << a;
}

string str = "Hi World";
if(auto [pos, size] = pair(str.find("Hi"), str.size()); pos != string::npos){
    std::cout << pos << " Hello, size is " << size;
}
```
使用这种方式可以尽可能约束作用域，让代码更简洁，可读性略有下降，但是还好

#### 内联变量
C\+\+17 前只有内联函数，现在有了内联变量，我们印象中 C\+\+ 类的静态成员变量在头文件中是不能初始化的，但是有了内联变量，就可以达到此目的了：
```cpp
// header file
struct A {
    static const int value;
}
inline int const A::value = 10;

// ========= 或者 ===========
struct A {
    inline static const int value = 10;
}
```

#### 折叠表达式
C\+\+17 引入了折叠表达式使可变模板编程更方便：
```cpp
template <typename ... Ts>
auto sum(Ts ... ts){
    return (ts + ...);
}
int a = {sum(1, 2, 3, 4, 5)};   // 15
std::string a{"hello "};
std::string b{"world"};
cout << sum(a, b) << endl;      // hello world
```

#### constexpr lambda 表达式
C\+\+17 前 lambda 表达式只能在运行时使用，C\+\+17引入了constexpr lambda表达式，可以用于在编译期进行计算。
```cpp
int main(){     // C++17可编译
    constexpr auto lamb = [](int n){ return n * n; };
    static_assert(lamb(3) == 9, "a");
}
```
**注意**：constexpr函数有如下限制：
函数体不能包含汇编语句、goto语句、label、try块、静态变量、线程局部存储、没有初始化的普通变量，不能动态分配内存，不能有new、delete等，不能虚函数。

#### namespace嵌套
```cpp
namespace A{
    namespace B{
        namespace C{
            void func();
        }
    }
}

// C++17，更方便更舒适
namespace A::B::C {
    void func();
}
```

#### __has_include预处理表达式
可以判断是否有某个头文件，代码可能会在不同编译器下工作，不同编译器的可用头文件有可能不同，所以可以用此来判断：
```cpp
#if defined __has_include
#if __has_include(<charconv>)
#define has_charconv 1
#include <charconv>
#endif
#endif

std::optional<int> ConvertToInt(const std::string& str){
    int value{};
#ifdef has_charconv
    const auto last = str.data() + str.size();
    const auto res = std::from_chars(str.data(), last, value);
    if(res.ec == std::errc{} and res.ptr == last) return value;
#else
    // alternative implementation...
    // 其他的实现方式
#endif
    return std::nullopt;
}
```

#### 在lambda表达式中用*this捕获对象副本
正常情况下，lambda表达式中访问类的成员变量需要捕获this，但是这里捕获的是this指针，指向的是对象的引用，正常情况下可能没问题，但是如果多线程情况下，函数的作用域超过了对象的作用域，对象已经被析构，还访问了成员变量，就会有问题。
```cpp
struct A{
    int a;
    void func(){
        auto f = [this]{
            cout << a << endl;
        };
        f();
    }
};

int main(){
    A a;
    a.func();
    return 0;
}
```
所以 C\+\+17 增加了新特性，捕获*this，不持有this指针，而是持有对象的拷贝，这样生命周期就与对象的生命周期不相关了。
```cpp
struct A{
    int a;
    void func(){
        auto f = [*this]{
            cout << a << endl;
        };
        f();
    }
};

int main(){
    A a;
    a.func();
    return 0;
}
```

#### 新增Attribute
我们可能平时在项目中见过__declspec、attribute, #pragma指示符，使用它们来给编译器提供一些额外的信息，来产生一些优化或特定的代码，也可以给其他开发者一些提示信息。
例如：
```cpp
struct A { short f[3]; } __attribute__((aligned(8)));

void fatal() __attribute__((noreturn));
```
在C\+\+11和C\+\+14中有更方便的方法：
```cpp
[[carries_dependency]] 让编译期跳过不必要的内存栅栏指令
[[noreturn]] 函数不会返回
[[deprecated]] 函数将弃用的警告

[[noreturn]] void terminate() noexcept;
[[deprecated("use new func instead")]] void func() {}
```
C\+\+17又新增了三个:
\[\[fallthrough\]\]，用在switch提示可以直接落下去，不需要break，让编译器忽略警告。
```cpp
switch (i) {
    case 1:
        xxx;    // warning
    case 2:
        xxx;
        [[fallthrough]];    // 消除警告
    case 3:
        xxx;
        break;
}
```
使得编译器和其他开发者都可以理解开发者的意图。

\[\[nodiscard\]\]：表示修饰的内容不能被忽略，可用于修饰函数，标明返回值一定要被处理。
```cpp
[[nodiscard]] int func();
void F(){
    func(); // warning 没有处理函数返回值
}
```

\[\[maybe_unused\]\]：提示编译器修饰的内容可能暂时没有使用，避免产生警告。
```cpp
void func1() {}
[[maybe_unused]] void func2() {}    // 消除警告
void func3() {
    int x = 1;
    [[maybe_unused]] int y = 2;     // 消除警告
}
```

#### 字符串转换 :star:
新增from_chars函数和to_chars函数，直接看代码：
```cpp
#include <charconv>

int main(){
    const std::string str{"123456098"};
    int value = 0;
    const auto res = std::from_chars(str.data(), str.data() + 4, value);
    if (res.ec == std::errc()){
        cout << value << ", distance " << res.ptr - str.data() << endl;
    }else if(res.ec == std::errc::invalid_argument){
        cout << "invalid" << endl;
    }

    str = std::string("12.34");
    double val = 0;
    const auto format = std::chars_format::general;
    res = std::from_chars(str.data(), str.data() + str.size(), value, format);

    str = std::string("xxxxxxxx");
    const int v = 1234;
    res = std::to_chars(str.data(), str.data() + str.size(), v);
    cout << str << ", filled " << res.ptr - str.data() << " characters \n";
    // 1234xxx, filled 4 characters.
}
```

#### std::variant
C\+\+17增加了std::variant实现类似union的功能，但却比union更高级，举个例子union里面不能有string这种类型，但std::variant却可以，还可以支持更多复杂类型，如map等，看代码：
```cpp
int main(){ // C++17可编译
    std::variant<int, std::string> var("hello");
    cout << var.index() << endl;
    var = 123;
    cout << var.index() << endl;

    try{
        var = "world";
        std::string str = std::get<std::string>(var);   //通过类型获取值
        var = 3;
        int i = std::get<0>(var);   // 通过index获取值
        cout << str << endl;
        cout << i << endl;
    }catch(...){
        // xxx
    }
    return 0;
}
```
注意：一般情况下variant的第一个类型要有对应的构造函数，否则编译失败：
```cpp
struct A{
    A(int i) {}
};
int main(){
    std::variant<A, int> var;   // 编译失败
}
```
如何避免这种情况，可以使用std::monostate来打个桩，模拟一个空状态。
```cpp
std::variant<std::monostate, A> var;    // 可以编译成功
```

#### std::optional
我们有时候可能会有需求，让函数返回一个对象，如下：
```cpp
struct A {};
A func(){
    if(flag) return A();
    else {
        // 异常情况下，怎么返回异常值，想返回一个空
    }
}
```

有一种方法是返回对象指针，异常情况下就可以返回nullptr啦，但是这就涉及到了内存管理，也许你会使用智能指针，但是这里更方便的方法就是std::optional啦。
```cpp
std::optional<int> StoI(const std::string& s){
    try{
        return std::stoi(s);
    }catch(...){
        return std::nullopt;
    }
}
void func(){
    std::string s{"123"};
    std::optional<int> o = StoI(s);
    if(o){
        cout << *o << endl;
    }else{
        cout << "error" << endl;
    }
}
```

#### std::any :star:
C\+\+17引入了any可以用来存储任何类型的单个值，见代码：
```cpp
int main(){     // C++17可编译
    std::any a = 1;
    cout << a.type().name() << " " << std::any_cast<int>(a) << endl;
    a = 2.2f;
    cout << a.type().name() << " " << std::any_cast<double>(a) << endl;
    a.reset();
    if(a.has_value()){
        cout << a.type().name();
    }
    a = std::string("a");
    cout << a.type().name() << " " << std::any_cast<std::string>(a) << endl;
}
```

#### std::apply
使用std::apply可以将tuple展开作为函数参数传入，见代码：
```cpp
int add(int first, int second) { return first + second; }

auto add_lambda = [](auto first, auto second) { return first + second; }

int main(){
    std::cout << std::apply(add, std::pair(1, 2)) << "\n";
    std::cout << add(std::pair(1, 2)) << "\n";
    std::cout << std::apply(add_lambda, std::tuple(2.0f, 3.0f)) << "\n";
}
```

#### std::make_from_tuple
使用make_from_tuple可以将tuple展开作为构造函数参数
```cpp
struct Foo{
    Foo(int first, int second, int third){
        std::cout << first << " " << second << " " << third << std::endl;
    }
};

int main(){
    auto tuple = std::make_tuple(42, 3.14f, 0);
    std::make_from_tuple<Foo>(std::move(tuple));
}
```

#### std::string_view
通常我们传递一个string的时候，会触发对象的拷贝操作，大字符串的拷贝赋值操作会触发堆的内存分配，很影响运行效率，有了string_view就可以避免拷贝操作，平时传递过程中传递string_view即可。

```cpp
void func(std::string_view stv) { cout << stv << endl; }

int main(){
    std::string str = "Hello World";
    std::cout << str << std::endl;

    std::string_view stv(str.c_str(), str.size());
    cout << stv << endl;
    func(stv);
    return 0;
}
```

#### as_const 
C\+\+17使用as_const可以将左值转成const类型
```cpp
std::string str = "string";
const std::string& constStr = std::as_const(str);
```

#### file_system
C\+\+17正式将file_system纳入到标准之中，提供了关于文件的大多数功能，基本上应有尽有，这里举几个简单例子
```cpp
namespace fs = std::filesystem;
fs::create_directory(dir_path);
fs::copy_file(src, dst, fs::copy_options::skip_existing);
fs::exists(filename);
fs::current_path(err_code);
```

#### std::shared_mutex
C\+\+17引入了shared_mutex，可以实现读写锁
### C++20新特性


# 操作系统
## 说说静态库和动态库的区别是什么[^1]
1. 静态库代码装载的速度快，执行速度略比动态库快。
2. 动态库更加节省内存，可执行文件体积比静态库小很多。
3. 静态库是在编译时加载，动态库是在运行时加载。
4. 生成的静态链接库，Windows下以.lib为后缀，Linux下以.a为后缀。生成的动态链接库，Windows下以.dll为后缀，Linux下以.so为后缀。

### 虚拟内存
操作系统为每一个进程分配一个独立的地址空间，这就是虚拟内存。虚拟内存与物理内存存在映射关系，通过页表寻址完成虚拟地址和物理地址的转换。
#### 为什么要用虚拟内存
因为早期的内存分配方法存在以下问题：
1. 进程地址空间不隔离。会导致数据被随意修改。
2. 内存使用效率低。
3. 程序运行的地址不确定。操作系统随机为进程分配内存空间，所以程序运行的地址是不确定的。

#### 使用虚拟内存的好处
1. 扩大地址空间。每个进程独占一个4G空间，虽然真实物理内存没那么多。
2. 内存保护：防止不同进程对物理内存的争夺和践踏，可以对特定内存地址提供写保护，防止恶意篡改。
3. 可以实现内存共享，方便进程通信。
4. 可以避免内存碎片，虽然物理内存可能不连续，但映射到虚拟内存上可以连续。

# 计算机网络
## TCP与UDP

## 拥塞控制

# Redis
## Redis的数据类型

# 数据库原理
## 说一说你对数据库事务的了解
事务可由一条非常简单的SQL语句组成，也可以由一组复杂的SQL语句组成。在事务中的操作，要么都执行修改，要么都不执行，这就是事务的目的，也是事务模型区别于文件系统的重要特征之一。

事务需遵循ACID四个特性：
- A（atomicity），原子性。原子性指整个数据库事务是不可分割的工作单位。只有使事务中所有的数据库操作都执行成功，整个事务的执行才算成功。事务中任何一个SQL语句执行失败，那么已经执行成功的SQL语句也必须撤销，数据库状态应该退回到执行事务前的状态。
- C（consistency），一致性。一致性指事务将数据库从一种状态转变为另一种一致的状态。在事务开始之前和事务结束以后，数据库的完整性约束没有被破坏。
- I（isolation），隔离性。事务的隔离性要求每个读写事务的对象与其他事务的操作对象能相互分离，即该事务提交前对其他事务都不可见，这通常使用锁来实现。
- D（durability） ，持久性。事务一旦提交，其结果就是永久性的，即使发生宕机等故障，数据库也能将数据恢复。持久性保证的是事务系统的高可靠性，而不是高可用性。

事务可以分为以下几种类型：

- 扁平事务：是事务类型中最简单的一种，而在实际生产环境中，这可能是使用最为频繁的事务。在扁平事务中，所有操作都处于同一层次，其由BEGIN WORK开始，由COMMIT WORK或ROLLBACK WORK结束。处于之间的操作是原子的，要么都执行，要么都回滚。
- 带有保存点的扁平事务：除了支持扁平事务支持的操作外，允许在事务执行过程中回滚到同一事务中较早的一个状态，这是因为可能某些事务在执行过程中出现的错误并不会对所有的操作都无效，放弃整个事务不合乎要求，开销也太大。保存点（savepoint）用来通知系统应该记住事务当前的状态，以便以后发生错误时，事务能回到该状态。
- 链事务：可视为保存点模式的一个变种。链事务的思想是：在提交一个事务时，释放不需要的数据对象，将必要的处理上下文隐式地传给下一个要开始的事务。注意，提交事务操作和开始下一个事务操作将合并为一个原子操作。这意味着下一个事务将看到上一个事务的结果，就好像在一个事务中进行的。
- 嵌套事务：是一个层次结构框架。有一个顶层事务（top-level transaction）控制着各个层次的事务。顶层事务之下嵌套的事务被称为子事务（subtransaction），其控制每一个局部的变换。
- 分布式事务：通常是一个在分布式环境下运行的扁平事务，因此需要根据数据所在位置访问网络中的不同节点。对于分布式事务，同样需要满足ACID特性，要么都发生，要么都失效。

对于MySQL的InnoDB存储引擎来说，它支持扁平事务、带有保存点的扁平事务、链事务、分布式事务。对于嵌套事务，MySQL数据库并不是原生的，因此对于有并行事务需求的用户来说MySQL就无能为力了，但是用户可以通过带有保存点的事务来模拟串行的嵌套事务。
## 谈谈MySQL的事务隔离级别
SQL 标准定义了四种隔离级别，这四种隔离级别分别是：
- 读未提交（READ UNCOMMITTED）；
- 读提交 （READ COMMITTED）；
- 可重复读 （REPEATABLE READ）；
- 串行化 （SERIALIZABLE）。

事务隔离是为了解决脏读、不可重复读、幻读问题，下表展示了 4 种隔离级别对这三个问题的解决程度：

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
| --- | --- | --- | --- |
| READ UNCOMMITTED | 可能 | 可能 | 可能 |
| READ COMMITTED | 不可能 | 可能 | 可能 |
| REPEATABLE READ | 不可能 | 不可能 | 可能 |
| SERIALIZABLE | 不可能 | 不可能 | 不可能 |

上述4种隔离级别MySQL都支持，并且InnoDB存储引擎默认的支持隔离级别是REPEATABLE READ，但是与标准SQL不同的是，InnoDB存储引擎在REPEATABLE READ事务隔离级别下，使用Next-Key Lock的锁算法，因此避免了幻读的产生。所以，InnoDB存储引擎在默认的事务隔离级别下已经能完全保证事务的隔离性要求，即达到SQL标准的SERIALIZABLE隔离级别。

并发情况下，读操作可能存在的三类问题：
- 脏读：当前事务(A)中可以读到其他事务(B)未提交的数据（脏数据），这种现象是脏读。
- 不可重复读：在事务A中先后两次读取同一个数据，两次读取的结果不一样，这种现象称为不可重复读。脏读与不可重复读的区别在于：前者读到的是其他事务未提交的数据，后者读到的是其他事务已提交的数据。
- 幻读：在事务A中按照某个条件先后两次查询数据库，两次查询结果的条数不同，这种现象称为幻读。不可重复读与幻读的区别可以通俗的理解为：前者是数据变了，后者是数据的行数变了。


# 软件设计模式

# 计算机组成原理
## L1 cache和内存的速度差距

# 编译原理

# 几个算法题
## 不使用条件判断, 实现两个数取较小值的函数
## $1,2,3,\cdots,n$ 中缺失了两个数, 求缺失的数

# 参考
[^1]: [C++岗位面试真题宝典](https://www.nowcoder.com/issue/tutorial?tutorialId=10069)
[^2]: [C++14新特性的所有知识点全在这儿啦！](https://segmentfault.com/a/1190000023441427)
[^3]: [C++17新特性](https://segmentfault.com/a/1190000023456766)
[^4]: [为什么 C++ 中使用虚函数时会影响效率？](https://www.zhihu.com/question/22958966/answer/23195612)
