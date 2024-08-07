---
title: 数据库
math: true
date: 2022-08-28 14:28:40
categories:
    - 面试
tags:
    - 面试
    - 八股文
    - 数据库
index_img: https://cdn.dianhsu.com/img/2023-06-07-17-56-39.jpg
---

# 数据库的三范式是什么？
- 第一范式：强调的是列的原子性，即数据库表的每一列都是不可分割的原子数据项。
- 第二范式：要求实体的属性完全依赖于主关键字。所谓完全 依赖是指不能存在仅依赖主关键字一部分的属性。
- 第三范式：任何非主属性不依赖于其它非主属性。

# MySQL 支持哪些存储引擎?
MySQL 支持多种存储引擎,比如 InnoDB,MyISAM,Memory,Archive 等等。在大多数的情况下,直接选择使用 InnoDB 引擎都是最合适的,InnoDB 也是 MySQL 的默认存储引擎。

MyISAM 和 InnoDB 的区别有哪些：
- InnoDB 支持事务，MyISAM 不支持
- InnoDB 支持外键，而 MyISAM 不支持
- InnoDB 是聚集索引，数据文件是和索引绑在一起的，必须要有主键，通过主键索引效率很高；
  MyISAM 是非聚集索引，数据文件是分离的，索引保存的是数据文件的指针，主键索引和辅助索引是独立的。
- Innodb 不支持全文索引，而 MyISAM 支持全文索引，查询效率上 MyISAM 要高；
- InnoDB 不保存表的具体行数，MyISAM 用一个变量保存了整个表的行数。
- MyISAM 采用表级锁(table-level locking)；InnoDB 支持行级锁(row-level locking)和表级锁，默认为行级锁。

# 超键、候选键、主键、外键分别是什么？
- 超键：在关系中能唯一标识元组的属性集称为关系模式的超键。一个属性可以为作为一个超键，多个属性组合在一起也可以作为一个超键。超键包含候选键和主键。
- 候选键：是最小超键，即没有冗余元素的超键。
- 主键：数据库表中对储存数据对象予以唯一和完整标识的数据列或属性的组合。一个数据列只能有一个主键，且主键的取值不能缺失，即不能为空值（Null）。
- 外键：在一个表中存在的另一个表的主键称此表的外键。

# SQL 约束有哪几种？
- NOT NULL: 用于控制字段的内容一定不能为空（NULL）。
- UNIQUE: 控件字段内容不能重复，一个表允许有多个 Unique 约束。
- PRIMARY KEY: 也是用于控件字段内容不能重复，但它在一个表只允许出现一个。
- FOREIGN KEY: 用于预防破坏表之间连接的动作，也能防止非法数据插入外键列，因为它必须是它指向的那个表中的值之一。
- CHECK: 用于控制字段的值范围。

# MySQL 中的 varchar 和 char 有什么区别？
char 是一个定长字段,假如申请了`char(10)`的空间,那么无论实际存储多少内容.该字段都占用 10 个字符,而 varchar 是变长的,也就是说申请的只是最大长度,占用的空间为实际字符长度+1,最后一个字符存储使用了多长的空间。
在检索效率上来讲，char > varchar，因此在使用中，如果确定某个字段的值的长度，可以使用char，否则应该尽量使用varchar，例如存储用户MD5加密之后的密码，应该使用char。

# MySQL中in和exists区别
MySQL中的in语句是把外表和内表做hash连接，而exists语句是对外表做loop循环，每次loop循环再对内表进行查询。一直大家都认为exists比in语句的效率更高，而这个说法是不准确的。这个是要区分环境的。

如果查询的两个表大小相当，那么用in和exists差别不大。如果两个表中一个较小，一个较大，则子查询表大的用exists，子查询表小的用in。
`not in` 和 `not exists`：如果查询语句使用了`not in`，那么内外表都进行全表扫描，没有用到索引；而`not exists`的子查询依然能从用到表上的索引。所以无论哪个表大，用`not exists`都比`not in`要快。

# drop、delete与truncate的区别

|          | Delete                                 | Truncate                     | Drop                                                 |
| -------- | -------------------------------------- | ---------------------------- | ---------------------------------------------------- |
| 类型     | 属于DML                                | 属于DDL                      | 属于DDL                                              |
| 回滚     | 可回滚                                 | 不可回滚                     | 不可回滚                                             |
| 删除内容 | 表结构还在，删除表的全部或者一部分数据 | 表结构还在，删除表的所有数据 | 从数据库中删除表，所有的数据行，索引和权限也会被删除 |
| 删除速度 | 删除速度慢，需要逐行删除               | 删除速度快                   | 删除速度快                                           |

# 什么是存储过程？有哪些优缺点？
储存过程是一些预编译的SQL语句。
1. 更加直白的理解：存储过程可以说是一个记录集，它是由一些T-SQL语句组成的代码块，这些T-SQL语句代码就像一个方法一样实现一些功能（对单表或多表的增删），然后再给这个代码块取一个名字，在用到这个功能的时候调用他就行了。
2. 存储过程是一个预编译的代码块，执行效率比较高，一个存储过程代替大量T-SQL语句，可以降低网络通信量，提高通信效率，可以一定程度上确保数据安全。

# MySQL执行查询的过程
1. 客户端通过TCP连接发送连接请求到MySQL连接器，连接器会对该请求进行权限验证及连接资源分配
2. 查缓存。（当判断缓存是否命中时，MySQL不会进行解析查询语句，而是直接使用SQL语句和客户端发送过来的其他原始信息。所以，任何字符上的不同，例如空格、注解等都会导致缓存的不命中。）
3. 语法分析（SQL语法是否写错了）。如何把语句给到预处理器，检查数据表和数据列是否存在，解析别名看是否存在歧义。
4. 优化。是否使用索引，生成执行计划。
5. 交给执行器，将数据保存到结果集中，同时会逐步将数据缓存到查询缓存中，最红将结果集返回给客户端。

![MySQL执行查询的过程](https://cdn.dianhsu.com/img/2022-08-14-20-46-50.png)

更新语句执行会复杂一点，需要检查表是否含排他锁，写binlog，刷盘，是否执行commit。

# 事务
## 什么是数据库事务
事务时一个不可分割的数据库操作序列，也是数据库并发控制的基本单位，其执行结果必须是数据库从一种一致性状态变到另一种一致性状态。事务是逻辑上的一组操作，要么都执行，要么都不执行。

事务最经典的例子就是转账了。

假如小明要给小红转账1000元，这个转账就会涉及到两个关键操作就是：将小明的余额减少1000元，将小红的余额增加1000元。万一在这两个操作之间突然出现错误比如银行系统崩溃，导致小明的余额减少但是小红的余额没有增加，这样就不对了。事务就是保证这两个关键操作要么都成功，要么都要失败。

## 介绍一下事务的四个特征
事务就是一组原子性的操作，这些操作要么全部发生，要么全部不发生。事务把数据库从一种一致性状态转换到另外一种一致性状态。

- 原子性。事务是数据库的逻辑工作单位，事务中包含的个操作要么都做、要么都不做。
- 一致性。事务执行的结果必须是使数据库从一个一致性状态转变成另外一个一致性状态。因此当数据库中只包含成功事务提交的结果时，就说明数据库处于一致性状态。如果数据库系统运行时发生故障，有些事务尚未完成就被迫中断，这些未完成事务对数据库所做的修改有一部分已写入物理数据库，这时数据库就处于一种不正确的状态，或者说是不一致状态。
- 隔离性。一个事务的执行不能被其他事务干扰。即一个事务内部的操作及使用的数据对其他并发事务时隔离的，并发执行的各个事务之间不能相互干扰。
- 持久性。指一个事务一旦提交，它对数据库中的数据的改变就应该是永久性的。接下来其他的操作或故障不应该对其执行结果有任何影响。

## 说一下MySQL的四种隔离级别
- READ UNCOMMITTED （读未提交）
  在该隔离级别，所有事务都可以看到其他未提交事务的执行结果。本隔离级别很少用于实际应用，因为它的性能也不比其他的级别好多少。读取未提交的数据，也称之为脏读（Dirty Read）。
- READ COMMITTED （读已提交）
  这是大多数数据库系统的默认隔离级别（但不是MySQL默认的）。它满足了隔离的简单定义：一个事务只能看到已经提交事务所做的改变，这种隔离级别也支持所谓的不可重复读，因为同一事务的其他实例在该实例处理其间可能会有新的commit，所以同一select可能返回不同的结果。
- REPEATABLE READ （可重复读）
  这是MySQL的默认事务隔离级别，它确保同一事务的多个实例在并发读取数据时，会看到同样的数据行。不过理论上，这会导致另一个棘手的问题：幻读（Phantom Read）。
- SERIALIZABLE （串行化）
  通过强制事务排序，使之不可能相互冲突，从而解决幻读问题。简言之，它是每个读的数据行上加上共享锁。在这个级别，可能导致大量的超时现象和锁竞争。

| 隔离级别        | 脏读 | 不可重复读 | 幻读 |
| --------------- | ---- | ---------- | ---- |
| READ UNCOMMITTED | ✅    | ✅          | ✅    |
| READ COMMITTED   | ❌    | ✅          | ✅    |
| REPEATABLE READ | ❌    | ❌          | ✅    |
| SERIALIZABLE    | ❌    | ❌          | ❌    |

MySQL 默认采用的 REPEATABLE READ 隔离级别，Oracle默认采用的 READ COMMITTED。
事务隔离机制的实现基于锁机制和并发调度。其中并发调度使用的是MVVC（多版本并发控制），通过保存修改的旧版本信息来支持并发一致性读和回滚操作。
因为隔离级别越低，事务请求的锁越少，所以大部分数据库系统的隔离级别都是READ COMMITTED（读取提交内容），但是你要知道的是InnoDB存储引擎默认使用REPEATABLE READ（可重复读）并不会有任何性能损失。
InnoDB存储引擎在分布式事务的情况下一般会用到SERIALIZABLE（可串行化）隔离级别。

## 什么是脏读？幻读？不可重复读？
- 脏读：事务A读取了事务B更新的数据，然后B回滚操作，那么A读取到的数据是脏数据。
- 不可重复读：事务A多次读取同一数据，事务B在事务A多次读取的过程中，对数据做了更新并提交，导致事务A多次读取同一数据时，结果不一致。
- 幻读：系统管理员A将数据库中所有学生的成绩从具体分数改成ABCDE等级，但是系统管理员B就在这个时候插入一条具体分数的记录，当系统管理员A改结束后发现还有一条记录没有改过来，就像发生幻觉一样，这就叫幻读。

不可重复读侧重于修改，幻读侧重于新增和删除（多了或者少了行），脏读诗一个书屋回滚影响另外一个事务。

## 事务的实现原理
事务是基于重做日志文件（redo log）和回滚日志（undo log）实现的。

每提交一个事务必须先将该事务的所有日志写入到重做日志文件进行持久化，数据库就可以通过重做日志来保证事务的原子性和持久性。

每当有修改事务时，还会产生undo log，如果需要回滚，则根据undo log的反向语句进行逻辑操作，比如insert一条记录就delete一条记录，undo log主要是实现数据库的一致性。
## MySQL日志介绍一下
InnoDB事务日志包括redo log和undo log。
undo log 指事务开始之前，在操作任何数据之前，需要将需要操作的数据备份到一个地方。redo log指事务中操作的任何数据，将最新的数据备份到一个地方。

事务日志的目的：实例或者介质失败，事务日志文件就能派上用场。

**redo log**
redo log不是随着事务的提交才写入的，而是在实物的执行过程中，就开始写入redo log中。具体的落盘策略可以进行配置。放置在发生故障的时间点，尚有脏页未写入磁盘，在重启MySQL服务的时候，根据redo log进行重做，从而达到事务的未入磁盘数据进行持久化这一特性。redo log是为了实现事务的持久化而出现的产物。

![Redo log](https://cdn.dianhsu.com/img/2022-08-14-22-16-23.png)

**undo log**
undo log用来回滚行记录到某个版本。事务未提交之前，undo 保存了未提交之前的版本数据，undo log中的数据可以作数据的旧版本快照供其他并发事务进行快照读。是为了实现事务的原子性而出现的产物，在MySQL InnoDB存储引擎中用来实现多版本并发控制。

![Undo log](https://cdn.dianhsu.com/img/2022-08-14-22-21-12.png)

## 什么是MySQL的binlog
MySQL的binlog是记录所有数据库表结构变更（例如CREATE、ALTER TABLE）以及表数据修改（INSERT、UPDATE和DELETE）的二进制日志。binlog不会记录SELECT和SHOW这类操作，因为这类操作对数据本身没有修改，但你可以通过查询通用日志来查看MySQL执行过的所有语句。

MySQL的binlog以事件形式记录，还包含语句执行的消耗的时间，MySQL的二进制日志是事务安全型的。binlog的主要目的是复制和恢复。

binlog有三种格式，各有优缺点：
- statement: 基于SQL语句的模式，某些语句和函数如UUID、LOAD DATA INFILE等在复制过程可能导致数据不一致甚至出错。
- row: 基于行的模式，记录的是行的变化，很安全。但是binlog会比其他两种模式大很多，在一些大表中清楚大量数据时在binlog中会生成很多条语句，可能导致从库延迟变大。
- mixed: 混合模式，根据语句来选择是statement还是row。

## 隔离级别是如何实现的
事务的隔离机制主要是依赖锁机制和MVCC（多版本并发控制）实现的，读已提交和可重复读可以通过MVCC实现，串行化可以通过锁机制实现。

## 什么是MVCC
MVCC，即多版本并发控制。MVCC的实现，是通过保存数据在某个时间点的快照来实现的。根据事务的开始的时间不同，每个事物对同一张表，同一个时刻看到的数据可能是不同的。

## MVCC的实现原理
对于InnoDB，聚簇索引记录中包含3个隐藏的列：
- ROW ID: 隐藏的自增ID，如果表没有主键，InnoDB会自动按照ROW ID产生一个聚集索引数。
- 事务ID: 记录最后一次修改该记录的事务ID。
- 回滚指针: 指向这条记录的上一个版本。

我们拿上面的例子，对应解释下MVCC的实现原理，如下图：
![MVCC实现原理](https://cdn.dianhsu.com/img/2022-08-14-22-49-51.png)
如图，首先insert语句向表t1中插入了一条数据，a字段为1，b字段为1，ROW ID也为1，事务ID假设为1，回滚指针假设为NULL。当执行update t1 set b=666 where a=1时，大致步骤如下：
- 数据库会先对满足a=1的行加排他锁；
- 然后将原纪录复制到undo表空间中；
- 修改b字段的值为666，修改事务ID为2；
- 并通过隐藏的回滚指针指向undo log中的历史记录；
- 事务提交，释放前面对满足a=1的行所加的排他锁；

因此可以总结出MVCC实现的原理大致是：
InnoDB每一行数据都有一个隐藏的回滚指针，用于指向该行修改前的最后一个历史版本，这个历史版本存放在undo log中。如果要执行更新操作，会将原纪录放入undo log中，并通过隐藏的回滚指针指向undo log中的原纪录。其它事务此时需要查询时，就是查询undo log中这行数据的最后一个历史版本。

MVCC最大的好处就是读不加锁，读写不冲突，极大地增加了MySQL的并发性。通过MVCC，保证了事务ACID中的I（隔离性）特性。

# 锁
## 为什么要加锁?
当多个用户并发地存取数据时，在数据库中就会产生多个事务同时存取同一数据的情况。若对并发的操作不加控制就可能会读取和存储不正常的数据，破坏数据库的一致性。

在多用户环境下保证数据库的完整性和一致性。

## 按照锁的粒度来分类，数据库锁有哪些
在关系型数据库中，可以按照锁的粒度把数据库锁分为行级锁（InnoDB引擎）、表级锁（MyISAM引擎）和页级锁（BDB引擎）。

**行级锁**
- 行级锁是MySQL中锁定粒度最细的一种锁，表示只针对当前操作的行进行加锁。行级锁能大大减少数据库操作的冲突。其加锁粒度最小，但加锁的开销也最大。行级锁分为共享锁和排他锁。
- 开销大，加锁慢；会出现死锁；锁定粒度最小，发生锁冲突的概率最低，并发度也最高。

**表级锁**
- 表级锁是MySQL中锁定粒度最大的一种锁，表示对当前操作的整张表加锁，它实现简单，资源消耗较少，被大部分MySQL引擎支持。最常使用的MyISAM与InnoDB都支持表级锁定。表级锁定分为表共享读锁（共享锁）与表独占写锁（排他锁）。
- 开销小，加锁快；不会出现死锁；锁定粒度大，发出锁冲突的概率最高，并发度最低。

**页级锁**
- 页级锁是MySQL中锁定粒度介于行级锁和表级锁中间的一种锁。表级锁速度快，但冲突多，行级锁冲突少，但速度慢。所以取了折中的页级，一次锁定相邻的一组记录，BDB支持页级锁
- 开销和加锁时间介于表级锁和行级锁中间；会出现死锁；锁定粒度介于表级锁和行级锁中间，并发度一般。

**MyISAM和InnoDB存储引擎使用的锁**
- MyISAM采用的是表级锁（table-level locking）。
- InnoDB支持行级锁和表级锁，默认为行级锁。

## 从锁的类别上面划分MySQL都有哪些锁
从锁的类别上面来讲，有共享锁和排他锁
- 共享锁：又叫做读锁。当用户要进行数据的读取时，对数据加上共享锁。共享锁可以同时加上多个。
- 排他锁：又叫做写锁。当用户要进行数据的写入时，对数据加上排他锁。排他锁只可以加上一个，它和其他的排他锁、共享锁都互斥。

## 数据库的乐观锁和悲观锁
数据库管理系统（DBMS）中的并发控制的任务是确保在多个事务同时存取数据库中同一数据时不破坏事务的隔离性和统一性以及数据库的统一性。乐观并发控制（乐观锁）和悲观并发控制（悲观锁）是并发控制主要采用的技术手段。

- 悲观锁：假定会发生并发冲突，屏蔽一切可能违反数据完整性的操作。在查询完数据的时候就把事务锁起来，直到提交事务。实现方式：使用数据库的锁机制
- 乐观锁：假设不会发生并发冲突，只在提交操作时检查是否违反数据的完整性。在修改数据的时候，把事务锁起来，通过version的方式来进行锁定。实现方式：一般会使用版本号机制或者CAS算法实现。

**两种锁的使用场景**

从上面对两种锁的介绍，我们知道两种锁各有优缺点，不可认为一种好于另一种，像乐观锁适用于写比较少的情况，即冲突真的很少发生，这样可以省去锁的开销，加大了系统的整个吞吐量。

但如果是多写的情况，一般会经常产生冲突，这就会导致上层应用会不断进行retry，这样反倒是降低了性能，所以一般多写的场景下用悲观锁多一些。

## InnoDB引擎的行锁是怎么实现的
InnoDB是基于索引来完成行锁
例：`select * from tab_with_index where id = 1 for update;`
`for update`可以根据条件来完成行锁锁定，并且`id`是有索引键的列，如果`id`不是索引键那么InnoDB将完成表锁，并发将无从谈起。

## 什么是死锁，怎么解决

死锁是两个或者多个事务在同一个资源上相互占用，并请求对方锁定的资源，从而导致恶性循环的现象

常见的解决死锁的方法
- 如果不同程序会并发存取多个表，尽量约定以相同的顺序访问表，可以大大降低死锁机会。
- 在同一个事务中，尽可能做到一次锁定所需要的所有资源，减少死锁产生概率。
- 对于非常容易产生死锁的业务部分，可以尝试使用升级锁定颗粒度，通过表级锁定减少死锁产生的概率。

如果业务处理不好可以用分布式事务锁或者使用乐观锁

## 隔离级别与锁的关系
在 Read Uncommitted级别下，读取数据不需要加共享锁，这样就不会跟被修改的数据上的排他锁冲突。
在 Read Committed级别下，读操作需要加共享锁，但是语句执行完之后释放共享锁。
在 Repeatable Read级别下，读操作需要加共享锁，但是在事务提交之前并不释放共享锁，这就是必须等待事务执行完毕之后才释放共享锁。
在Serializable级别下，因为该级别锁定整个范围的键，并一直持有锁，直到事务完成。

## 优化锁方面的建议
- 使用较低的隔离级别
- 设计索引，尽量使用索引去访问数据，加锁更加准确，从而减少锁冲突
- 选择合理的事务大小，给记录显示加锁时，最好一次性请求足够级别的所。例如，修改数据的话，最好申请排他锁，而不是先申请共享锁，修改时再申请排他锁，这样会导致死锁
- 不同的程序访问一组表的时候，应尽量约定一个相同的顺序访问各个表，对于一个表而言，尽可能的固定顺序访问表中的行，这样会大大减少死锁的机会。
- 尽量使用相等的条件访问数据，这样可以避免间隙锁对并发插入的影响。
- 不要申请超过实际需要的锁级别
- 数据查询的时候不是必要，不要使用加锁。MySQL的MVCC可以实现事务的查询而不用加锁，优化事务性能：MVCC只在 读已提交 和 可重复读 两种隔离级别
- 对于特定的事务，可以使用表锁来提高处理速度或者减少死锁的可能。

# 分库分表
## 为什么要分库分表
**分表**
比如你单表都几千万数据了，你确定你能扛得住吗？绝对不行，单表数据量太大，会极大影响你的sql执行的性能，到了后面你的sql可能就跑的很慢了。一般来说，就以我的经验来看，单表到几百万的时候，性能就会相对差一些了，你就得分表了。
分表就是把一个表的数据放到多个表中，然后查询的时候你就查一个表。比如按照用户id来分表，将一个用户的数据就放在一个表中。然后操作的时候你对一个用户就操作那个表就好了。这样可以控制每个表的数据量在可控的范围内，比如每个表就固定200万以内。

**分库**
分库就是你的一个库一般我们经验而言，最多支撑到并发2000，一定要扩容了，而且一个健康的单库并发值你最好保持在每秒1000左右，不要太大。那么你就可以通过将一个库的数据拆分到多个库当中，访问的时候就访问一个库就好了。

这就是所谓的分库分表。

# 参考
[^1]: [MySQL八股文连环45问（背诵版）](https://zhuanlan.zhihu.com/p/403656116)
[^2]: [MySQL八股文背诵版](https://www.nowcoder.com/discuss/985275)