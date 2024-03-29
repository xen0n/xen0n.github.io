---
title: '《开局一个二进制，从零开始的 LoongArch 指令集推导》——第三回 阅读文本'
date: 2021-02-21T12:04:00+08:00
draft: false
aliases:
    - /2021/02/21/reversing-loongarch-3/
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

上一回我们讲到，解包出来的二进制真的是 LoongArch 的 ELF 文件，接下来我们可以有两个方向：一是释读 LoongArch ELF 格式的特殊内容；二是直接动手，搞明白指令含义。

ELF 文件格式支持每个架构各自表达一些特定属性、tag、section。这么做也是合情合理，正如没有两片雪花完全相同，不同架构当然也有各自独特的属性。你不会看到 AMD64 的程序库声明自己不支持浮点指令，也不会看到 ARM 可执行文件包含 MIPS 格式的重定向记录。由于 ELF 格式本身就考虑了这部分需求，我们不需要先行了解任何 LoongArch 的信息，就可以搞明白很多东西——

然而，实际操作中当然需要先弄懂指令集，才能真正把这些架构相关扩展整明白。例如你看到一个类型 3 的重定向，地址是 `78f00`，内容是 `1a2b3c`，你并不能直接知道它的含义是把“什么东西”写到“什么位置”。到底是把 `1a2b3c` 左移 10 位然后合并到 `78f00 - 代码段基址` 的指令字里？还是用 `1a2b3c` 先减去 `78f00` 构造一个 PC-relative 偏移量然后左移 6 位写入相同的地方？

那我们还是先想办法把指令都提取出来再说吧！

有一个工具叫 `readelf`，顾名思义，它 `reads ELF files`；你可以自己不带参数，或者带着 `--help` 运行一下，支持的功能挺多的。我们直接让他解析文件头：

```plain
$ readelf -eW libpython2.7_d.so.1.0
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           <unknown>: 0x102
  Version:                           0x1
  Entry point address:               0x52a10
  Start of program headers:          64 (bytes into file)
  Start of section headers:          9896856 (bytes into file)
  Flags:                             0x3
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         6
  Size of section headers:           64 (bytes)
  Number of section headers:         34
  Section header string table index: 33

Section Headers:
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            0000000000000000 000000 000000 00      0   0  0
  [ 1] .note.gnu.build-id NOTE            0000000000000190 000190 000024 00   A  0   0  4
  [ 2] .hash             HASH            00000000000001b8 0001b8 002a88 04   A  4   0  8
  [ 3] .gnu.hash         GNU_HASH        0000000000002c40 002c40 002910 00   A  4   0  8
  [ 4] .dynsym           DYNSYM          0000000000005550 005550 00a038 18   A  5   7  8
  [ 5] .dynstr           STRTAB          000000000000f588 00f588 006f5c 00   A  0   0  1
  [ 6] .gnu.version      VERSYM          00000000000164e4 0164e4 000d5a 02   A  4   0  2
  [ 7] .gnu.version_r    VERNEED         0000000000017240 017240 000110 00   A  5   7  8
  [ 8] .rela.dyn         RELA            0000000000017350 017350 0386a0 18   A  4   0  8
  [ 9] .rela.plt         RELA            000000000004f9f0 04f9f0 001cc8 18  AI  4  19  8
  [10] .plt              PROGBITS        00000000000516c0 0516c0 001350 10  AX  0   0 16
  [11] .text             PROGBITS        0000000000052a10 052a10 25b058 00  AX  0   0  8
  [12] .rodata           PROGBITS        00000000002ada68 2ada68 04664d 00   A  0   0  8
  [13] .eh_frame         PROGBITS        00000000002f40b8 2f40b8 000004 00   A  0   0  4
  [14] .init_array       INIT_ARRAY      00000000002fbc88 2f7c88 000008 08  WA  0   0  8
  [15] .fini_array       FINI_ARRAY      00000000002fbc90 2f7c90 000008 08  WA  0   0  8
  [16] .data.rel.ro      PROGBITS        00000000002fbc98 2f7c98 000138 00  WA  0   0  8
  [17] .dynamic          DYNAMIC         00000000002fbdd0 2f7dd0 000230 10  WA  5   0  8
  [18] .data             PROGBITS        00000000002fc000 2f8000 10b790 00  WA  0   0  8
  [19] .got.plt          PROGBITS        0000000000407790 403790 0009a8 08  WA  0   0  8
  [20] .got              PROGBITS        0000000000408138 404138 000998 08  WA  0   0  8
  [21] .sdata            PROGBITS        0000000000408ad0 404ad0 000008 00  WA  0   0  8
  [22] .bss              NOBITS          0000000000408ad8 404ad8 023c00 00  WA  0   0  8
  [23] .comment          PROGBITS        0000000000000000 404ad8 000022 01  MS  0   0  1
  [24] .debug_aranges    PROGBITS        0000000000000000 404afa 001c00 00      0   0  1
  [25] .debug_info       PROGBITS        0000000000000000 4066fa 1f390b 00      0   0  1
  [26] .debug_abbrev     PROGBITS        0000000000000000 5fa005 01caf8 00      0   0  1
  [27] .debug_line       PROGBITS        0000000000000000 616afd 273a49 00      0   0  1
  [28] .debug_frame      PROGBITS        0000000000000000 88a548 05c2b8 00      0   0  8
  [29] .debug_str        PROGBITS        0000000000000000 8e6800 028332 01  MS  0   0  1
  [30] .debug_ranges     PROGBITS        0000000000000000 90eb32 0089c0 00      0   0  1
  [31] .symtab           SYMTAB          0000000000000000 9174f8 037380 18     32 7723  8
  [32] .strtab           STRTAB          0000000000000000 94e878 0219d8 00      0   0  1
  [33] .shstrtab         STRTAB          0000000000000000 970250 000142 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  p (processor specific)

Program Headers:
  Type           Offset   VirtAddr           PhysAddr           FileSiz  MemSiz   Flg Align
  LOAD           0x000000 0x0000000000000000 0x0000000000000000 0x2f40bc 0x2f40bc R E 0x4000
  LOAD           0x2f7c88 0x00000000002fbc88 0x00000000002fbc88 0x10ce50 0x130a50 RW  0x4000
  DYNAMIC        0x2f7dd0 0x00000000002fbdd0 0x00000000002fbdd0 0x000230 0x000230 RW  0x8
  NOTE           0x000190 0x0000000000000190 0x0000000000000190 0x000024 0x000024 R   0x4
  GNU_STACK      0x000000 0x0000000000000000 0x0000000000000000 0x000000 0x000000 RW  0x10
  GNU_RELRO      0x2f7c88 0x00000000002fbc88 0x00000000002fbc88 0x000378 0x000378 R   0x1

 Section to Segment mapping:
  Segment Sections...
   00     .note.gnu.build-id .hash .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .plt .text .rodata .eh_frame
   01     .init_array .fini_array .data.rel.ro .dynamic .data .got.plt .got .sdata .bss
   02     .dynamic
   03     .note.gnu.build-id
   04
   05     .init_array .fini_array .data.rel.ro .dynamic
```

由于 ELF 文件头本身就是平台无关的，使用任何架构的 `readelf` 都可以读，也不管你是原生工具链，还是交叉工具链。

出于人类常识，移植一个全新的架构也犯不着把有的没的都全部改一遍，为了改而改，这样反而增加适配的工作量；所以 section 名字也都是熟悉的。那么代码段就还是叫 `.text`——文本！机器语言对机器而言就是“文本”。

```plain
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [11] .text             PROGBITS        0000000000052a10 052a10 25b058 00  AX  0   0  8
```

这意思就是，这个库的代码段装载到从 `0x52a10` 开始的一块内存，内容从文件的第 `0x52a10` 字节（编号从 0 开始）起，长度有 `0x25b058` 字节。

马上来看一下！还记得老胡那一页指令格式的 PPT 吗？所有指令都定长 32 位，跟大多数 RISC 架构都一样，那么——

```py
import struct
import sys

# one little-endian 32-bit word
INSN = struct.Struct('<I')

with open(sys.argv[1], 'rb') as fp:
    fp.seek(0x52a10, 0)
    text = fp.read(0x25b058)

# 先看 10 条指令
i = 0
while i < 40:
    insn = INSN.unpack(text[i:i + 4])[0]
    i += 4

    print(f'{insn:08x}')
```

```plain
1c0076a4
02dca084
1c0076ac
02dc818c
58001984
1c0076ac
28def18c
40000d80
4c000180
03400000
```

很工整嘛！看上去我们猜的没错——与所有其他常见 RISC 指令集一样，LoongArch 的机器码在内存中，就是一堆原生字节序的整数。对 LoongArch 而言，就是一堆 32 位的小端序整数。像这前两条指令 `1c0076a4 02dca084`，你如果直接拿十六进制编辑器打开文件，其实在那个位置存放的是 `a4 76 00 1c 84 a0 dc 02`，每 4 个字节都是反过来的。

那么我们现在已经找到了整个代码段，借助老胡的 PPT 助攻，我们甚至不用自己统计分析指令格式了，真的爽！何况现在已知的指令格式就有 10 种，还可能有未知的（剧透：真的有！），自己分析还不知要到猴年马月……现在只需要搞明白哪些 opcode 是使用的哪种指令格式，含义是啥就好了。

接下来，终于可以进入真正指令的破译工作了！欲知后事如何，且听下回分解~
