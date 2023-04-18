---
title: Vagrant：一款方便、快捷虚拟机管理工具
math: true
date: 2023-04-17 16:04:50
categories: 工具
tags:
    - 虚拟机
    - vagrant
index_img: https://cdn.dianhsu.com/img/2023-04-18-10-22-54.jpg
---

最近在编译OpenWrt，因为Windows下面无法交叉编译，装个虚拟机临时用一用。下载Archlinux的时候，发现一个好用的虚拟机管理工具——vagrant。vagrant主要有以下几个功能：
- 可以零配置新建一个虚拟机环境，省去了繁杂的配置过程
  ```bash
    vagrant init archlinux/archlinux # 新建一个Vagrantfile配置文件，并配置os为Archlinux
    vagrant up # 下载镜像、配置虚拟机和启动虚拟机
  ```
- 快速连接虚拟机
  ```bash
    vagrant ssh # 连接Vagrantfile管理的虚拟机
  ```
- 打包虚拟机镜像，并分发
  ```bash
    vagrant package --base "my-algorithm-virtualmachine" --output algorithm.box # 将虚拟机打包成box文件，可以托管到Vagrant cloud
  ```

vagrant提供了虚拟机创建、管理、链接和打包的功能，给虚拟机使用了提供了极大的便利。

## Vagrant的安装[^1]
Vagrant安装前，需要配置好虚拟机环境（Provider），如：VirtualBox、VMware Workspace、QEMU等，这里用的是VirtualBox。在Windows下使用VirtualBox的时候，需要关掉Hyper-V。Windows 10可以在Powershell中使用以下命令关闭Hyper-V。
```ps1
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All
```
如果是Windows 11用户，可以在Powershell中使用以下命令关闭Hyper-V。
```ps1
bcdedit /set hypervisorlaunchtype off
```
装好VirtualBox之后，从Vagrant的下载页面[^2]下载Vagrant的安装文件并安装好Vagrant。

安装成功之后，当在Powershell中执行`vagrant version`后，会出现以下内容。
```
Installed Version: 2.3.4
Latest Version: 2.3.4

You're running an up-to-date version of Vagrant!
```

## Vagrant的使用
安装好vagrant之后，新建一个vagrantfile可以在当前目录下执行以下命令。
```bash
vagrant init archlinux/archlinux
```
当执行`vagrant up`命令的时候，vagrant会从本地寻找`archlinux/archlinux`这个名称的box。如果本地box列表中不存在这个名称的box的话，vagrant会自动从vagrant cloud[^3]下载这个box。在使用的过程中，可以先去vagrant cloud搜索一下自己的Provider的镜像。
当虚拟机启动完成之后，就可以通过`vagrant ssh`连接到此虚拟机了。
另外，正常关闭虚拟机，使用`vagrant halt`命令。删除虚拟机，使用`vagrant destroy`命令。

总结一下：
- `vagrant init <box name>` 创建虚拟机配置文件，如果需要编辑网络、内存和硬盘等设置，可以在这一步之后，修改Vagrantfile配置文件，详细的配置文件设置可以参考官方文档中Vagrantfile[^4]这一页。
- `vagrant up` 下载虚拟机镜像，执行虚拟机配置并启动虚拟机。
- `vagrant ssh` 通过ssh连接到虚拟机
- `vagrant halt` 关闭虚拟机
- `vagrant destroy` 删除虚拟机

## 安利自己的Codeforces环境
每次换了电脑，或者重装系统之后，重新配一套Codeforces环境确实也很麻烦。了解vagrant之后，使用vagrant搭建了一套Codeforces用的虚拟环境。

使用方法：
```bash
vagrant init dianhsu/archlinux
vagrant up
```

这套环境是基于ArchLinux的镜像的，里面主要安装的软件如下所示：

- vim9 + SpaceVim[^5] + coc[^9]（Vim配置环境）
- nvm[^6]（NodeJs版本管理器）
- cf-tool[^7]（Codeforces命令行工具）
- oh-my-zsh[^8]


## 参考
[^1]: https://developer.hashicorp.com/vagrant/docs/installation
[^2]: https://developer.hashicorp.com/vagrant/downloads
[^3]: https://app.vagrantup.com/boxes/search
[^4]: https://app.vagrantup.com/boxes/search
[^5]: https://spacevim.org/
[^6]: https://github.com/nvm-sh/nvm
[^7]: https://github.com/dianhsu/cf-tool
[^8]: https://ohmyz.sh/
[^9]: https://github.com/neoclide/coc.nvim