---
title: Dev Container：也许是一种比虚拟机更方便的虚拟开发环境
math: false
date: 2023-06-07 13:03:59
categories: 工具
tags:
    - 虚拟环境
    - Docker

index_img: https://cdn.dianhsu.com/img/2023-06-07-18-00-17.jpg-400x250
---

## Dev Container介绍

之前在用Vagrant[^4] + VirtualBox的虚拟环境进行OpenWrt编译，因为Vagrant + VirtualBox的方式可以在Windows上面提供一个可分发的、独立的Linux开发环境，可以很方便地在多个不同的桌面环境下使用完全相同的开发环境。但是使用Vagrant + VirtualBox的虚拟开发环境也存在一些问题，这些问题主要有：
1. 虚拟机启动比较慢，Vagrant偶尔不能获取到VirtualBox的状态。此外虚拟机偶尔不能正常关机，需要使用强制关机的方式才可以关机。
2. 虚拟机运行过程中占用的系统资源（CPU核心数、内存）比较多。如果电脑配置不太高，运行虚拟机的同时运行其他程序会感觉到一些卡顿。
3. 虚拟机的镜像文件比较大，通常是几GB到十几GB的大小，在多个桌面环境下进行安装，对网络的要求比较高。

考虑到Vagrant + VirtualBox的这些不足，因为Vagrant也支持Docker作为Provider，尝试使用Docker容器代替VirtualBox这个Provider。Docker Container和虚拟机都是在于底层硬件隔离的环境中部署应用程序的方式，这两种方式方式的区别，主要在于隔离的级别不同。Docker Container相对于虚拟机的隔离级别比较低，所以Docker Container的容器比较轻巧、打包的容量比较小并且启动速度比较快。


![Virtual Machines 和 Containers 的对比](https://cdn.dianhsu.com/img/2023-06-07-19-06-21.png)

在使用Docker作为Vagrant的Provider之后，考虑到常用的编辑器和IDE均对Docker已有支持，在使用Docker的情况下，就不再使用Vagrant来管理Container了。Visual Studio Code提供了一种对使用Docker作为开发环境更友好的方式——Dev Container[^1][^2]，这里就使用Visual Studio Code + Dev Container的方式进行介绍。

## Dev Container安装及使用

首先下载并安装Visual Studio Code和Docker Engine，Visual Studio Code的下载地址是：[https://code.visualstudio.com/#alt-downloads](https://code.visualstudio.com/#alt-downloads)，Docker Engine的下载地址是：[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)，在支持Docker Desktop的平台上，也可以选择安装Docker Desktop。

在安装好Visual Studio Code和Docker Engine之后，使用Visual Studio Code打开目标项目的工作目录，点击Visual Studio Code界面左下角的启动远程连接的按钮，启动远程连接的按钮如下图所示：
![启动远程连接的按钮](https://cdn.dianhsu.com/img/2023-06-07-20-24-18.png)

点击启动远程连接的按钮之后，就会出现远程连接的选项界面，这里点击选项`添加开发容器配置文件...`。

![远程连接选项](https://cdn.dianhsu.com/img/2023-06-07-20-26-13.png)

在接下来的步骤中依次选择需要的容器的操作系统、容器的操作系统版本以及容器中附带的软件。这里我选择的是Ubuntu(Jammy)并且不安装任何附加软件。点击确定之后，在当前Visual Studio Code打开的项目的根目录下会生成一个`.devcontainer`的文件夹，在这个文件夹中包含一个`devcontainer.json`文件，文件的内容如下所示：

```json5
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
// README at: https://github.com/devcontainers/templates/tree/main/src/ubuntu
{
	"name": "Ubuntu",
	// Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
	"image": "mcr.microsoft.com/devcontainers/base:jammy"

	// Features to add to the dev container. More info: https://containers.dev/features.
	// "features": {},

	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	// "forwardPorts": [],

	// Use 'postCreateCommand' to run commands after the container is created.
	// "postCreateCommand": "uname -a",

	// Configure tool-specific properties.
	// "customizations": {},

	// Uncomment to connect as root instead. More info: https://aka.ms/dev-containers-non-root.
	// "remoteUser": "root"
}
```

这样，我们项目就拥有了一个Dev Container基础环境。接下来，我们从容器中打开我们项目的工作目录。点击左下角启动远程连接的按钮，在远程连接的选项界面出现了一个新的选项`在容器中重新打开`，我们点击这个选项。

![新的选项“在容器中重新打开”出现](https://cdn.dianhsu.com/img/2023-06-07-20-36-35.png)

左下角远程连接变成`开发容器:xxx`之后，就代表已经从容器中打开了当前项目。此时打开终端，就可以看到当前目录为`/workspaces/<项目目录名称>/`，因为容器会自动挂在当前项目目录到`/workspaces/`中。到这里，我们就可以愉快地在容器中进行软件开发啦。😊

![通过Dev Container打开项目](https://cdn.dianhsu.com/img/2023-06-07-20-42-37.png)


## 基于Dev Container的Codeforces竞赛环境配置

这里演示下用Dev Container进行Codeforces竞赛环境配置。首先在桌面上创建一个名叫`algorithm`的文件夹，之后我们Codeforces的代码都放在这里了。接下来用Visual Studio Code打开这个目录。

这里我们想自定义容器镜像，就不使用Dev Container创建配置文件的工具了，而是选择手动创建这些文件。在`algorithm`目录下创建一个名为`.devcontainer`的文件夹，在`.devcontainer`目录中创建两个空白文件，文件名为`devcontainer.json`和`Dockerfile`文件。

`.devcontainer/devcontainer.json`的文件内容如下所示：
> 这里的配置文件中多了`build`键和`mounts`键，少了一个`image`键。
> `build`键是代表我们的容器环境是从本地的Dockerfile构建的，上面的配置文件中拥有的`image`键代表的是从远端拉取容器镜像。
> `mounts`键是挂载卷到容器的某个目录，这里是挂载了cf-tool的配置文件目录，即使容器销毁，下次打开容器依旧可以用之前写好的配置文件。
> 详细的配置文件可以参考官方的references[^7]。
```json5
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
// README at: https://github.com/devcontainers/templates/tree/main/src/ubuntu
{
	"name": "Algorithm",
	// Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
	"build": {
		"dockerfile": "Dockerfile"
	},
	"mounts": [
		{
			"source": "cf-volume",
			"target": "/root/.cf/",
			"type": "volume"
		}
	],
	// Features to add to the dev container. More info: https://containers.dev/features.
	// "features": {},
	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	// "forwardPorts": [],
	// Use 'postCreateCommand' to run commands after the container is created.
	// "postCreateCommand": "uname -a",
	// Configure tool-specific properties.
	// "customizations": {},
	// Uncomment to connect as root instead. More info: https://aka.ms/dev-containers-non-root.
	"remoteUser": "root"
}
```

`.devcontainer/Dockerfile`的文件内容如下所示：

> 这里设置容器所需要的镜像，作为一个C++选手，自然要选择带了GCC的容器了。虽然可以用Ubuntu的镜像安装GCC，但是Ubuntu的源中的GCC版本落后于GNU官方提供的GCC容器[^3]，所以这里直接选择的就是GCC的容器。其他语言的选手，可以在Docker Hub[^6]或者其他的平台寻找适合自己的基础镜像。
> 接下来安装cf-tool就可以了
```Dockerfile
# 导入基础镜像GCC
FROM gcc
# 更新包数据库
RUN apt-get update
# 安装必要的软件包
RUN apt-get install -y gdb build-essential curl sed unzip
# 安装cf-tool
RUN curl -L $(curl -s https://api.github.com/repos/dianhsu/cf-tool/releases/latest | grep /cf_linux_x64.zip | cut -d '"' -f 4) -o dist.zip && unzip dist.zip && rm dist.zip && mv cf /usr/bin/cf && chmod a+x /usr/bin/cf
```

填写好上面两个文件之后，看到的文件结构和文件内容如下图所示：

![创建文件之后的效果](https://cdn.dianhsu.com/img/2023-06-07-21-02-21.png)

接下来点击Visual Studio Code左下角的远程连接按钮，从远程连接选项中选择`在容器中重新打开`，就可以从容器中打开`algorithm`目录了，我们从命令行运行了一下`cf-tool`[^5]工具，效果如下图所示。
![从容器打开项目文件夹](https://cdn.dianhsu.com/img/2023-06-07-21-00-04.png)

`algorithm`目录已经挂载到容器中的`/workspaces/algorithm`处。为了在不打开容器的时候也可以访问提交的代码，最好将代码放在`algorithm`当中。在上面这样的环境设置下，容器销毁之后，容器中`/root/.cf/`和`/workspaces/algorithm/`这两个目录依旧存在，而只有`/workspaces/algorithm/`可以在宿机中直接访问。`/root/.cf/`这个目录，也就是`cf-volume`可以在Docker的Volumes里面看到，这个目录只有挂载到容器中才能访问，不可以通过宿机直接访问。

![Docker的Volumes](https://cdn.dianhsu.com/img/2023-06-07-21-21-52.png)

### Tips
使用Dev Container作为Codeforces竞赛环境的Tips：
- 可以在项目目录下写几个tasks方便编译、运行、调试和提交代码。
- 可以一边写代码，一边玩游戏了，不卡🤣🤣🤣。
- 容器镜像的管理工作流可以根据自己的喜好选择，可以选择本地构建，也可以选择远程自动构建并托管到Docker Hub之类的平台上。

作为一个工具控，对更加便利、高效的开发环境的追求是没有止境的，欢迎大家po一下自己的开发方式，感谢🎉🎉🎉。

## 参考
[^1]: https://code.visualstudio.com/docs/devcontainers/containers
[^2]: https://containers.dev/
[^3]: https://hub.docker.com/_/gcc
[^4]: https://www.vagrantup.com/
[^5]: https://github.com/dianhsu/cf-tool
[^6]: https://hub.docker.com/
[^7]: https://containers.dev/implementors/json_reference/