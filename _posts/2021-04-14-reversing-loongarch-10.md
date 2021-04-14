---
layout: post
title: '《开局一个二进制，从零开始的 LoongArch 指令集推导》——第十回 序与跋（六）'
date: 2021-04-14 14:00:00
---

> 本 LoongArch 指令集研究工作在百度贴吧龙芯吧同步连载。
>
> 本研究中涉及的逆向工程仅出于学习、研究目的。本研究工作未得到任何龙芯、麒麟等软硬件厂商的任何形式帮助。
>
> 本研究属于个人行为，与本人雇主或任何其他主体无关。

在上一回，我们已经介绍了足够多背景知识和方向，现在可以开始把 LoongArch 寄存器规范的拼图完成了！

首先我们先从简单的问题入手，先来尝试回答 saved registers 序列包含哪些寄存器。

在整个工作过程中，为了提高效率，我们一直伴随开发着一个反汇编工具。因为我们现在已经认识构成函数 prologue 的所有指令了，所以直接反汇编整个 `.text` 段，找到保存寄存器最多的一串 prologue，就能知道哪些寄存器构成 saved registers 了。

这不就找到了吗！

```plain
libpython2.7_d.so.1.0 代码（-O0 编译，无优化）

000000000012a750 <PyUnicode_BuildEncodingMap>:

   12a750:      02f3c063        addi    sp, sp, -784
   12a754:      29cc2061        sd      ra, 776(sp)
   12a758:      29cc0076        sd      fp, 768(sp)
   12a75c:      29cbe077        sd      r23, 760(sp)
   12a760:      29cbc078        sd      r24, 752(sp)
   12a764:      29cba079        sd      r25, 744(sp)
   12a768:      29cb807a        sd      r26, 736(sp)
   12a76c:      29cb607b        sd      r27, 728(sp)
   12a770:      29cb407c        sd      r28, 720(sp)
   12a774:      29cb207d        sd      r29, 712(sp)
   12a778:      29cb007e        sd      r30, 704(sp)
   12a77c:      29cae07f        sd      r31, 696(sp)
   12a780:      02cc4076        addi    s9, sp, 784

...

   12afc4:      28cc2061        ld      ra, 776(sp)
   12afc8:      28cc0076        ld      fp, 768(sp)
   12afcc:      28cbe077        ld      r23, 760(sp)
   12afd0:      28cbc078        ld      r24, 752(sp)
   12afd4:      28cba079        ld      r25, 744(sp)
   12afd8:      28cb807a        ld      r26, 736(sp)
   12afdc:      28cb607b        ld      r27, 728(sp)
   12afe0:      28cb407c        ld      r28, 720(sp)
   12afe4:      28cb207d        ld      r29, 712(sp)
   12afe8:      28cb007e        ld      r30, 704(sp)
   12afec:      28cae07f        ld      r31, 696(sp)
   12aff0:      02cc4063        addi    sp, sp, 784
   12aff4:      4c000020        ret
```

```plain
libpython2.7.so.1.0 代码（-O2 编译，有优化）

00000000000e8f20 <PyUnicode_BuildEncodingMap@@Base>:

   e8f20:       02f58063        addi    sp, sp, -672
   e8f24:       29c9a07b        sd      r27, 616(sp)
   e8f28:       29ca6061        sd      ra, 664(sp)
   e8f2c:       29ca4076        sd      fp, 656(sp)
   e8f30:       29ca2077        sd      r23, 648(sp)
   e8f34:       29ca0078        sd      r24, 640(sp)
   e8f38:       29c9e079        sd      r25, 632(sp)
   e8f3c:       29c9c07a        sd      r26, 624(sp)
   e8f40:       29c9807c        sd      r28, 608(sp)
   e8f44:       29c9607d        sd      r29, 600(sp)
   e8f48:       29c9407e        sd      r30, 592(sp)
   e8f4c:       29c9207f        sd      r31, 584(sp)

...

   e9128:       28ca6061        ld      ra, 664(sp)
   e912c:       28ca4076        ld      fp, 656(sp)
   e9130:       28ca2077        ld      r23, 648(sp)
   e9134:       28ca0078        ld      r24, 640(sp)
   e9138:       28c9e079        ld      r25, 632(sp)
   e913c:       28c9c07a        ld      r26, 624(sp)
   e9140:       28c9a07b        ld      r27, 616(sp)
   e9144:       28c9807c        ld      r28, 608(sp)
   e9148:       28c9607d        ld      r29, 600(sp)
   e914c:       28c9407e        ld      r30, 592(sp)
   e9150:       28c9207f        ld      r31, 584(sp)
   e9154:       02ca8063        addi    sp, sp, 672
   e9158:       4c000020        ret
```

这个函数的 C 代码开头长这样，可以看到有茫茫多的局部变量。而且它的篇幅很长，有茫茫多的函数调用，想必需要保存的东西也会很多。实际上也确实是这样的；再找不到比这更长的 prologue 了。

```c
PyObject*
PyUnicode_BuildEncodingMap(PyObject* string)
{
    Py_UNICODE *decode;
    PyObject *result;
    struct encoding_map *mresult;
    int i;
    int need_dict = 0;
    unsigned char level1[32];
    unsigned char level2[512];
    unsigned char *mlevel1, *mlevel2, *mlevel3;
    int count2 = 0, count3 = 0;

    /* ... */
}
```

开优化的代码可能由于 instruction scheduling 等等原因，prologue 的指令不一定连续，保存和恢复的具体顺序也不一定。我们按照顺序排列这里看到的一堆寄存器，很显然**从 r23 到 r31 都是 saved registers，按顺序分配**。如果换成按 stack slot（也就是距离 sp 的偏移量）从高到低排序，也是一样的顺序。（为何要从高到低排呢？因为和大多数架构一样，LoongArch 的栈是从高地址向低地址增长的，因此地址越高，越接近“栈底”，也就是越先被分配。）

搞明白主力的 saved registers 是哪些之后，接下来我们还要研究 fp 应该位于 saved registers 序列的头还是尾。找一些比较小的函数，看下是不是总会出现 fp 就知道了。因为不开优化的代码总会用到 fp，我们只好去开优化的代码里翻翻。私有（`static`）的函数看不到函数名，也只能硬着头皮看：

```plain
不知道哪个函数

   56a20:       02fec063        addi    sp, sp, -80
   56a24:       29c10077        sd      r23, 64(sp)
   56a28:       29c0e078        sd      r24, 56(sp)
   56a2c:       29c0a07a        sd      r26, 40(sp)
   56a30:       29c0807b        sd      r27, 32(sp)
   56a34:       29c0607c        sd      r28, 24(sp)
   56a38:       29c0407d        sd      r29, 16(sp)
   56a3c:       29c0207e        sd      r30, 8(sp)
   56a40:       29c12061        sd      ra, 72(sp)
   56a44:       29c0c079        sd      r25, 48(sp)

还是不知道哪个函数

   5a480:       02ff0063        addi    sp, sp, -64
   5a484:       29c0607a        sd      r26, 24(sp)
   5a488:       29c0e061        sd      ra, 56(sp)
   5a48c:       29c0c077        sd      r23, 48(sp)
   5a490:       29c0a078        sd      r24, 40(sp)
   5a494:       29c08079        sd      r25, 32(sp)
   5a498:       29c0407b        sd      r27, 16(sp)
```

这样我们就发现了，如果需要保存的寄存器不多，那么是轮不到 fp 上场的，虽然如果 fp 被用到了它会出现在 stack slot 最底下。整理一下：

* 分配顺序（从先到后）：`r23-r31 fp`
* 栈上顺序（从底到顶）：`(ra) fp r23-r31`

按照分配顺序起名字，`r23-r31` 应该叫做 `s0-s8`。至于 `fp`，虽然可选它作为帧指针，但无奈并没有什么上苍的旨意强制所有程序都要正确维护帧指针，因此它正确的归宿仍然是 saved register 序列，`r22 = s9 = fp`。它与其他 saved registers 的唯一区别，也就是在栈上排在 `ra` 之后 `s0` 之前而已。

我们的知识又扩充了一行！

|编号|别名|保存方|备注|
|----|----|------|----|
|1|ra|Caller|返回地址|
|3|sp|Callee|栈指针|
|22|s9/fp|Callee|保证不被过程调用覆盖；可用作帧指针|
|23-31|s0-s8|Callee|保证不被过程调用覆盖|

我们还有好几个问题没有回答；欲知后事如何，请看下回分解。
