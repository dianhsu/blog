#!/bin/env python3
import os
import sys


ignore_prefix = ["./algorithm/oj/", "./.github/", "./.git/", "./markdown-renderer/"]
ignore_suffix = []
required_prefix = []
required_suffix = ['.md']


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


def handle(file_path: str):
    print(file_path)


def dfs(dir: str):
    for it in os.listdir(dir):
        ignore = False
        path = os.path.join(dir, it)
        if not check(path):
            continue
        # print("debug", path)
        if os.path.isfile(path):
            handle(path)
        elif os.path.isdir(path):
            dfs(path)


def main():
    dfs(".")


if __name__ == '__main__':
    main()
