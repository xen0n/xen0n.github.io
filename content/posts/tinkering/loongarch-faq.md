---
title: "关于 LoongArch 的常见问题解答"
date: 2022-02-12T14:55:00+08:00
draft: false
ShowToc: true
TocOpen: true
---

## 前言

自从 2021 年 LoongArch 架构官宣以来，这个架构获得了与其年龄和市场规模不成比例的关注（此处为褒义）。
但与国内外社会舆论、世界开源社区的热情相对比之下，这个架构的网上公开信息却大部分来自龙芯公司的公关宣传稿；
这可能对主要工作是开会、签字、画饼、圈钱的那些人已经足够了，但对那些要干活的广大开发者却远远不够。

本文就争取做这么一篇讲述客观事实，对开发者有用的 FAQ 文档。
由于涉及商业利益的事物不可避免存在争议，本文也力争将多方观点同时整理、平等呈现。

本文内容会不定期更新，所有更新内容都会注明更新日期。您当前看到的版本是 2022-02-13 更新的。

免责说明：除观点性质的文字之外，本文中体现的信息均取自公开资料。观点性质的文字总会被明确标注出来。
这些观点性质的文字仅代表个人观点，与本人雇主、龙芯公司等实体均无关。
本人与龙芯生态、MIPS 生态的任何企业均无关联。

## 更新记录

更新记录明细可在[本文件的 Git 提交历史](https://github.com/xen0n/xen0n.github.io/commits/main/content/posts/tinkering/loongarch-faq.md)查看。

* 2022-02-13: 部分措辞调整。
* 2022-02-12: 最初版本。

## 关于指令集

### LoongArch 是什么？中文名叫啥？

> 龙芯架构 LoongArch 是一种精简指令集计算机（Reduced Instruction Set Computing，简称 RISC）风格的指令系统架构。
>
> ——《龙芯架构参考手册》卷一：基础架构，引言

LoongArch 是龙芯公司设计的一种 CPU 指令集架构，2020 年对外公开其存在，2021 年起公开出货，在其 3A5000 CPU 产品开始搭载。

根据 LoongArch 的参考手册标题以及手册的第一句（引文即为此），LoongArch 的中文名应为“龙芯架构”。

### LoongArch 有 logo 吗？

根据现有资料，没有；注册商标的图样是纯文本。

其实比较奇怪，因为一个好的 logo 显然有助于品牌传播。希望 2022 年可以看到一个！

### LoongArch 这个单词的词源是啥，怎么念？

（注意：此处使用的英语发音为美式。）

显然，该单词是“龙芯”（Loongson）、“Architecture”两个单词的混成词（portmanteau，也叫“混合词”、“合音词”等等）。

介于此，LoongArch 的发音也应当是“龙芯”和“Architecture”两词的混合，即 /**lʊŋ˧˥**ɕin˥˥/ + /ˈ**ɑɹk**ɪtɛkt͡ʃɚ/ = /**ˈlʊŋ˧˥ˌɑɹk**/，读若“龙Arc”。<sub>中式英语发音 lóng à ke，“龙啊克” :smirk:</sub>

当然，实践中“Arch”可能也被直接拼读为/ɑɹt͡ʃ/（作“拱门”解的 arch 一词），其原因与“char”经常不被念为“car”类似。这也是可接受的读音。<sub>中式英语发音 lóng à chi 或 lóng à qu，“龙啊吃”、“龙啊去” :smirk:</sub>

### LoongArch 作为一个指令集的基本特征如何？

LoongArch 是一门：

- 支持 32 位、64 位操作的，
- 仅支持小端（Little-endian）字节序的，
- 指令字定长 32 位的，
- 寄存器-寄存器架构。

#### 其他可观察到的结论

*   **LoongArch 的操作码全部从最高位向低位延伸，也就是“前缀编码”。**

    这有助于节约指令字空间。当然，这意味着 LoongArch 表面上没有明确的“操作码”字段，虽然每个指令的高 6 位也是相当能体现指令功能分类的，仅此而已。

    （单纯从技术角度评价，前缀编码不是最优选择：后缀编码也能起到相同的节约效果。且对于小端架构，操作码位于低位更大的好处在于可以无缝支持指令字压缩，这一点可参考 RVC 的设计思路：译码器可根据靠前的字节确定指令长度。LoongArch 的做法排除了同一机器模式下支持更短指令字的可能，因为操作码从高位起，且没有明确分段，无法保证少于 4 字节的取指能看到足够的操作码。如果不是设计阶段忽视了该问题，那么 LoongArch 使用前缀编码的决策依据应该是“16 位指令字带来的代码密度提升在业务上不那么重要”。）

*   **LoongArch 是相当经典的 RISC 架构。**

    定长指令字，32 个寄存器，0 号寄存器固定表示零，目标寄存器可以不是源寄存器之一，运算操作不访存，内存模型平坦，等等。

*   **LoongArch 的一些操作比 MIPS 和 RISC-V 更带劲。**

    跳转指令和 PIC 相关操作的立即数非常宽；装载立即数至多需要 4 条指令不需要移位；ABI 甚至给未来保留了一个静态寄存器（callee-save register）剩下的也差不多够用；RISC-V 基础指令集较为欠缺的位操作能力在 LoongArch 基础指令集基本都有。

#### 基本操作的宽度定义

在基本操作的宽度定义上，LoongArch 遵循传统架构（如 x86、MIPS）做法：对于多数操作而言，某个特定操作码的宽度不随微架构、当前机器模式确定的寄存器宽度而改变。例如，使用 `add.d` 操作码的指令要么在当前模式或处理器核上非法，要么永远代表 64 位加法。

注意这与 RISC-V 的做法不同：仍以加法操作为例，RISC-V 的 `add` 指令总是操作 XLEN 宽度，在 RV32 核上操作 32 位宽，在 RV64 核上就操作 64 位了。相应地，RV64 新增的 `addw` 指令只操作低 32 位，而这条指令在 RV32 不存在。

### LA464 处理器核/微架构和 GS464V 是不是一个东西，为啥改名了？

**本回答含有猜测成分。**

首先需要明确一点，龙芯公司对其微架构/处理器核的命名似乎没有特别的讲究。
例如，3A4000 处理器包含 4 个 GS464V 核，但几年前的 3B1500 处理器，在文档上它的核也叫 GS464V。
（[维基百科][en-wiki-loongson]上有 GS464EV 的说法，这就是社区为了解除歧义而不得不生造的名字。3A2000/3A3000 的微架构叫 GS464E。）

[en-wiki-loongson]: https://en.wikipedia.org/wiki/Loongson

在网上一些较早的公开发表文章和讲演（例如 [2020.08 老胡][hww-pres-202008]）中，
主要是一些讲述 3A5000 和 LoongArch 开发过程的内容，可以看到“调整现有 IP 核的指令系统”等类似的文字。
考虑到 3A4000 到 3A5000 是一个 tock-tick 周期，
这似乎意味着 3A4000 换掉译码器就约等于 3A5000。
然而事实上指令集已经不兼容了，共用一个代号终归不好；龙芯公司最终还是在 2021 年 8 月份修改了所有手册与开源代码，
将 GS464V 批量替换为 LA464。

[hww-pres-202008]: https://www.bilibili.com/video/BV1BK411T7Za

整体上看，还是把 LA464 和 GS464V 理解为微架构大体相同，但支持指令集不同的一对不太相似的“双胞胎”为好。

### LoongArch 和 MIPS 有什么关系？

（请注意：由于所做的事情都是“通用计算”这一件事，所有 RISC 架构都存在相当程度的相似性。）

按照公开资料，LoongArch 与 MIPS 不能互操作，并且一些关键架构特性也不能做到 1:1 对应；虽然它们的许多指令可以做到 1:1 对应。

- LoongArch 指令编码与 MIPS 完全不同。
- LoongArch 不存在跳转延迟槽（branch delay slots），而 MIPS 直到 R6 才增加了可选使用的无延迟槽跳转指令。
- LoongArch 去掉了 MIPS 上的一部分历史包袱，例如神奇的 HI/LO 累加器。
- LoongArch 的 ABI 完全离开 MIPS 传统，而基于 RISC-V ABI 定义。分立的返回值寄存器、内核专用寄存器等概念都被摈弃。

但在 LoongArch 上可以看到客观的 MIPS 影响，例如：

- LoongArch 浮点比较、跳转操作所用的谓词寄存器（predicate register）`$fccX` 是单独的 8 个 flag 位，与 MIPS 做法相同，少见于现代架构。
- LoongArch 特权架构部分与 MIPS 有所相似（例如 TLB 的奇偶页设计，麻烦，不见于其他架构，但 LoongArch 这么做了）。
- 个别一些指令（如 `maskeqz/masknez`）与 MIPS R6 对应指令（`selnez/seleqz`）语义相同，且不见于其他架构。
- 个别一些操作（如 64 位立即数的装载，分四段，官方指令名为 `lu12i.w/ori/lu32i.d/lu52i.d`）与 MIPS R6 类似（`lui/ori/ahi/ati`），仅细节不同（每段的宽度，LoongArch `12/20/20/12` vs MIPS R6 `16/16/16/16`）；此做法不见于其他架构。
- 虚拟化扩展（Loongson Virtualization Extension）的缩写叫 LVZ，非常可疑。因为按照 Loongson SIMD Extension = LSX，Loongson Advanced SIMD Extension = LASX，Loongson Binary Translation Extension = LBT（不对称：没叫 LBTX）的规律，这个扩展应该缩写叫 LVX 或者 LV，无论如何不可能从第二个单词取出两个字母变成 LVZ。VZ 是 MIPS 的叫法！
- LoongArch 汇编语法与 MIPS 汇编近似。去掉了表示内存寻址的括号记法，但寄存器名字同样必须加 `$` 符号，伪指令如 `move` 取名与 MIPS 相同（而与 RISC-V 等不同）。
- 工具链、内核等基础软件的早期 LoongArch 移植基本上是相应 MIPS 代码的复制粘贴、文本替换。（当然，由于这样做的代码质量低、且两个架构并不 **那么** 相似等原因，龙芯公司随后便不这么做了。）

### LoongArch 和 RISC-V 有什么关系？

（请注意：由于所做的事情都是“通用计算”这一件事，所有 RISC 架构都存在相当程度的相似性。）

按照公开资料，LoongArch 与 RISC-V 不能互操作，并且一些关键架构特性也不能做到 1:1 对应；虽然它们的许多指令在一定条件下（如限定 64 位操作）可以做到 1:1 对应。

- LoongArch 特权架构、内存管理与 RISC-V 相当不同。
- LoongArch 基础指令集支持的操作基本是 RISC-V 相应部分的超集。
- RISC-V 的带立即数指令，立即数总是做符号扩展，而 LoongArch 有区分（算术操作做符号扩展，逻辑操作做零扩展）。
- LoongArch 操作码位于指令字高位，因而无法以 RVC 的方式实现代码压缩。

在 LoongArch 的软件部分，如 ABI 和一些基础工具链组件上，可以明显看到 RISC-V 的影响。
LoongArch ABI 与 RISC-V ABI 相当相似，且指令语义相似度也高。
在进行基础软件移植时，对 RISC-V 汇编代码经常只需做简单语法层面调整即可正确完成 LoongArch 版的相应操作。

LoongArch 的一些指令与对应的 RISC-V 指令语义完全相同，一些架构特性也类似。如：

- PIC 操作指令 `pcaddu12i` 与 RISC-V `auipc` 语义相同。
- 寄存器跳转指令 `jirl` 与 RISC-V `jalr` 语义相同，而与 MIPS `jalr` 非常不同。
- 计时指令 `rdtime.*` 与 RISC-V 相应指令语义类似，都基于恒定频率计时器。
- （实际从前身 3A4000 就有体现）LoongArch 特权资源位于 CSR 空间，CSR 概念显然来自 RISC-V。
- RISC-V 最早有四层权限（从高到低 Machine/Hypervisor/Supervisor/User，后来 Hypervisor 被移除），LoongArch 也定义了四层（从高到低 PLV0/PLV1/PLV2/PLV3）。但 LoongArch 操作系统跑在 PLV0 最高级，而 RISC-V 操作系统建议是跑在 Supervisor 级别。

这些也可能是 RISC-V 对 LoongArch 的影响体现。

### LoongArch 有哪些 ABI？

按照[龙芯架构 ELF psABI 文档][elf-psabi-doc-html]，LoongArch 目前定义了 3x2=6 种 ABI。

其中数据模型为：

- ILP32（`int`、`long`、指针都为 32 位宽，是 32 位但不彻底排斥 64 位操作的模型）
- LP64（`long` 及更宽的类型与指针为 64 位宽，是 Linux 世界通行的 64 位数据模型）

浮点支持为：

- 软浮点（S）
- 单精度硬浮点（F）
- 双精度硬浮点（D）

目前只有 LP64D 一种 ABI 有完整的支持。目前市面上已公开的商业发行版只使用这一种 ABI 构建。
如果您尝试使用其他 ABI，有极大可能会遇到各种编译错误，不建议在生态建设的早期使用。
特别地，ILP32 系列 ABI 的支持非常不完整，如果尝试使用，大概率会直接报错。

[elf-psabi-doc-html]: https://loongson.github.io/LoongArch-Documentation/LoongArch-ELF-ABI-CN.html

### LoongArch 的向量扩展是怎么一回事？

**由于相关文档没有开放，以下内容是猜测。**

MIPS 时代末期的龙芯 3A4000 实现的是完整的 MIPS MSA 向量扩展。
除此之外，3A4000 还支持从 2F 时代继承的 LoongMMI，以及从未在公开文档出现的 LSX/LASX。
梳理这些向量支持：

- MSA：根据 [MSA64 手册 v1.12][MD00868-1D-MSA64-AFP-01.12] 的描述，是 128 位固定向量宽度。
- LoongMMI：用法极度类似 x86 MMX，64 位固定向量宽度。
- LSX/LASX：除 PPT 之外公开资料近似不存在，工具链源码短暂出现后被撤回。LSX 应该是 128 位固定向量宽度，LASX 则为 256 位固定向量宽度。

[MD00868-1D-MSA64-AFP-01.12]: https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MD00868-1D-MSA64-AFP-01.12.pdf

可见所有这些向量支持都是固定宽度的。结合《龙芯架构参考手册》卷一 表 2-2“CPUCFG 访问配置信息列表”对
`LSX`、`LASX` 位的描述（“128 位向量扩展”、“256 位向量扩展”），可以推测 LoongArch 的
LSX/LASX 和 MIPS 时代的 LSX/LASX 应该是近似的东西，至少向量宽度也是固定的。
指令编码必然改变了，也可能有些指令被增删或修改，毕竟没有公开文档和开源支持，外界不会有代码依赖这些指令，也就不需要考虑兼容性。

注意到近年新兴的向量扩展，如 AArch64 的 SVE 与 RISC-V 的 RVV 都是变长向量：
软件可以在运行时动态配置向量单元使其操作宽度适应软件需求，也意味着硬件升级不需要相应修改软件即可透明地利用更宽的硬件资源。
可见这是一个较好的发展趋势。
我们在龙芯的 glibc 代码库中，注意到了[提前为变长向量做准备的变更][loongson-glibc-scalable-vec-clue]。
考虑到 LSX/LASX 迟迟未能公布可能有多方面原因（尤其不能排除知识产权问题），这或许意味着 LSX/LASX
将永远不会公开，而在将来的某个时间点会有类似 RVV 的向量指令替代 LSX/LASX 供世界使用。

[loongson-glibc-scalable-vec-clue]: https://github.com/loongson/glibc/commit/02cae44d5f05a06cba72458cf33d4a21b3813e3c


### LoongArch 的二进制翻译扩展是怎么一回事？

**由于相关文档没有开放，以下内容是猜测。**

与向量扩展的情况类似，我们可以参考 MIPS 时代龙芯的二进制翻译扩展来推测 LoongArch 的相应情况。
虽然公开渠道没有指令编码和内核支持，但这个扩展在一些[学术汇报][syuu]、乃至龙芯自己做的展示（[2020.08 老胡][hww-pres-202008]、[2021.04 福工][foxsen-pres-202104]）中已经初见端倪：

[syuu]: https://www.slideshare.net/syuu1228/hardware-assited-x86-emulation-on-godson-3-5040660
[foxsen-pres-202104]: https://www.bilibili.com/video/BV1KZ4y1c7kQ

- 新增了架构状态 EFLAGS 寄存器，为一些基础指令新增只按照相应语义更新 EFLAGS 的对应指令
- 新增了架构状态 TOP 寄存器，以及对应的 FPU 模式位，在 x87 模式下，改变浮点操作寄存器字段的语义，使其变为基于 TOP 的寻址方式

后来又添加了 ARM 条件执行等操作的支持，想必也是类似的实现思路。那么 LoongArch 的 x86、ARM
二进制翻译大概率也是先前二进制翻译扩展的微调；至于 MIPS 二进制翻译，由于同属经典 RISC 架构，
可能唯一的硬件支持会是跳转延迟槽。（HI/LO 等其他一些奇葩 MIPS 特性可以在翻译阶段由软件轻易完成，反正也要重建数据流。）

## 关于开发

### 我准备移植我的软件到 LoongArch，有什么需要准备的吗？

**您不需要特别准备！**

LoongArch 生态建设的预期是成为一个“正常”的软硬件平台。
您怎么为其他平台（如 x86、ARM）做开发，除了那些本质上就与平台相关的事情之外，在 LoongArch 上您就怎么做。

如果您使用高级语言进行具体领域的业务研发，您大体上总是不需要关注平台底层的技术细节。
这些事情已经主要由开源社区（包括全世界使用龙芯的企业和个人开发者）完成了。

如果您本身即是基础软件的开发者，或者属于需要偶尔关注底层技术细节的上层开发者，
龙芯公司提供的[龙芯架构文档][loongarch-doc-mainpage-html]是很好的出发点。

[loongarch-doc-mainpage-html]: https://loongson.github.io/LoongArch-Documentation

### 我用 C/C++ 语言，怎么写 CFLAGS？怎么针对 LoongArch 及其基础特性做条件编译？

请参阅[《龙芯架构工具链约定》][tc-conventions-doc-html]。

[tc-conventions-doc-html]: https://loongson.github.io/LoongArch-Documentation/LoongArch-toolchain-conventions-CN.html

### 我没有 LoongArch 硬件，我的软件该怎么测试？

大部分情况下，您可以使用 QEMU 完成测试。
系统级模拟（模拟一台完整的龙芯架构计算机）与用户态模拟（将当前系统的内核模拟为龙芯架构）均可以支持。
QEMU 的使用方法不属于本文范畴，请参考其他在线资料。

注：截至 2022-02-12，LoongArch 的 target 支持没有合入 QEMU 主线，这意味着您需要自行编译[龙芯的开发分支][qemu-loongson-tcg-dev]。

[qemu-loongson-tcg-dev]: https://github.com/loongson/qemu/tree/tcg-dev

## 关于生态

### 有哪些 Linux 发行版提供 LoongArch 支持了？

得益于龙芯公司优先提供的硬件与团队协作等资源，LoongArch 的商业生态建设非常迅速。

截至 2022-02-12，已有多种（中国大陆境内实体开发的）商业 Linux 发行版提供了 LoongArch port（包括但不限于，按字母顺序排列）：

- Kylin（麒麟）
- Loongnix（龙芯中科）
- UOS（统信）

[Loongnix][loongnix-home] 声称自己是“龙芯开源社区推出的 Linux 操作系统”，
但由于该“龙芯开源社区”实际外部参与者寥寥、部分软件包不开源（尤指工具链；当前的 LoongArch Loongnix 甚至有向量支持！）等原因，
该发行版实质上也属于商业发行版。

[loongnix-home]: http://www.loongnix.cn

在 LoongArch 指令集手册等文档发布、以及工具链等基础软件的龙芯分支（fork）开源后，社区发行版也加快了移植的脚步。
截至 2022-02-12 已经出现了以下的发行版移植项目（包括但不限于，字母顺序排列）：

- Arch Linux
- CLFS
- Gentoo

### 为什么我不能在社区发行版上运行 WPS Office 等软件？（“旧世界”“新世界”是怎么一回事？）

截至 2022-02-12，所有商业发行版与所有社区发行版互不兼容。
社区发行版上构建的所有二进制软件，以及部分以源码、字节码形式存在的高级语言软件（如 Python、Java 写作的软件）不能在商业发行版上运行，反之亦然。
目前第三方软件开发商提供的闭源软件（如 WPS Office 等）都是在商业发行版上构建的，在社区发行版上有极大的概率不能工作。

这个情况一般被称作 **“新旧世界”的兼容问题**。
因为龙芯公司在向开源社区发表 LoongArch 之前已经在幕后完成了所有商业动作，所以开源生态又叫“新世界”；
与之相对的，所有商业发行版都属于“旧世界”。
两个世界在未来会得到统一，但目前可以被视作两个平行宇宙。目前看来兼容的技术难度非常大。

至于为何会出现两个世界，以及有哪些方法可以做到兼容，就说来话长了 ;-) 所有细节会在不久后的另一篇文章中专门讲述。

### 市面上有哪些 LoongArch 硬件可以买到？

虽然龙芯产品的国际购买渠道自从 2F 时代之后就已基本不复存在，但至少在中国大陆地区，已经有多种搭载
LoongArch CPU 的产品可以在公开渠道方便地买到。
例如，龙芯 3A5000 有 ATX 主板、整机、笔记本形态的产品，3C5000L 有机架式服务器形态的产品。

由于涉及商业，本文不便提供任何具体的购买渠道或链接，但您总可以自行在某宝、某东、某鱼等平台上搜索“龙芯”关键词。

注意：由于目前龙芯产品产量较小，无法靠规模效应摊薄成本，这些产品会比各项指标近似的 x86、ARM 等“主流”产品贵上许多。加之生态建设早期会有许多基础性的问题亟待解决，因此 **不建议只想买来使用的非开发者用户冲动购买**。

### 怎么认识其他 LoongArch 同好？

有人用的技术就有交流社区，LoongArch 当然不例外（本文作者和伙伴们又不是猫）。

网上有许多地方都可以讨论龙芯、LoongArch 等等相关话题，人多的公开场合包括但不限于：

- [龙芯开源社区论坛](http://bbs.loongnix.cn/)（由于技术原因，目前不支持 HTTPS）（仅中文交流）
- [百度贴吧龙芯吧](https://tieba.baidu.com/f?kw=%E9%BE%99%E8%8A%AF&ie=utf-8)（仅中文交流）
- [Telegram Loongson group](https://t.me/loongson_users)（中文 & English）
- QQ 群 922566903

可能还有其他讨论龙芯话题的 QQ 群，但由于本文作者不使用 QQ，因此不知道群号。（欢迎知道的朋友给作者私聊或者提 PR 补充！）

注：这些公开场合相比技术交流更适合灌水。
由于围绕龙芯有一群观念较为极端的最终用户粉丝，就事论事的技术交流万一涉及一些敏感话题点，在以上公开场合不一定会有效率。
但如果您具备相应的技术交流态度、技能，您应该自己也能找到开发者的交流场所，因此此处就暂时不提供了 ;-)
