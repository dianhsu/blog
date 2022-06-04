---
title: 介绍一个查看Codeforces GYM的代码的工具
date: 2022-06-04 23:25:17
categories: 工具
tags:
    - 工具
    - Codeforces
index_img: https://cdn.dianhsu.top/img/2022-06-04-23-48-18.png
---

# 简介
因为Codeforces GYM要求黄名(rating >= 2100) 或者 紫名(rating >= 1900)并且打过30场计分的比赛才可以查看公开的代码，为了方便群友查看GYM中的代码，故写了这个小工具。

# 前置工具
本工具需要安装浏览器用户脚本管理器，例如： [暴力猴](https://chrome.google.com/webstore/detail/violent-monkey/jinjaccalgkegednnccohejagnlnfdag)

上面链接是通过Google商店下载，如果进不去，可以通过GitHub下载 [暴力猴](https://github.com/violentmonkey/violentmonkey/releases)

# 安装过程

安装好了暴力猴之后，打开暴力猴，点击`+`新建一个脚本

![暴力猴](https://cdn.dianhsu.top/img/2022-06-04-23-37-06.png)

将下面脚本代码粘贴到编辑器内。

```javascript
// ==UserScript==
// @name        GYM code view - codeforces.com
// @namespace   Violentmonkey Scripts
// @match       https://codeforces.com/gym/*/status
// @grant       MIT
// @version     1.0
// @author      dianhsu
// @run-at      document-idle
// @description 2022/6/4 15:41:09
// ==/UserScript==

function init(){
  let items = document.querySelector('.status-frame-datatable').querySelectorAll('tr')
  let reg = /\d+/g;
  let contestId = window.location.pathname.match(reg);
  items.forEach(function(item){
    if(item.className === 'first-row'){
      let th = document.createElement('th');
      th.class = 'top right';
      th.append("View");
      item.append(th);
    }else{
      let submissionId = item.dataset.submissionId;
      let td = document.createElement('td');
      let a = document.createElement('a');
      a.append('code');
      a.title = 'code';
      a.target = '_blank';
      a.href = `https://cf.dianhsu.com/gym/${contestId}/submission/${submissionId}`;
      td.append(a);
      item.append(td);
    }
  });
};
init();
```
如下图所示

![暴力猴中的脚本页面](https://cdn.dianhsu.top/img/2022-06-04-23-39-20.png)

最后点击右上角保存即可。

# 如何获取代码

打开一场GYM比赛的`status`页面，列表中多了一列`Views`，如下图所示。

![GYM中的Status页面](https://cdn.dianhsu.top/img/2022-06-04-23-42-20.png)

点击`code`链接，就会在新标签页中显示出代码。

![跳转到了贴代码的网站](https://cdn.dianhsu.top/img/2022-06-04-23-44-21.png)

# 其他的一些说明

1. 目前还没做代码高亮，后续有想法
2. 有些比赛需要通过邀请链接才能进去查看比赛。这个逻辑后台已经写了，前端没想好放在哪。
3. 后端源码 [cf-code](https://github.com/dianhsu/cf-code)
