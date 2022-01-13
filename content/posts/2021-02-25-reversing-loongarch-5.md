---
title: '《开局一个二进制，从零开始的 LoongArch 指令集推导》——第五回 序与跋（一）'
date: 2021-02-25T14:19:00+08:00
draft: false
---

> 本 LoongArch 指令集研究工作在百度贴吧龙芯吧同步连载。
>
> 本研究中涉及的逆向工程仅出于学习、研究目的。本研究工作未得到任何龙芯、麒麟等软硬件厂商的任何形式帮助。
>
> 本研究属于个人行为，与本人雇主或任何其他主体无关。

上一回我们从“把大象放进冰箱”说起，科普了一下基本的汇编语言概念，认识到了 C 语言的“函数”到了汇编，就是一组操作步骤的集合；那么今天，我们就要运用相同的人类常识，搞明白最初的 LoongArch 指令了！

首先，我们想知道，LoongArch 的函数大概长什么样子。但怎么知道一个函数从何处开始，到何处结束呢？

其实，函数、数据的边界，这正是前面提到过的 ELF 符号表记录的东西——可以理解成，一个符号就对应一个地址。那么下一个符号开始，自然就意味着上一个符号结束。处理 ELF 的工具几乎一定会支持符号表，但自己写一个还是很麻烦的（你可以自己试一试），有没有现成可以展示各个符号分别包含代码的工具呢？

当然有，`objdump` 是也。马上试一试：

```plain
$ objdump -dCw usr/lib/loongarch64-linux-gnu/libpython2.7_d.so.1.0
usr/lib/loongarch64-linux-gnu/libpython2.7_d.so.1.0:     file format elf64-little

objdump: can't disassemble for architecture UNKNOWN!
```

噢，我的上帝，不认识 `EM_LOONGARCH` 可执行文件，就拒绝解析……

不过，倒是有一个土办法可以绕过一下，LoongArch 的指令不是跟小端 MIPS 一样，都是 32 位小端整数么？我们动一下这个文件，假装它是一个 MIPS 可执行文件，适用 MIPS 的 `objdump` 不就能读了么？

我们先来找一下哪些字节代表架构类型：

```c
/* Type for a 16-bit quantity.  */
typedef uint16_t Elf32_Half;
typedef uint16_t Elf64_Half;

#define EI_NIDENT (16)

typedef struct
{
  unsigned char e_ident[EI_NIDENT];     /* Magic number and other info */
  Elf64_Half    e_type;                 /* Object file type */
  Elf64_Half    e_machine;              /* Architecture */
} Elf64_Ehdr;
```

通过对 `/usr/include/elf.h` 的阅读，我们发现第 18、19 两个字节代表 `e_machine` 字段，是一个和 ELF 文件相同字节序的整数，正是我们要修改的位置。

```c
#define EM_MIPS          8      /* MIPS R3000 big-endian */
```

由于历史原因，即便小端 MIPS 二进制，它的 machine number 也取 8。复制一份 `libpython2.7_d.so`，编辑文件的这两个字节，从 `02 01` 编辑成 `08 00`，保存，再来用 `mips64el-unknown-linux-gnu-objdump` 试试……

```plain
$ mips64el-unknown-linux-gnu-objdump -dCw ./libpython2.7_d-fakemips.so | less

./libpython2.7_d-fakemips.so:     file format elf64-tradlittlemips


Disassembly of section .plt:

00000000000516c0 <.plt>:
   516c0:       1c0076ce        bgtz    zero,6f1fc <stringlib_split_whitespace+0x2d8>
   516c4:       0011bdad        0x11bdad
   516c8:       28c341cf        slti    v1,a2,16847
   516cc:       02ff61ad        0x2ff61ad
   516d0:       02c341cc        syscall 0xb0d07
   516d4:       004505ad        0x4505ad
   516d8:       28c0218c        slti    zero,a2,8588
   516dc:       4c0001e0        0x4c0001e0
   516e0:       1c0076cf        bgtz    zero,6f220 <stringlib_split_whitespace+0x2fc>
   516e4:       28c301ef        slti    v1,a2,495
   516e8:       1c00000d        bgtz    zero,51720 <.plt+0x60>
   516ec:       4c0001e0        0x4c0001e0
   516f0:       1c0076cf        bgtz    zero,6f230 <stringlib_split_whitespace+0x30c>
   516f4:       28c2e1ef        slti    v0,a2,-7697
   516f8:       1c00000d        bgtz    zero,51730 <.plt+0x70>
   516fc:       4c0001e0        0x4c0001e0
(...)
```

看到东西了！右边的“MIPS 汇编”可以完全无视，毕竟根本就不是这个架构的指令，但左边也是一样可以看的，这样就省得一上来各种东西都要自己来一遍了。这个阶段的分析根本用不着这么麻烦。
