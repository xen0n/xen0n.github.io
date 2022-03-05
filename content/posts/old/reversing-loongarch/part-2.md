---
title: '《开局一个二进制，从零开始的 LoongArch 指令集推导》——第二回 ELF'
date: 2021-02-19T11:30:00+08:00
draft: false
aliases:
    - /2021/02/19/reversing-loongarch-2/
文章类别:
    - LoongArch
    - 旧文
    - 龙芯
    - 逆向工程
---

> 本 LoongArch 指令集研究工作在百度贴吧龙芯吧同步连载。
>
> 本研究中涉及的逆向工程仅出于学习、研究目的。本研究工作未得到任何龙芯、麒麟等软硬件厂商的任何形式帮助。
>
> 本研究属于个人行为，与本人雇主或任何其他主体无关。

上回我们讲到，拿到了 `libpython2.7` 和 `libpython2.7-dbg` 的包，接下来的事情自然是“开箱验货”——成品 LoongArch 二进制的真容终于要一见天日了！

Debian `.deb` 软件包的格式和静态库 `.a` 文件一样，都是 `ar` 生成的归档文件，使用 `ar x` 命令解压就好了。

解开之后有几个文件，其中 `data.tar.xz` 就是这个包的真正文件内容了（实际压缩格式可能会有不同，目前拿到的这些包都是 `xz`），再次 `tar xf` 解压之后，一个 `usr` 目录就出现在我们眼前……

```plain
$ tree usr
usr
├── lib
│   ├── loongarch64-linux-gnu
│   │   ├── libpython2.7.so.1 -> libpython2.7.so.1.0
│   │   └── libpython2.7.so.1.0
│   └── python2.7
│       └── config-loongarch64-linux-gnu
│           └── libpython2.7.so -> ../../loongarch64-linux-gnu/libpython2.7.so.1
└── share
    ├── doc
    │   └── libpython2.7 -> libpython2.7-stdlib
    └── lintian
        └── overrides
            └── libpython2.7

8 directories, 5 files
```

`/usr/lib` 下是标准的 Debian multiarch 结构，当中坐着一个动态链接库，我们来看看它大概长啥样：

```plain
$ file usr/lib/loongarch64-linux-gnu/libpython2.7.so.1.0
usr/lib/loongarch64-linux-gnu/libpython2.7.so.1.0: ELF 64-bit LSB shared object, *unknown arch 0x102* version 1 (SYSV), dynamically linked, BuildID[sha1]=003ad73232b08c258e5cb383207119da9f1ab05f, stripped
```

哦，我的老朋友！瞧瞧我们都看到了什么，`*unknown arch 0x102*`！

```c
// binutils-gdb
// include/elf/common.h
#define EM_LOONGARCH    258     /* Loongson Loongarch */
```

我们真的拿到了 LoongArch 的成品二进制！

这是一个打开优化的生产二进制，性能想必是高，使用指令种类多，体积也瘦小。

但我们同时也看到了一个逆向工程师不喜欢的 `stripped` 单词——当然这也是常规操作——意思是说，这个文件被一个叫 `strip` 的程序“脱”掉了一层皮，没有了调试信息和符号表。

对于 `stripped` 二进制，我们只能方便地访问公有符号，也就是 C 语言中没有声明为 `static` 的函数和数据。

鉴于 CPython 代码的组织形式（或者任何架构合理、可维护的 C/C++ 项目都差不多），可以说绝大部分符号都被脱掉了，大部分函数都不便找到源码相互对照。

不过，不用慌张，我们还有一个 `dbg` 包！

我们再用相同方法解开 `libpython2.7-dbg`，看一看这份二进制如何，是不是能方便我们的工作：

```plain
$ file usr/lib/loongarch64-linux-gnu/libpython2.7_d.so.1.0
usr/lib/loongarch64-linux-gnu/libpython2.7_d.so.1.0: ELF 64-bit LSB shared object, *unknown arch 0x102* version 1 (SYSV), dynamically linked, BuildID[sha1]=19d5a4d6d6752b4201edae4bd9571d15e33a87ad, with debug_info, not stripped
```

这就很舒服了！
