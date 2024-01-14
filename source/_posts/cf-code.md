---
title: 介绍一个查看Codeforces GYM的代码的工具
date: 2022-06-04 23:25:17
categories: 工具
tags:
    - 工具
    - Codeforces
index_img: https://cdn.dianhsu.com/img/2023-06-07-18-05-28.jpg-400x250
---

# 简介
因为Codeforces GYM要求黄名(rating >= 2100) 或者 紫名(rating >= 1900)并且打过30场计分的比赛才可以查看公开的代码，为了方便群友查看GYM中的代码，故写了这个小工具。

# 前置工具
本工具需要安装浏览器用户脚本管理器，例如： [暴力猴](https://chrome.google.com/webstore/detail/violent-monkey/jinjaccalgkegednnccohejagnlnfdag)

上面链接是通过Google商店下载，如果进不去，可以通过GitHub下载 [暴力猴](https://github.com/violentmonkey/violentmonkey/releases)

# 安装过程

访问[脚本安装链接](https://raw.githubusercontent.com/dianhsu/cf-code/main/script.user.js)，点击`确认安装`即可。


# 如何获取代码

打开一场GYM比赛的`status`页面，列表中第一列代码编号变成了可以点击的链接啦，如下图所示。
![安装插件之后](https://cdn.dianhsu.com/img/2022-06-06-12-52-37.png)

对比一下安装插件之前的页面。

![安装插件之前](https://cdn.dianhsu.com/img/2022-06-06-12-51-50.png)

点击一下代码编号的链接，就跳转到了贴代码的网站。

![跳转到了贴代码的网站](https://cdn.dianhsu.com/img/2022-06-04-23-44-21.png)

PS：原本个人submission里面的无法查看的代码也可以查看啦


# 其他的一些说明

1. 目前还没做代码高亮，后续有想法。 PS：已实现
2. 有些比赛需要通过邀请链接才能进去查看比赛。这个逻辑后台已经写了，前端没想好放在哪。
3. 插件和后端源码 [cf-code](https://github.com/dianhsu/cf-code)

