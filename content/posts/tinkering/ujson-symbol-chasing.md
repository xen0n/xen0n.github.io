---
title: '跟 ujson 玩符号捉迷藏'
date: 2016-05-30T19:16:51+08:00
draft: false
aliases:
    - /2016/05/30/ujson-symbol-chasing/
文章类别:
    - Python
    - 折腾
---

## tl;dr

Python 的 高性能 JSON 库 `ujson` 截至目前在 Gentoo (GCC 5.3.0) 与
[FreeBSD 10][upstream-issue-freebsd] 上使用时都可能碰到 `ImportError` 错误.
该错误的修复补丁已经[提交上游][pr], 估计过一阵子就能用上了!

[upstream-issue-freebsd]: https://github.com/esnme/ultrajson/issues/180
[pr]: https://github.com/esnme/ultrajson/pull/222


## 问题

高高兴兴地开了一个新坑, 初始化了虚拟环境, 因为马上要处理一个巨大的 JSON
所以装上了 `ujson`. 开始干活!

```
In [1]: import ujson
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
<ipython-input-1-580339775a25> in <module>()
----> 1 import ujson

ImportError: /.../ujson.so: undefined symbol: Buffer_AppendShortHexUnchecked
```

(文件路径很长, 编辑掉了大部分)


## 解决

这是什么情况? 搜索了一圈, 果然我[不是][gentoo-ml][一个人][upstream-issue-freebsd],
不过看起来应该挺简单的样子因为 Gentoo 邮件列表的那个人机器上虚拟环境外的安装是正常的?!
再加上这个问题之前我在很多 Gentoo 系统上也从来没有遇到, 这就说明问题应该局限在
Python 包里面, 而且跟具体系统配置应该也有关系.

[gentoo-ml]: https://archives.gentoo.org/gentoo-user/message/a17dc1393d347a89f63d8e0db4734e6e

因为 `ujson` 是一个纯 C 写成的 Python 扩展, 本身也支持 Python 3 (我使用的是
Python 3.5 创建虚拟环境), 所以问题应该跟 Python 的 ABI 无关. 经过简单的网络搜索和
grep, 出问题的函数是 `ujson` 的一个内部 helper 函数, 这就 10000% 确定是 `ujson`
本身的 bug 了. 我们来看一下这个函数的声明:

```c
/* 为了清晰, 换行是我加的 */
FASTCALL_ATTR INLINE_PREFIX
void
FASTCALL_MSVC
Buffer_AppendShortHexUnchecked(char *outputOffset, unsigned short value);
```

还有 FreeBSD issue 中提到的 `strreverse` 的:

```c
FASTCALL_ATTR INLINE_PREFIX
void
FASTCALL_MSVC
strreverse(char* begin, char* end);
```

摘抄下这里的宏定义, 可以看到这些定义比较简陋 (平台跟编译器是平行的概念,
比方说并不是所有 Windows 程序都是用 MSVC 编译的,
完整文件的 Windows 部分里还有 `__declspec(dllexport)` 这种东西,
这种代码放到 MinGW GCC 下就要编译错误了), 不过并不影响阅读:

```c
#ifdef _WIN32

#define FASTCALL_MSVC __fastcall
#define FASTCALL_ATTR
#define INLINE_PREFIX __inline

#else

#define FASTCALL_MSVC

#if !defined __x86_64__
#define FASTCALL_ATTR __attribute__((fastcall))
#else
#define FASTCALL_ATTR
#endif

#define INLINE_PREFIX inline

#endif
```

其他函数的声明都没有这些 fastcall 和内联的标记, 因此问题就出在 fastcall 或者内联上.
不过 fastcall 是 [x86-32 的一种调用约定][fastcall-wiki], 在 AMD64 上并不存在,
那么问题只能是因为内联了.

[fastcall-wiki]: https://en.wikipedia.org/wiki/X86_calling_conventions#Microsoft_fastcall

各位还记得 C 内联函数使用的小细节吗? (此处可以暂停下来 Google 或者翻书哦)

没错, `inline` 只是给编译器的**建议**而不是**命令**, 到底是否内联编译器完全可以自行决定.
一般情况下编译器比人要聪明, 所以这样的设定并不会产生问题;
问题在于有些时候人类确实明白自己在做的事情,
尤其是编译器反对人的想法之后自己做的事情却不一定正确 (因为编译器也是人写的, 会有 bug 啊)...
因为很久之前并没有这样的问题, 最近两年 (2015-08 之后) 才开始出现,
所以用系统上的两个 gcc 版本测试了一下:

```
$ nm ujson.gcc-4.9.3.so | grep 'strreverse\|Buffer_AppendShortHex'
0000000000007557 T Buffer_AppendShortHexUnchecked
0000000000007557 t Buffer_AppendShortHexUnchecked.localalias.1
000000000000805d T strreverse
000000000000805d t strreverse.localalias.0
$ nm ujson.gcc-5.3.0.so | grep 'strreverse\|Buffer_AppendShortHex'
                 U Buffer_AppendShortHexUnchecked
                 U strreverse
```

果然! 那我们把两个函数标记成强制内联就好了:

```diff
diff --git a/lib/ultrajson.h b/lib/ultrajson.h
index 6b1fb85..894f367 100644
--- a/lib/ultrajson.h
+++ b/lib/ultrajson.h
@@ -115,7 +115,11 @@ typedef uint32_t JSUINT32;
 #define FASTCALL_ATTR
 #endif

+#ifdef __GNUC__
+#define INLINE_PREFIX __attribute__((always_inline)) inline
+#else
 #define INLINE_PREFIX inline
+#endif

 typedef uint8_t JSUINT8;
 typedef uint16_t JSUTF16;
```

因为没有用过别的编译器, 所以我只添加了 GCC 的判断和相应代码,
不过自然会有人来添加其他的所以就无所谓了...
测试一下:

```
$ nm ujson.gcc-5.3.0-always_inline.so | grep 'strreverse\|Buffer_AppendShortHex'
$
```

两个函数名已经不存在了, 这很正常, 因为它们都被内联了啊, `import` 看看:

```
In [1]: import ujson

In [2]:
```

好!


## 附: ujson 版权声明

本文引用了 `ujson` 项目的代码, 因此需要附上它的 BSD 协议:

```
Developed by ESN, an Electronic Arts Inc. studio.
Copyright (c) 2014, Electronic Arts Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of ESN, Electronic Arts Inc. nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL ELECTRONIC ARTS INC. BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Portions of code from MODP_ASCII - Ascii transformations (upper/lower, etc)
http://code.google.com/p/stringencoders/
Copyright (c) 2007  Nick Galbreath -- nickg [at] modp [dot] com. All rights reserved.

Numeric decoder derived from from TCL library
http://www.opensource.apple.com/source/tcl/tcl-14/tcl/license.terms
 * Copyright (c) 1988-1993 The Regents of the University of California.
 * Copyright (c) 1994 Sun Microsystems, Inc.
```


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
