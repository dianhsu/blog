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

# C\+\+

## 虚函数
### 虚函数，纯虚函数和虚析构函数 [^1]

- C\+\+ 中的虚函数的作用主要是实现了多态的机制。关于多态，简而言之就是用父类型的指针指向其子类的实例，然后通过父类的指针调用实际子类的成员函数。这种技术可以让父类的指针有“多种形态”，这是一种泛型技术。如果调用非虚函数，则无论实际对象是什么类型，都执行基类类型所定义的函数。非虚函数总是在编译时根据调用该函数的对象，引用或指针的类型而确定。如果调用虚函数，则直到运行时才能确定调用哪个函数，运行的虚函数是引用所绑定或指针所指向的对象所属类型定义的版本。虚函数必须是基类的非静态成员函数。虚函数的作用是实现动态联编，也就是在程序的运行阶段动态地选择合适的成员函数，在定义了虚函数后，可以在基类的派生类中对虚函数重新定义，在派生类中重新定义的函数应与虚函数具有相同的形参个数和形参类型。以实现统一的接口，不同定义过程。如果在派生类中没有对虚函数重新定义，则它继承其基类的虚函数。
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

## C\+\+11/14/17/20新特性
### C\+\+11新特性
#### 智能指针
##### unique_ptr
> 为动态申请的内存提供异常安全
> 将动态申请内存的所有权传递给某个函数(不能给复制，只能移动)
> 从某个函数返回动态申请内存的所有权
> 在容器中保存指针

在那些要不是为了避免不安全的异常问题（以及为了保证指针所指向的对象都被正确地删除释放），我们不可以使用内建指针的情况下，我们可以在容器中保存unique_ptr以代替内建指针

##### shared_ptr & weak_ptr
当 shared_ref_cnt 被减为0时，自动释放 ptr 指针所指向的对象。当 shared_ref_cnt 与 weak_ref_cnt 都变成0时，才释放 ptr_manage 对象。
如此以来，只要有相关联的 shared_ptr 存在，对象就存在。weak_ptr 不影响对象的生命周期。当用 weak_ptr 访问对象时，对象有可能已被释放了，要先 lock()。
weak_ptr可以保存一个“弱引用”，指向一个已经用shared_ptr进行管理的对象。为了访问这个对象，一个weak_ptr可以通过shared_ptr的构造函数或者是weak_ptr的成员函数lock()转化为一个shared_ptr。当最后一个指向这个对象的shared_ptr退出其生命周期并且这个对象被释放之后，将无法从指向这个对象的weak_ptr获得一个shared_ptr指针，shared_ptr的构造函数会抛出异常，而weak_ptr::lock也会返回一个空指针。

###### weak_ptr防止循环引用
众所周知，shared_ptr可能造成循环引用问题，那么weak_ptr是怎么解决循环引用问题的呢？看一个例子
```cpp
class A {
public:
    shared_ptr<B> ab;
    // 这里可以加上构造／析构函数看下是否能够被调用
};
class B {
public:
    shared_ptr<A> ba;
    // 这里可以加上构造／析构函数看下是否能够被调用
};
shared_ptr<A> spa = make_shared<A>();  // 定义一个A对象
shared_ptr<B> spb = make_shared<B>();  // 定义一个A对象
spa.ab = spb; //shared_ptr计数成员_Sp_counted_base浅拷贝，use ref＋＋
spb.ba = spa;
```
显然，由于A、B互相引用，都无法释放，造成内存泄漏(示例参考自blog)

怎样打破这种循环引用？cppreference的说法是

> std::weak_ptr 的另一用法是打断 std::shared_ptr 所管理的对象组成的环状引用。若这种环被孤立（例如无指向环中的外部共享指针），则 shared_ptr 引用计数无法抵达零，而内存被泄露。能令环中的指针之一为弱指针以避免此情况。

#### 右值引用与移动构造函数


### C\+\+14新特性 [^2]
#### 函数返回值类型推导
C\+\+14 对函数返回类型推导规则做了优化，先看一段代码：
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

使用C\+\+11编译：
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
在C\+\+11中，lambda表达式参数需要使用具体的类型声明：
```cpp
auto f = [](int a) { return a; }
```
在C\+\+14中，对此进行优化，lambda表达式参数可以直接是auto：
```cpp
auto f = [](auto a){ return a; }
cout << f(1) << endl;
cout << f(2.3f) << endl;
```

#### 变量模板
C\+\+14支持变量模板：
```cpp
template<class T>
constexpr T pi = T(3.1415926535897932385L);
int main(){
    cout << pi(int) << endl;
    cout << pi(double) << endl;
}
```

#### 别名模板
C\+\+14 也支持别名模板
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
   在 C\+\+14 中可以这样做：
   ```cpp
   constexpr int factorial(int n){  // C++11 中不可以， C++14 中可以
        int ret = 0;
        for(int i = 0; i < n; ++i){
            ret += i;
        }
        return ret;
   }
   ```
2. C\+\+11 中 constexpr 函数必须把所有的东西都放在一个单独的return语句中，而constexpr则无此限制：
   ```cpp
   constexpr int func(bool flag){   // C++14 和 C++11 均可
        return 0;
   }
   ```
   在 C\+\+14 中可以这样：
   ```cpp
   constexpr int func(bool flag){   // C++11 中不可以， C++14 中可以
        if(flag) return 1;
        else return 0;
   }
   ```

#### \[\[deprecated\]\] 标记
C\+\+14 中增加了 deprecated 标记，修饰类、变量、函数等，当程序中使用了被其修饰的代码的时候，编译时会产生警告，用来提示开发者该标记修饰的内容将来可能会被移除，尽量不要使用。
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
C\+\+14 引入了二进制字面量，也引入了分隔符。
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
C\+\+14 通过 std::make_timed_mutex 与 std::shared_lock 来实现读写锁，保证多个线程可以同时读，写操作不可以同时和读操作一起进行。
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
C\+\+14 引入 std::quoted 用于给字符串添加双引号
```cpp
int main(){
    string str = "hello world";
    cout << str << endl;
    cout << std::quoted(str) << endl;
    return 0;
}
```

### C\+\+17新特性 [^3]
#### 构造函数模板推导
在 C\+\+17 前构造一个模板类对象需要指明类型：
```cpp
pair<int, double> p(1, 2.2);    // before C++17
```
C\+\+17 就不需要特殊指定，直接可以推导出类型：
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
C\+\+17 前if语句需要这样写代码：
```cpp
int a = GetValue();
if(a < 101){
    cout << a;
}
```
C\+\+17 之后可以这样：
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

### C\+\+20新特性


# 操作系统
## 什么是僵尸进程？
一个子进程结束后，它的父进程并没有等待它（调用wait或者waitpid），那么这个子进程将成为一个僵尸进程。僵尸进程是一个已经死亡的进程，但是并没有真正被销毁。它已经放弃了几乎所有内存空间，没有任何可执行代码，也不能被调度，仅仅在进程表中保留一个位置，记载该进程的进程ID、终止状态以及资源利用信息(CPU时间，内存使用量等等)供父进程收集，除此之外，僵尸进程不再占有任何内存空间。这个僵尸进程可能会一直留在系统中直到系统重启。

危害：占用进程号，而系统所能使用的进程号是有限的；占用内存。

以下情况不会产生僵尸进程：
- 该进程的父进程先结束了。每个进程结束的时候，系统都会扫描是否存在子进程，如果有则用Init进程接管，成为该进程的父进程，并且会调用wait等待其结束。
- 父进程调用wait或者waitpid等待子进程结束（需要每隔一段时间查询子进程是否结束）。wait系统调用会使父进程暂停执行，直到它的一个子进程结束为止。waitpid则可以加入```WNOHANG```(wait-no-hang)选项，如果没有发现结束的子进程，就会立即返回，不会将调用waitpid的进程阻塞。同时，waitpid还可以选择是等待任一子进程（同wait），还是等待指定pid的子进程，还是等待同一进程组下的任一子进程，还是等待组ID等于pid的任一子进程；
- 子进程结束时，系统会产生```SIGCHLD```(signal-child)信号，可以注册一个信号处理函数，在该函数中调用waitpid，等待所有结束的子进程（注意：一般都需要循环调用waitpid，因为在信号处理函数开始执行之前，可能已经有多个子进程结束了，而信号处理函数只执行一次，所以要循环调用将所有结束的子进程回收）；
- 也可以用```signal(SIGCLD, SIG_IGN)```(signal-ignore)通知内核，表示忽略```SIGCHLD```信号，那么子进程结束后，内核会进行回收。

## 什么是孤儿进程？
<details>
<summary>展开</summary>

一个父进程已经结束了，但是它的子进程还在运行，那么这些子进程将成为孤儿进程。孤儿进程会被Init（进程ID为1）接管，当这些孤儿进程结束时由Init完成状态收集工作。
</details>

## 什么是IO多路复用？怎么实现？
IO多路复用（IO Multiplexing）是指单个进程/线程就可以同时处理多个IO请求。

实现原理：用户将想要监视的文件描述符（File Descriptor）添加到select/poll/epoll函数中，由内核监视，函数阻塞。一旦有文件描述符就绪（读就绪或写就绪），或者超时（设置timeout），函数就会返回，然后该进程可以进行相应的读/写操作。

<details>
<summary>select/poll/epoll三者的区别？</summary>

- ```select```：将文件描述符放入一个集合中，调用select时，将这个集合从用户空间拷贝到内核空间（缺点1：每次都要复制，**开销大**），由内核根据就绪状态修改该集合的内容。（缺点2）**集合大小有限制**，32位机默认是1024（64位：2048）；采用水平触发机制。select函数返回后，需要通过遍历这个集合，找到就绪的文件描述符（缺点3：**轮询的方式效率较低**），当文件描述符的数量增加时，效率会线性下降；
- ```poll```：和select几乎没有区别，区别在于文件描述符的存储方式不同，poll采用链表的方式存储，没有最大存储数量的限制；
- ```epoll```：通过内核和用户空间共享内存，避免了不断复制的问题；支持的同时连接数上限很高（1G左右的内存支持10W左右的连接数）；文件描述符就绪时，采用回调机制，避免了轮询（回调函数将就绪的描述符添加到一个链表中，执行epoll_wait时，返回这个链表）；支持水平触发和边缘触发，采用边缘触发机制时，只有活跃的描述符才会触发回调函数。

总结，区别主要在于：
- 一个线程/进程所能打开的最大连接数
- 文件描述符传递方式（是否复制）
- 水平触发 or 边缘触发
- 查询就绪的描述符时的效率（是否轮询）
</details>

<details>
<summary>什么时候使用select/poll，什么时候使用epoll？</summary>

当连接数较多并且有很多的不活跃连接时，epoll的效率比其它两者高很多；但是当连接数较少并且都十分活跃的情况下，由于epoll需要很多回调，因此性能可能低于其它两者。
</details>

<details>
<summary>什么是文件描述符？</summary>

文件描述符在形式上是一个非负整数。实际上，它是一个索引值，指向内核为每一个进程所维护的该进程打开文件的记录表。当程序打开一个现有文件或者创建一个新文件时，内核向进程返回一个文件描述符。

内核通过文件描述符来访问文件。文件描述符指向一个文件。
</details>

## 缺页中断
- 缺页异常：malloc和mmap函数在分配内存时只是建立了进程虚拟地址空间，并没有分配虚拟内存对应的物理内存。当进程访问这些没有建立映射关系的虚拟内存时，处理器自动触发一个缺页异常，引发缺页中断。
- 缺页中断：缺页异常后将产生一个缺页中断，此时操作系统会根据页表中的外存地址在外存中找到所缺的一页，将其调入内存。
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

## 什么是协程？

协程是一种用户态的轻量级线程，协程的调度完全由用户控制。协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈，直接操作栈则基本没有内核切换的开销，可以不加锁的访问全局变量，所以上下文的切换非常快。

### 协程与线程进行比较？
<details>
<summary>展开</summary>

1. 一个线程可以拥有多个协程，一个进程也可以单独拥有多个协程，这样python中则能使用多核CPU。

2. 线程进程都是同步机制，而协程则是异步

3. 协程能保留上一次调用时的状态，每次过程重入时，就相当于进入上一次调用的状态
</details>

## 什么是死锁？

在两个或者多个并发进程中，每个进程持有某种资源而又等待其它进程释放它们现在保持着的资源，在未改变这种状态之前都不能向前推进，称这一组进程产生了死锁(deadlock)。

## 死锁产生的必要条件？
- **互斥**：一个资源一次只能被一个进程使用；
- **占有并等待**：一个进程至少占有一个资源，并在等待另一个被其它进程占用的资源；
- **非抢占**：已经分配给一个进程的资源不能被强制性抢占，只能由进程完成任务之后自愿释放；
- **循环等待**：若干进程之间形成一种头尾相接的环形等待资源关系，该环路中的每个进程都在等待下一个进程所占有的资源。

## 有哪些页面置换算法？
在程序运行过程中，如果要访问的页面不在内存中，就发生缺页中断从而将该页调入内存中。此时如果内存已无空闲空间，系统必须从内存中调出一个页面到磁盘中来腾出空间。页面置换算法的主要目标是使页面置换频率最低（也可以说缺页率最低）。

- **最佳页面置换算法**OPT（Optimal replacement algorithm）：置换以后不需要或者最远的将来才需要的页面，是一种理论上的算法，是最优策略；
- **先进先出**FIFO：置换在内存中驻留时间最长的页面。缺点：有可能将那些经常被访问的页面也被换出，从而使缺页率升高；
- **第二次机会算法**SCR：按FIFO选择某一页面，若其访问位为1，给第二次机会，并将访问位置0；
- **时钟算法** Clock：SCR中需要将页面在链表中移动（第二次机会的时候要将这个页面从链表头移到链表尾），时钟算法使用环形链表，再使用一个指针指向最老的页面，避免了移动页面的开销；
- **最近未使用算法**NRU（Not Recently Used）：检查访问位R、修改位M，优先置换R=M=0，其次是（R=0, M=1）；
- **最近最少使用算法**LRU（Least Recently Used）：置换出未使用时间最长的一页；实现方式：维护时间戳，或者维护一个所有页面的链表。当一个页面被访问时，将这个页面移到链表表头。这样就能保证链表表尾的页面是最近最久未访问的。
- **最不经常使用算法**LFU（Least Frequently Used）：置换出访问次数最少的页面


# 计算机网络
## 什么是三次握手 (three-way handshake)？
- 第一次握手：Client将SYN置1，随机产生一个初始序列号seq发送给Server，进入SYN_SENT状态；
- 第二次握手：Server收到Client的SYN=1之后，知道客户端请求建立连接，将自己的SYN置1，ACK置1，产生一个acknowledge number=sequence number+1，并随机产生一个自己的初始序列号，发送给客户端；进入SYN_RCVD状态；
- 第三次握手：客户端检查acknowledge number是否为序列号+1，ACK是否为1，检查正确之后将自己的ACK置为1，产生一个acknowledge number=服务器发的序列号+1，发送给服务器；进入ESTABLISHED状态；服务器检查ACK为1和acknowledge number为序列号+1之后，也进入ESTABLISHED状态；完成三次握手，连接建立。

## 什么是四次挥手？
- 第一次挥手：Client将FIN置为1，发送一个序列号seq给Server；进入FIN_WAIT_1状态
- 第二次挥手：Server收到FIN之后，发送一个ACK=1，acknowledge number=收到的序列号+1；进入CLOSE_WAIT状态。此时客户端已经没有要发送的数据了，但仍可以接受服务器发来的数据
- 第三次挥手：Server将FIN置1，发送一个序列号给Client；进入LAST_ACK状态
- 第四次挥手：Client收到服务器的FIN后，进入TIME_WAIT状态；接着将ACK置1，发送一个acknowledge number=序列号+1给服务器；服务器收到后，确认acknowledge number后，变为CLOSED状态，不再向客户端发送数据。客户端等待2*MSL（报文段最长寿命）时间后，也进入CLOSED状态。完成四次挥手

## TCP与UDP
- TCP是面向连接的，UDP是无连接的
- TCP是可靠的，UDP不可靠
- TCP只支持点对点通信，UDP支持一对一、一对多、多对一、多对多
- TCP是面向字节流的，UDP是面向报文的
- TCP有拥塞控制机制，UDP没有。网络出现的拥塞不会使源主机的发送速率降低，这对某些实时应用是很重要的，比如媒体通信，游戏
- TCP首部开销（20字节）比UDP首部开销（8字节）要大
- UDP 的主机不需要维持复杂的连接状态表


## 拥塞控制
拥塞控制主要由四个算法组成：慢启动（Slow Start）、拥塞避免（Congestion voidance）、快重传 （Fast Retransmit）、快恢复（Fast Recovery）
1. 慢启动：刚开始发送数据时，先把拥塞窗口（congestion window）设置为一个最大报文段MSS的数值，每收到一个新的确认报文之后，就把拥塞窗口加1个MSS。这样每经过一个传输轮次（或者说是每经过一个往返时间RTT），拥塞窗口的大小就会加倍
2. 拥塞避免：当拥塞窗口的大小达到慢开始门限(slow start threshold)时，开始执行拥塞避免算法，拥塞窗口大小不再指数增加，而是线性增加，即每经过一个传输轮次只增加1MSS.
3. 快重传：快重传要求接收方在收到一个失序的报文段后就立即发出重复确认（为的是使发送方及早知道有报文段没有到达对方）而不要等到自己发送数据时捎带确认。快重传算法规定，发送方只要一连收到三个重复确认就应当立即重传对方尚未收到的报文段，而不必继续等待设置的重传计时器时间到期。
4. 快恢复：当发送方连续收到三个重复确认时，就把慢开始门限减半，然后执行拥塞避免算法。不执行慢开始算法的原因：因为如果网络出现拥塞的话就不会收到好几个重复的确认，所以发送方认为现在网络可能没有出现拥塞。
   也有的快重传是把开始时的拥塞窗口cwnd值再增大一点，即等于 `ssthresh + 3*MSS` 。这样做的理由是：既然发送方收到三个重复的确认，就表明有三个分组已经离开了网络。这三个分组不再消耗网络的资源而是停留在接收方的缓存中。可见现在网络中减少了三个分组。因此可以适当把拥塞窗口扩大些。

## TCP如何保证传输的可靠性
- 数据包校验
- 对失序数据包重新排序（TCP报文具有序列号）
- 丢弃重复数据
- 应答机制：接收方收到数据之后，会发送一个确认（通常延迟几分之一秒）；
- 超时重发：发送方发出数据之后，启动一个定时器，超时未收到接收方的确认，则重新发送这个数据；
- 流量控制：确保接收端能够接收发送方的数据而不会缓冲区溢出
# Redis
## Redis的数据类型
## Redis数据持久化
## Redis实现消息队列

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

## 索引有哪几种？
MySQL的索引可以分为以下几类：

1. 普通索引和唯一索引
   普通索引是MySQL中的基本索引类型，允许在定义索引的列中插入重复值和空值。
   唯一索引要求索引列的值必须唯一，但允许有空值。如果是组合索引，则列值的组合必须唯一。
   主键索引是一种特殊的唯一索引，不允许有空值。
2. 单列索引和组合索引
   单列索引即一个索引只包含单个列，一个表可以有多个单列索引。
   组合索引是指在表的多个字段组合上创建的索引，只有在查询条件中使用了这些字段的左边字段时，索引才会被使用。使用组合索引时遵循最左前缀集合。
3. 全文索引
   全文索引类型为FULLTEXT，在定义索引的列上支持值的全文查找，允许在这些索引列中插入重复值和空值。全文索引可以在CHAR、VARCHAR或者TEXT类型的列上创建。MySQL中只有MyISAM存储引擎支持全文索引。
4. 空间索引
   空间索引是对空间数据类型的字段建立的索引，MySQL中的空间数据类型有4种，分别是GEOMETRY、POINT、LINESTRING和POLYGON。MySQL使用SPATIAL关键字进行扩展，使得能够用创建正规索引类似的语法创建空间索引。创建空间索引的列，必须将其声明为NOT NULL，空间索引只能在存储引擎为MyISAM的表中创建。

## MySQL的Hash索引和B树索引有什么区别？
hash索引底层就是hash表，进行查找时，调用一次hash函数就可以获取到相应的键值，之后进行回表查询获得实际数据。B+树底层实现是多路平衡查找树，对于每一次的查询都是从根节点出发，查找到叶子节点方可以获得所查键值，然后根据查询判断是否需要回表查询数据。它们有以下的不同：
- hash索引进行等值查询更快(一般情况下)，但是却无法进行范围查询。因为在hash索引中经过hash函数建立索引之后，索引的顺序与原顺序无法保持一致，不能支持范围查询。而B+树的的所有节点皆遵循(左节点小于父节点，右节点大于父节点，多叉树也类似)，天然支持范围。
- hash索引不支持使用索引进行排序，原理同上。
- hash索引不支持模糊查询以及多列索引的最左前缀匹配，原理也是因为hash函数的不可预测。
- hash索引任何时候都避免不了回表查询数据，而B+树在符合某些条件(聚簇索引，覆盖索引等)的时候可以只通过索引完成查询。
- hash索引虽然在等值查询上较快，但是不稳定，性能不可预测，当某个键值存在大量重复的时候，发生hash碰撞，此时效率可能极差。而B+树的查询效率比较稳定，对于所有的查询都是从根节点到叶子节点，且树的高度较低。
因此，在大多数情况下，直接选择B+树索引可以获得稳定且较好的查询速度。而不需要使用hash索引。

## 聚簇索引和非聚簇索引有什么区别？
在InnoDB存储引擎中，可以将B+树索引分为聚簇索引和辅助索引（非聚簇索引）。无论是何种索引，每个页的大小都为16KB，且不能更改。

聚簇索引是根据主键创建的一棵B+树，聚簇索引的叶子节点存放了表中的所有记录。辅助索引是根据索引键创建的一棵B+树，与聚簇索引不同的是，其叶子节点仅存放索引键值，以及该索引键值指向的主键。也就是说，如果通过辅助索引来查找数据，那么当找到辅助索引的叶子节点后，很有可能还需要根据主键值查找聚簇索引来得到数据，这种查找方式又被称为书签查找。因为辅助索引不包含行记录的所有数据，这就意味着每页可以存放更多的键值，因此其高度一般都要小于聚簇索引。

## MySQL的两种存储引擎 InnoDB 和 MyISAM 的区别？
- InnoDB支持事务，可以进行Commit和Rollback；
- MyISAM 只支持表级锁，而 InnoDB 还支持行级锁，提高了并发操作的性能；
- InnoDB 支持外键；
- MyISAM 崩溃后发生损坏的概率比 InnoDB 高很多，而且恢复的速度也更慢；
- MyISAM 支持压缩表和空间数据索引，InnoDB需要更多的内存和存储；
- InnoDB 支持在线热备份


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
