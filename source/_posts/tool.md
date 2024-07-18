---
title: 工具
date: 2022-05-10 19:09:43
tags:
    - 工具
categories: 工具
index_img: https://cdn.dianhsu.com/img/2023-06-07-18-11-25.jpeg
---

# 工具

## Competitive Server
> 需要安装flask
支持[Competitive Companion](https://github.com/jmerle/competitive-companion)吊起，生成文件夹和测试文件

然后可以用[cf-tool(rev.dianhsu)](https://github.com/dianhsu/cf-tool)在该目录下进行编译和运行

备注：因为生成的文件和标题相同，考虑特殊字符会导致cf-tool错误，需要在编译命令中的文件名处加上引号

```python
from flask import Flask
from flask import request

import os

app = Flask(__name__)
BASE_DIR = '.'
PORT = 10042

@app.route("/", methods=['POST'])
def handle():
    tests = request.json['tests']
    problem_dir = os.path.join(BASE_DIR, request.json['name'])
    os.makedirs(problem_dir, exist_ok=True)
    for idx, it in enumerate(tests):
        with open(os.path.join(problem_dir, f'testI{idx + 1}.txt'), 'w') as f:
            f.write(it['input'])
        with open(os.path.join(problem_dir, f'testO{idx + 1}.txt'), 'w') as f:
            f.write(it['output'])
    return ""


if __name__ == '__main__':
    app.run(port=PORT, debug=False)
```
## NeoVim配置

### 安装NeoVim
- Windows: 从[neovim github release](https://github.com/neovim/neovim/releases/)下载最新的安装包，解压之后将目录添加到PATH即可
- Linux: 可以通过包管理工具下载NeoVim，例如：`sudo apt install neovim`（Ubuntu）
- macOS: 可以通过HomeBrew工具安装NeoVim，`brew install neovim`。
### 安装包管理工具
我用的是[vim-plug](https://github.com/junegunn/vim-plug)，按照链接当中的方法，安装NeoVim的vim-plug。

### NeoVim配置文件

```vim
set hlsearch
set showmatch
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent
set number
syntax on
set noswapfile
set backspace=indent,eol,start
set smartindent

set updatetime=300

let g:formatdef_custom_cpp = '"clang-format -style={BaseOnStyle: Google, IndentWidth: 4} --verbose"'
let g:formatters_cpp = ['custom_cpp']
let c_no_curly_error = 1

call plug#begin('~/.vim/plugged')

Plug 'bfrg/vim-cpp-modern'

Plug 'neoclide/coc.nvim', {'branch': 'release'}

Plug 'jackguo380/vim-lsp-cxx-highlight'

Plug 'Chiel92/vim-autoformat'

call plug#end()

inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

inoremap <silent><expr> <cr> pumvisible() ? coc#_select_confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"
```

### C++环境配置（LSP和Formatter支持）
需要安装clangd和clang-format。
Windows可以在[https://winlibs.com/#download-release](https://winlibs.com/#download-release)这里下载带clangd和llvm环境的gcc套件。
Linux和macOS可以使用包管理工具安装环境。

## 拒绝QQ拦截外部链接

```javascript
// ==UserScript==
// @name        拒绝拦截外部链接 - qq.com
// @namespace   Violentmonkey Scripts
// @match       https://c.pc.qq.com/middlem.html
// @grant       none
// @version     1.0
// @author      dianhsu
// @description 2021/8/29 下午6:46:14
// ==/UserScript==

(function(){
  'use strict';
  
  //console.log(window.location.href)
  let searchParams = new URLSearchParams(window.location.search);
  let reqUrl = searchParams.get("pfurl");
  if(!!reqUrl){
      window.location.href = reqUrl;
  }
})();
```

## Linux

### HP Printer
配置打印机的时候，出现这个错误

```bash
CUPS server error

client-error-not-possible
```

安装`smbclient`即可解决。

## CUPS 打印机双页打印
首先安装需要的Python包
```bash
pip3 install pycups
pip3 install PyPDF2
```
执行下面的代码
```python
# !/usr/bin/env python3
import os
import tempfile
import uuid

import PyPDF2
import cups
from PyPDF2 import PdfFileReader

# 连接打印机
conn = cups.Connection()
printers = conn.getPrinters()
printer = None
for key in printers:
    printer = key
if printer is None:
    print('亲，你的打印机呢')
    exit(-1)
# 上传文件
tmp_dir = tempfile.TemporaryDirectory().name
os.makedirs(tmp_dir, exist_ok=True)
tmp_path = os.path.join(tmp_dir, f'{uuid.uuid4()}.pdf')
pdf_path = input("请输入PDF路径: ")

# 如果是奇数页文件情况，需要补充一个空白页到末尾
fin = open(pdf_path, 'rb')
pdf = PdfFileReader(fin)
page_num = pdf.getNumPages()
outputPdf = PyPDF2.PdfFileWriter()
outputPdf.appendPagesFromReader(pdf)
if page_num % 2 != 0:
    outputPdf.addBlankPage()
with open(tmp_path, 'wb') as fout:
    outputPdf.write(fout)
fin.close()
tmp_pdf = PdfFileReader(tmp_path)
page_num = tmp_pdf.getNumPages()

double_page = True
if double_page:
    # 获取奇数页码和偶数页码
    all_pages = [str(it + 1) for it in range(page_num)]
    odd_str = ','.join(all_pages[0::2])
    even_str = ','.join(all_pages[1::2])
    # 打印奇数页
    conn.printFile(printer, tmp_path, pdf_path, {'page-ranges': odd_str})
    # 去打印机把纸拿下来换一下
    test = input("请输入\"next\"打印背面: ")
    while test != "next":
        test = input("请输入\"next\"打印背面: ")
    # 从后往前打印偶数页
    conn.printFile(printer, tmp_path, pdf_path, {'outputorder': 'reverse', 'page-ranges': even_str})
else:
    # 按顺序打印全部的页码
    conn.printFile(printer, tmp_path, pdf_path, {})

```

