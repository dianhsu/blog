# !/bin/env python3
import os
import sys
import subprocess
from multiprocessing import Pool


ignore_prefix = ["./.github/", "./.git/", "./markdown-renderer/"]
ignore_suffix = []
required_prefix = []
required_suffix = ['.md']

# 检查文件是不是满足忽略条件的


def check(path: str):
    for it in ignore_prefix:
        if path.startswith(it):
            return False
    if len(required_prefix) > 0:
        for it in required_prefix:
            if path.startswith(it):
                return True
        return False
    if os.path.isfile(path):
        for it in ignore_suffix:
            if path.endswith(it):
                return False
        if len(required_suffix) > 0:
            for it in required_suffix:
                if path.endswith(it):
                    return True
            return False
    return True


arr = []


def dfs(dirname: str):
    # 遍历文件夹，找到渲染的markdown文件
    for it in os.listdir(dirname):
        path = os.path.join(dirname, it)
        if not check(path):
            continue
        if os.path.isfile(path):
            arr.append(path)
        elif os.path.isdir(path):
            dfs(path)


def convert(path: str):
    # 调用外部渲染工具，渲染一个HTML页面
    subprocess.run(["markdown-renderer", "-i", path])


if __name__ == '__main__':
    pool = Pool()
    dfs('.')
    pool.map(convert, arr)
    pool.close()
    pool.join()
