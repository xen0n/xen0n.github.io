---
title: "非官方但全面的 LoongArch 常见问题解答（2022-04-26 更新）"
date: 2022-02-12T14:55:00+08:00
draft: false
ShowToc: true
TocOpen: true
文章类别:
    - LoongArch
    - 龙芯
    - 折腾

summary: |
    关于 LoongArch 你可能需要知道的一些内容；由一名独立开发者汇总整理。
---

## 前言

自从 2021 年 LoongArch 架构官宣以来，这个架构获得了与其年龄和市场规模不成比例的关注（此处为褒义）。
但与国内外社会舆论、世界开源社区的热情相对比之下，这个架构的网上公开信息却大部分来自[龙芯中科技术股份有限公司][loongson-website]（下称龙芯公司）的公关宣传稿；
这对主要工作是开会、签字、画饼、圈钱的那些人可能已经足够了，但对那些要干活的广大开发者却远远不够。

[loongson-website]: https://www.loongson.cn/

本文就争取做这么一篇讲述客观事实，对开发者有用的 FAQ 文档。
由于涉及商业利益的事物不可避免存在争议，本文也力争将多方观点同时整理、平等呈现。

本文内容会不定期更新，所有更新内容都会注明更新日期。您当前看到的版本是 2022-04-26 更新的。

免责说明：除观点性质的文字之外，本文中体现的信息均取自公开资料。观点性质的文字总会被明确标注出来。
这些观点性质的文字仅代表个人观点，与本人雇主、龙芯公司等实体均无关。
本人与龙芯生态、MIPS 生态的任何企业均无关联。

## 更新记录

更新记录明细可在[本文件的 Git 提交历史](https://github.com/xen0n/xen0n.github.io/commits/main/content/posts/tinkering/loongarch-faq.md)查看。

* 2022-04-26: 更新上游状态；dotnet 的改动完全合并了。
* 2022-04-21: 小更新。
    - 更新上游状态；
    - 添加 Gentoo LoongArch 项目的外链。
    - LoongArch 的中文名称或定为“龙架构”。
* 2022-03-30: 更新上游状态。
* 2022-03-06: 添加“关于开发”一节两个话题；其他微调。
* 2022-02-21: 添加“关于使用”一节四个话题；为“关于开发”一节添加 target tuple、GOARCH 两个话题。
* 2022-02-20: 配合英语翻译的部分措辞调整与排版优化。
* 2022-02-15: 部分措辞调整。
* 2022-02-13: 部分措辞调整；添加指令格式、LoongArch 汇编的信息。
* 2022-02-12: 最初版本。

## 关于指令集

### LoongArch 是什么？中文名叫啥？

> 龙芯架构 LoongArch 是一种精简指令集计算机（Reduced Instruction Set Computing，简称 RISC）风格的指令系统架构。
>
> ——《龙芯架构参考手册 卷一：基础架构》，引言

LoongArch 是龙芯公司设计的一种 CPU 指令集架构，2020 年对外公开其存在，2021 年起公开出货，在其 3A5000 CPU 产品开始搭载。

根据 LoongArch 的参考手册标题以及手册的第一句（引文即为此），LoongArch 的中文名似乎应为“龙芯架构”。
龙芯中科也于 2022-01-29 申请注册“龙芯架构”为中国商标。
但随后 2022-02-23 龙芯中科即申请注册“龙架构”中国商标，
且又于 2022-04-13 在其微信公众号上发表[一篇文章][wxmp-article-1]首次将“LoongArch”与“龙架构”并列，
这似乎表明“龙架构”将成为 LoongArch 的正式中文名称。

[wxmp-article-1]: https://mp.weixin.qq.com/s/kAn_TrIirlGaBwJc6QOP3g

### LoongArch logo 长啥样？

根据现有资料，LoongArch 没有 logo。LoongArch 注册商标的图样是纯文本。

其实比较奇怪，因为一个好的 logo 显然有助于品牌传播。希望 2022 年可以看到一个！

### LoongArch 这个单词的词源是啥，怎么念？

（注意：此处使用的英语发音为美式。）

显然，该单词是“龙芯”（Loongson）、“Architecture”两个单词的混成词（portmanteau，也叫“混合词”、“合音词”等等）。

介于此，LoongArch 的发音也应当是“龙芯”和“Architecture”两词的混合，即 /**lʊŋ˧˥**ɕin˥˥/ + /ˈ**ɑɹk**ɪtɛkt͡ʃɚ/ = /ˈlʊŋ˧˥ˌɑɹk/，读若“龙Arc”。<sub>中式英语发音 lóng à ke，“龙啊克” :smirk:</sub>

当然，实践中“Arch”可能也被直接拼读为/ɑɹt͡ʃ/（作“拱门”解的 arch 一词），其原因与“char”经常不被念为“car”类似。这也是可接受的读音。<sub>中式英语发音 lóng à chi 或 lóng à qu，“龙啊吃”、“龙啊去” :smirk:</sub>

### LoongArch 作为一个指令集的基本特征如何？

LoongArch 是一门：

- 支持 32 位、64 位操作的，
- 仅支持小端（Little-endian）字节序的，
- 指令字定长 32 位的，

寄存器-寄存器架构。

#### 一些观察结论

*   **LoongArch 的操作码全部从最高位向低位延伸，也就是“前缀编码”。**

    这有助于节约指令字空间。当然，这意味着 LoongArch 表面上没有明确的“操作码”字段，虽然每个指令的高 6 位目前一定属于操作码，并且在一定程度上也能体现指令的功能分类，但仅此而已。

    > 笔者评论：
    >
    > 单纯从技术角度评价，前缀编码不是最优选择：后缀编码也能起到相同的节约效果。
    > 且对于小端架构，操作码位于低位更大的好处在于可以无缝支持指令字压缩。
    >
    > 这一点可参考 RVC 的设计思路：
    > 确定指令长度所需的所有信息都保证在取指返回的第一个字节可以看到，
    > 因而译码器总能正确确定指令长度，而不需要访问比实际指令长度更多的字节。
    >
    > LoongArch 的做法排除了同一机器模式下支持更短指令字的可能，因为操作码从高位起，且没有明确分段，无法保证少于 4 字节的取指能看到足够的操作码。
    > 可以假设复位或跳转后的第一条指令只有 2 字节长，此时取 4 字节显然是错误的；但如果只取 2 字节，而实际上第一条指令长 4 字节，那么 2 字节的取指完全可能只看到这条指令的低位即操作数字段，而操作数字段是任意的！这样就跑飞了。
    >
    > 如果不是设计阶段忽视了该问题，那么 LoongArch 使用前缀编码的决策依据应该是“16 位指令字带来的代码密度提升在真实业务场景下并不重要”。

*   **LoongArch 是相当经典的 <abbr title="Reduced Instruction Set Computing">RISC</abbr> 架构。**

    定长指令字，32 个寄存器，0 号寄存器固定表示零，目标寄存器可以不是源寄存器之一，运算操作不访存，内存模型平坦，等等。

*   **LoongArch 的一些操作比 MIPS (R6 之前) 和 RISC-V 更带劲。**

    跳转指令和 PIC 相关操作的立即数非常宽；装载立即数至多需要 4 条指令不需要移位；ABI 甚至给未来保留了一个静态寄存器（callee-save register）剩下的也差不多够用；RISC-V 基础指令集较为欠缺的位操作能力在 LoongArch 基础指令集基本都有。

#### 基本操作的宽度定义

在基本操作的宽度定义上，LoongArch 遵循传统架构（如 x86、MIPS）做法：对于多数操作而言，某个特定操作码代表操作的宽度不随微架构、当前机器模式确定的寄存器宽度而改变。
例如，`add.d` 指令要么在当前模式或处理器核上非法，要么永远代表 64 位加法。
`add.w` 指令永远合法（因为没有仅支持 16 位操作的 LoongArch 核），且永远代表 32 位加法。

|微架构/机器模式|指令|合法？|代表操作|
|:------:|:--:|:----:|--------|
|LA32|`add.w`|:o:|32 位加法|
|LA32|`add.d`|:x:|-|
|LA64|`add.w`|:o:|32 位加法|
|LA64|`add.d`|:o:|64 位加法|

注意这与 RISC-V 的做法不同：仍以加法操作为例，RISC-V 的 `add` 指令总是操作原生（XLEN）宽度，在 RV32 核上操作 32 位宽，在 RV64 核上就操作 64 位了。
相应地，RV64 新增的 `addw` 指令只操作低 32 位，而这条指令在 RV32 核上并不存在。


|微架构/机器模式|指令|合法？|代表操作|
|:------:|:--:|:----:|--------|
|RV32|`addw`|:x:|-|
|RV32|`add`|:o:|原生宽度加法（XLEN=32）|
|RV64|`addw`|:o:|32 位加法|
|RV64|`add`|:o:|原生宽度加法（XLEN=64）|

（花絮：这是笔者去年在龙芯正式公布指令集手册之前，[从零逆向 LoongArch][unofficial-reversed-insns] 过程中犯下的最重大错误之一——假定 LoongArch 采用了 RISC-V 的操作数宽度指定方式。:joy:）

[unofficial-reversed-insns]: https://github.com/loongson-community/docs/tree/master/unofficial/loongarch

### LoongArch 都有哪些指令格式？

#### 一句话回答

按照手册描述，LoongArch 有 9 种**典型**指令格式，而实际情况（按照基础软件移植的真实工作量）则有 39 种。

#### 龙芯公司的“官方口径”

按照《龙芯架构参考手册 卷一》的描述，**LoongArch 有 9 种典型的指令编码格式**。

|无立即数格式|有立即数格式|
|:--------:|:--------:|
|2R|2RI8|
|3R|2RI12|
|4R|2RI14|
||2RI16|
||1RI21|
||I26|

画出来是这样：

<style>
.loongarch-insn-formats {
    table-layout: fixed !important;
    font-family: "Fira Code", "Inziu Iosevka", "Source Code Pro", "Menlo", "Consolas", monospace;
}

.loongarch-insn-formats th,
.loongarch-insn-formats td {
    min-width: 1rem !important;
    padding: 0.1rem !important;
    border: 1px solid var(--border);
    text-align: center !important;
}

.loongarch-insn-formats th {
    background-color: var(--code-bg);
}

.loongarch-insn-formats th:first-child,
.loongarch-insn-formats tbody td:first-child {
    background-color: var(--code-bg);
}

.loongarch-insn-formats td {
    font-size: 14px; /* same as th */
}

.loongarch-insn-formats .field-opcode {
    background-color: var(--code-bg);
}
</style>
<table class="loongarch-insn-formats">
    <thead>
        <tr>
            <th rowspan="2">格式</th>
            <th colspan="32">指令字</th>
        </tr>
        <tr>
            <th>31</th><th>30</th><th>29</th><th>28</th><th>27</th><th>26</th><th>25</th><th>24</th>
            <th>23</th><th>22</th><th>21</th><th>20</th><th>19</th><th>18</th><th>17</th><th>16</th>
            <th>15</th><th>14</th><th>13</th><th>12</th><th>11</th><th>10</th><th>9</th><th>8</th>
            <th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>2R</td><td class="field-opcode" colspan="22"></td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>3R</td><td class="field-opcode" colspan="17"></td><td colspan="5">rk</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>4R</td><td class="field-opcode" colspan="12"></td><td colspan="5">ra</td><td colspan="5">rk</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>2RI8</td><td class="field-opcode" colspan="14"></td><td colspan="8">立即数</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>2RI12</td><td class="field-opcode" colspan="10"></td><td colspan="12">立即数</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>2RI14</td><td class="field-opcode" colspan="8"></td><td colspan="14">立即数</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>2RI16</td><td class="field-opcode" colspan="6"></td><td colspan="16">立即数</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>1RI21</td><td class="field-opcode" colspan="6"></td><td colspan="16">立即数低位</td><td colspan="5">rj</td><td colspan="5">立即数高位</td></tr>
        <tr><td>I26</td><td class="field-opcode" colspan="6"></td><td colspan="16">立即数低位</td><td colspan="10">立即数高位</td></tr>
    </tbody>
    <tfoot>
        <tr><td colspan="33">注：指令字部分，<code>这种背景颜色</code>的单元格意为该位属于操作码。</td></tr>
    </tfoot>
</table>

> 需要指出的是，存在少数指令，其指令编码域并不完全等同于这 9 种典型指令编码格式，而是在其基础上略有变化。
> 不过这种指令的数目并不多，且变化的幅度也不大，不会对于编译系统的开发人员带来不便。

“略有变化” :smirk:

#### 真实情况

参照上一问的回答，LoongArch 实际上没有**固定划分**的指令格式、操作数槽。
尽管多数指令的格式还算整齐，但那些少数的特殊指令编码格式简直近乎随意。

实际上，在真实汇编器（反汇编器）开发实践中，由于机器并不会关心哪个格式比哪个格式更“典型”，不一样就是不一样，开发人员往往还是要把所有指令格式变体都单独定义出来。
我们在大部分此类开源项目都可以看到这一现象：

* binutils: [MIPS][b-mips]、[RISC-V][b-riscv]、[SPARC][b-sparc]，不一定明确描述指令格式，但一定明确描述操作数槽。
* LLVM: [MIPS][l-mips]、[RISC-V][l-riscv]，实际定义的种类明显比这俩架构手册上的“基础指令格式”多得多。
* QEMU: [HPPA][q-hppa]、[RISC-V][q-riscv]，同上。

[b-mips]: https://github.com/bminor/binutils-gdb/blob/binutils-2_38/opcodes/mips-opc.c
[b-riscv]: https://github.com/bminor/binutils-gdb/blob/binutils-2_38/opcodes/riscv-opc.c
[b-sparc]: https://github.com/bminor/binutils-gdb/blob/binutils-2_38/opcodes/sparc-opc.c
[l-mips]: https://github.com/llvm/llvm-project/blob/llvmorg-13.0.0/llvm/lib/Target/Mips/MipsInstrFormats.td
[l-riscv]: https://github.com/llvm/llvm-project/blob/llvmorg-13.0.0/llvm/lib/Target/RISCV/RISCVInstrFormats.td
[q-hppa]: https://gitlab.com/qemu-project/qemu/-/blob/v6.2.0/target/hppa/insns.decode
[q-riscv]: https://gitlab.com/qemu-project/qemu/-/blob/v6.2.0/target/riscv/insn32.decode

如果按照“位域不同、操作数类型不同即指令格式不同”的标准进行严格划分，**LoongArch 基础架构 v1.00 共有 39 种不同指令格式**。
社区维护的 [loongarch-opcodes][loongarch-opcodes] 项目对 LoongArch 所有公开指令进行了汇总整理，
并给出了精确无歧义的指令格式命名方案。（利益相关：该项目由本文作者维护。）

精确描述的 LoongArch 的指令格式分类如下（操作数槽的名称含义详见 [loongarch-opcodes 项目文档][loongarch-opcodes]）：

[loongarch-opcodes]: https://github.com/loongson-community/loongarch-opcodes

<table class="loongarch-insn-formats">
    <thead>
        <tr>
            <th rowspan="2">格式</th>
            <th colspan="32">指令字</th>
        </tr>
        <tr>
            <th>31</th><th>30</th><th>29</th><th>28</th><th>27</th><th>26</th><th>25</th><th>24</th>
            <th>23</th><th>22</th><th>21</th><th>20</th><th>19</th><th>18</th><th>17</th><th>16</th>
            <th>15</th><th>14</th><th>13</th><th>12</th><th>11</th><th>10</th><th>9</th><th>8</th>
            <th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>CdFj</td><td class="field-opcode" colspan="22"></td><td colspan="5">Fj</td><td class="field-opcode" colspan="2"></td><td colspan="3">Cd</td></tr>
        <tr><td>CdFjFk</td><td class="field-opcode" colspan="17"></td><td colspan="5">Fk</td><td colspan="5">Fj</td><td class="field-opcode" colspan="2"></td><td colspan="3">Cd</td></tr>
        <tr><td>CdJ</td><td class="field-opcode" colspan="22"></td><td colspan="5">J</td><td class="field-opcode" colspan="2"></td><td colspan="3">Cd</td></tr>
        <tr><td>CjSd5k16</td><td class="field-opcode" colspan="6"></td><td colspan="16">Sd5k16 低位</td><td class="field-opcode" colspan="2"></td><td colspan="3">Cj</td><td colspan="5">Sd5k16 高位</td></tr>
        <tr><td>DCj</td><td class="field-opcode" colspan="24"></td><td colspan="3">Cj</td><td colspan="5">D</td></tr>
        <tr><td>DFj</td><td class="field-opcode" colspan="22"></td><td colspan="5">Fj</td><td colspan="5">D</td></tr>
        <tr><td>DJ</td><td class="field-opcode" colspan="22"></td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJK</td><td class="field-opcode" colspan="17"></td><td colspan="5">K</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJKUa2</td><td class="field-opcode" colspan="15"></td><td colspan="2">Ua2</td><td colspan="5">K</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJKUa3</td><td class="field-opcode" colspan="14"></td><td colspan="3">Ua3</td><td colspan="5">K</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJSk12</td><td class="field-opcode" colspan="10"></td><td colspan="12">Sk12</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJSk14</td><td class="field-opcode" colspan="8"></td><td colspan="14">Sk14</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJSk16</td><td class="field-opcode" colspan="6"></td><td colspan="16">Sk16</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJUk12</td><td class="field-opcode" colspan="10"></td><td colspan="12">Uk12</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJUk14</td><td class="field-opcode" colspan="8"></td><td colspan="14">Uk14</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJUk5</td><td class="field-opcode" colspan="17"></td><td colspan="5">Uk5</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJUk5Um5</td><td class="field-opcode" colspan="11"></td><td colspan="5">Um5</td><td class="field-opcode" colspan="1"></td><td colspan="5">Uk5</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJUk6</td><td class="field-opcode" colspan="16"></td><td colspan="6">Uk6</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJUk6Um6</td><td class="field-opcode" colspan="10"></td><td colspan="6">Um6</td><td colspan="6">Uk6</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DJUk8</td><td class="field-opcode" colspan="14"></td><td colspan="8">Uk8</td><td colspan="5">J</td><td colspan="5">D</td></tr>
        <tr><td>DSj20</td><td class="field-opcode" colspan="7"></td><td colspan="20">Sj20</td><td colspan="5">D</td></tr>
        <tr><td>DUj5</td><td class="field-opcode" colspan="22"></td><td colspan="5">Uj5</td><td colspan="5">D</td></tr>
        <tr><td>EMPTY</td><td class="field-opcode" colspan="32"></td></tr>
        <tr><td>FdCj</td><td class="field-opcode" colspan="24"></td><td colspan="3">Cj</td><td colspan="5">Fd</td></tr>
        <tr><td>FdFj</td><td class="field-opcode" colspan="22"></td><td colspan="5">Fj</td><td colspan="5">Fd</td></tr>
        <tr><td>FdFjFk</td><td class="field-opcode" colspan="17"></td><td colspan="5">Fk</td><td colspan="5">Fj</td><td colspan="5">Fd</td></tr>
        <tr><td>FdFjFkCa</td><td class="field-opcode" colspan="14"></td><td colspan="3">Ca</td><td colspan="5">Fk</td><td colspan="5">Fj</td><td colspan="5">Fd</td></tr>
        <tr><td>FdFjFkFa</td><td class="field-opcode" colspan="12"></td><td colspan="5">Fa</td><td colspan="5">Fk</td><td colspan="5">Fj</td><td colspan="5">Fd</td></tr>
        <tr><td>FdJ</td><td class="field-opcode" colspan="22"></td><td colspan="5">J</td><td colspan="5">Fd</td></tr>
        <tr><td>FdJK</td><td class="field-opcode" colspan="17"></td><td colspan="5">K</td><td colspan="5">J</td><td colspan="5">Fd</td></tr>
        <tr><td>FdJSk12</td><td class="field-opcode" colspan="10"></td><td colspan="12">Sk12</td><td colspan="5">J</td><td colspan="5">Fd</td></tr>
        <tr><td>JK</td><td class="field-opcode" colspan="17"></td><td colspan="5">K</td><td colspan="5">J</td><td class="field-opcode" colspan="5"></td></tr>
        <tr><td>JKUd5</td><td class="field-opcode" colspan="17"></td><td colspan="5">K</td><td colspan="5">J</td><td colspan="5">Ud5</td></tr>
        <tr><td>JSd5k16</td><td class="field-opcode" colspan="6"></td><td colspan="16">Sd5k16 低位</td><td colspan="5">J</td><td colspan="5">Sd5k16 高位</td></tr>
        <tr><td>JUd5</td><td class="field-opcode" colspan="22"></td><td colspan="5">J</td><td colspan="5">Ud5</td></tr>
        <tr><td>JUd5Sk12</td><td class="field-opcode" colspan="10"></td><td colspan="12">Sk12</td><td colspan="5">J</td><td colspan="5">Ud5</td></tr>
        <tr><td>JUk8</td><td class="field-opcode" colspan="14"></td><td colspan="8">Uk8</td><td colspan="5">J</td><td class="field-opcode" colspan="5"></td></tr>
        <tr><td>Sd10k16</td><td class="field-opcode" colspan="6"></td><td colspan="16">Sd10k16 低位</td><td colspan="10">Sd10k16 高位</td></tr>
        <tr><td>Ud15</td><td class="field-opcode" colspan="17"></td><td colspan="15">Ud15</td></tr>
    </tbody>
    <tfoot>
        <tr><td colspan="33">注：指令字部分，<code>这种背景颜色</code>的单元格意为该位属于操作码。</td></tr>
    </tfoot>
</table>

可见 LoongArch 的指令格式实际比 MIPS、RISC-V 复杂得多，此两种架构满打满算各自也就十几、二十种指令格式。
虽然 LoongArch 的有些格式完全可以合而为一（例如 FdCj 和 CdFj 不追求操作数顺序与汇编保持一致的话，完全就可以合并嘛），但一方面现在改已经晚了，另一方面，客观上目前的方案也确实取得了节省大量编码空间的效果。

### LA464 处理器核/微架构和 GS464V 是不是一个东西，为啥改名了？

**本回答含有猜测成分。**

首先需要明确一点，龙芯公司对其微架构/处理器核的命名似乎没有特别的讲究。
例如，3A4000 处理器包含 4 个 GS464V 核，但几年前的 3B1500 处理器，在文档上它的核也叫 GS464V。

> 笔者评论：
> [维基百科][en-wiki-loongson]上有 GS464EV 的说法，这就是社区为了解除歧义而不得不生造的名字。
> 3A2000/3A3000 的微架构叫 GS464E，而 3A4000 是一次 tock（微架构）迭代，其在 GS464E 基础上最明显的变化是终于以 <abbr title="MIPS&reg; SIMD Architecture">MSA</abbr> 的形式提供了易用的向量支持，故名。
>
> （先前的龙芯自制向量指令能力有限，且缺乏文档，因此才说 3A4000 的向量支持易用。）

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

（请注意：由于所做的事情都是“通用计算”这一件事，所有 <abbr title="Reduced Instruction Set Computing">RISC</abbr> 架构都存在相当程度的相似性。）

按照公开资料，LoongArch 与 MIPS 不能互操作，并且一些关键架构特性也不能做到 1:1 对应；虽然它们的许多指令可以做到 1:1 对应。

- LoongArch 指令编码与 MIPS 完全不同。
- LoongArch 不存在跳转延迟槽（branch delay slots），而 MIPS 直到 R6 才增加了可选使用的无延迟槽分支、跳转指令。
- MIPS 的一部分历史包袱，例如神奇的 HI/LO 累加器，在 LoongArch 都不存在。
- LoongArch 的 ABI 基于 RISC-V ABI 定义。MIPS ABI 规定的分立返回值寄存器、内核专用寄存器等概念在 LoongArch ABI 中都不存在。

但在 LoongArch 上可以看到客观的 MIPS 影响，例如：

- LoongArch 浮点比较、跳转操作所用的谓词寄存器（predicate register）`$fccX` 是单独的 8 个 flag 位，与 MIPS 做法相同，少见于现代架构。
- LoongArch 特权架构部分与 MIPS 有所相似。例如 <abbr title="Translation Look-aside Buffer">TLB</abbr> 的奇偶页设计，麻烦，不见于其他知名架构，但 LoongArch 这么做了。
- 个别一些指令与 MIPS R6 对应指令语义相同，且不见于其他知名架构。如 `maskeqz/masknez` 与 MIPS R6 `selnez/seleqz`。
- 个别一些操作与 MIPS R6 类似，仅细节不同。如 LoongArch 分四段装载 64 位立即数，官方指令名为 `lu12i.w/ori/lu32i.d/lu52i.d`，与 MIPS R6 `lui/ori/dahi/dati` 仅每段的宽度不同（LoongArch `12/20/20/12` vs MIPS R6 `16/16/16/16`）；此做法不见于其他知名架构。
- 虚拟化扩展（Loongson Virtualization Extension）的缩写叫 LVZ，非常可疑。因为按照 Loongson SIMD Extension = LSX，Loongson Advanced SIMD Extension = LASX，Loongson Binary Translation Extension = LBT（不对称：没叫 LBTX）的规律，这个扩展应该缩写叫 LVX 或者 LV，无论如何不可能从第二个单词取出两个字母变成 LVZ。VZ 是 MIPS 的叫法！
- LoongArch 汇编语法与 MIPS 汇编近似。去掉了表示内存寻址的括号记法，但寄存器名字同样必须加 `$` 符号，伪指令如 `move` 取名与 MIPS 相同（而与 RISC-V 等不同）。
- 工具链、内核等基础软件的早期 LoongArch 移植基本上是相应 MIPS 代码的复制粘贴、文本替换。（当然，由于这样做的代码质量低、且两个架构并不 **那么** 相似等原因，龙芯公司随后便不这么做了。）

### LoongArch 和 RISC-V 有什么关系？

（请注意：由于所做的事情都是“通用计算”这一件事，所有 <abbr title="Reduced Instruction Set Computing">RISC</abbr> 架构都存在相当程度的相似性。）

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
- LoongArch 特权资源位于 CSR 空间，CSR 概念显然来自 RISC-V。这一点实际从 3A5000 的前身 3A4000 就有体现。
- RISC-V 最早有四层权限（从高到低 Machine/Hypervisor/Supervisor/User，后来 Hypervisor 被移除），LoongArch 也定义了四层（从高到低 PLV0/PLV1/PLV2/PLV3）。但 LoongArch 操作系统跑在 PLV0 最高级，而 RISC-V 操作系统建议是跑在 Supervisor 级别。

这些也可能是 RISC-V 对 LoongArch 的影响体现。

### LoongArch 有哪些 ABI？

按照[龙芯架构 ELF psABI 文档][elf-psabi-doc-html]，LoongArch 目前定义了 3x2=6 种 ABI。

其中[数据模型][data-models]为：

[data-models]: https://en.wikipedia.org/wiki/64-bit_computing#64-bit_data_models

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

MIPS 时代末期的龙芯 3A4000 实现的是完整的 MIPS <abbr title="MIPS&reg; SIMD Architecture">MSA</abbr> 向量扩展。
除此之外，3A4000 还支持从 2F 时代继承的 LoongMMI，以及从未在公开文档出现的 LSX/LASX。
梳理这些向量支持：

- <abbr title="MIPS&reg; SIMD Architecture">MSA</abbr>：根据 [MSA64 手册 v1.12][MD00868-1D-MSA64-AFP-01.12] 的描述，是 128 位固定向量宽度。
- LoongMMI：用法极度类似 x86 MMX，64 位固定向量宽度。
- LSX/LASX：除 PPT 之外公开资料近似不存在，工具链源码短暂出现后被撤回。LSX 应该是 128 位固定向量宽度，LASX 则为 256 位固定向量宽度。

[MD00868-1D-MSA64-AFP-01.12]: https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MD00868-1D-MSA64-AFP-01.12.pdf

可见所有这些向量支持都是固定宽度的。结合《龙芯架构参考手册 卷一》表 2-2“CPUCFG 访问配置信息列表”对
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
二进制翻译大概率也是先前二进制翻译扩展的微调；至于 MIPS 二进制翻译，由于同属经典 <abbr title="Reduced Instruction Set Computing">RISC</abbr> 架构，
可能唯一的硬件支持会是跳转延迟槽。（HI/LO 等其他一些奇葩 MIPS 特性可以在翻译阶段由软件轻易完成，反正也要重建数据流。）

## 关于开发

### GitHub 上有好几个组织都跟龙芯/LoongArch 有关。哪个是“官方”？

你可能已经见过一两个下面的组织了：

* [“大龙芯联盟”（“Great Loongson Union”，loongson）][org-ls]（说实话笔者看这名字就烦），
* [LoongArch 平台软件移植（loongarch64）][org-la64]，以及
* [“龙芯社区”（“Loongson Community”，loongson-community）][org-l-c]。

[org-ls]: https://github.com/loongson
[org-la64]: https://github.com/loongarch64
[org-l-c]: https://github.com/loongson-community

长话短说：上面的列表是按“官方程度”降序排序的，但正如大多数围绕龙芯的事情一样，“官方”的并不一定就是好的、你想要的。

如果一定要听故事的话……

最开始，龙芯公司在 GitHub（或者任何其他“国际化的”代码托管服务）上没有任何存在，
因此 2015-07-14 一帮受够了的开源开发者设立了 [loongson-community 组织][org-l-c]作为集中的协作开发地点。
几乎所有组织成员当时都与龙芯公司没有关联；一方面由于这个，
另一方面，因为这种做技术决策和推进事情的方式并不为一些龙芯员工所待见，
龙芯公司从未官方承认过这个组织是它的“社区”，时至今日仍然如此。
的确；作为龙芯公司，可能确实很难去承认这么一个含有
[3A4000 密码学加速指令扩展逆向文档][3a4000-crypto-ase]、
[官方手册发布前就被逆向出来的 LoongArch 指令集手册][unofficial-reversed-insns]，
还有[其他一堆无门槛下载的文档][l-c-docs]
（龙芯公司官网的文档已经必须先注册账号（又名：销售线索）才能下载了）
的地方是“社区”……

[3a4000-crypto-ase]: https://github.com/loongson-community/loongson-3a4000-crypto-ase
[l-c-docs]: https://github.com/loongson-community/docs

快进到 2020 年，这一年的 8 月 LoongArch 已经官宣了，但没有代码开源出来。
长期 MATE 开发者、开源贡献者 [@yetist](https://github.com/yetist) 加入了龙芯公司，
做 LoongArch 的初始生态移植工作。
当他发觉竟没有一个**受官方承认的**社区能让同事们愿意参与其中，自然而然地，就在 2020-09-29
设立了 [loongarch64 组织][org-la64]，正好卡在国庆假期前这个时间点。
很多人都被邀请加入这个组织，其中有很多龙芯员工，但也有 Deepin（统信）的人，
以及其他很多与龙芯生态无关的开发者。
为确保工作质量，这个组织建立了内部规范：代码必须经过评审（code review），至少 3 个人同意才能合并。
龙芯公司员工没有绕过这规则的特权，当然至今为止也没有出现过违反规则的情况。
尽管时不时总有一些评审意见是低质量的，甚至闭眼同意的情况也有，但这种情况总是会被更仔细的评审者抓住。

再后来，到了 2021 年（可能与 Go loong64 移植需要开始推上游有关，但笔者记不太清了），
龙芯公司内部的**另一群人**（可能其实就是另一个部门）也发现需要一个 GitHub 组织，
然后意识到他们早在 2020-01-01 就注册了 [loongson 组织][org-ls]但完全没用起来。
出于不为人知的原因，他们没有和 loongarch64 组织协调一致，而是就在“自己的”组织单独玩：
这个组织从未邀请过非龙芯员工，团队结构也像是公司内部组织架构的翻版。
代码审查也是必须的，合并代码也要 3 个人同意，但从笔者的个人经验看来，这边的闭眼合并情况比
loongarch64 那边要严重一些。
有时候一个 PR 没有有效讨论就合并了，或者被直接关掉了，尤其后边一种，已经属于是不太礼貌的行为了。
那些龙芯公司“不喜欢”的变更基本不会有可能被合并，并且看上去对外部贡献者很快就要有 CLA 要签了。
总之这个组织的运作目的更像是为了内部协作和 bug 报告，而不是社区参与；
对于代码贡献，可能直接提交给“真”上游都比给龙芯靠谱。

> 花絮：
>
> 有种办法可以快速比较三个组织的开放程度：观察笔者账号在这三个组织的权限。
>
> 笔者是 loongson-community 的**所有者**（*owner*）之一，
> loongarch64 的普通成员之一**但有写权限**，
> 然而**完全不是** loongson 的成员。
> 这很能说明一些问题！

### 各路软件的 LoongArch 移植都进上游了吗？

要移植的软件真的有**很多**，有的进上游了，有的没进；
有的进展顺利，有的可能还在激烈争论。
笔者做了几张表来总结一下情况。

表例：

* :white_check_mark: -- 已经进入上游，并有正式版本支持
* :hourglass_flowing_sand: -- 已经进入上游，将在下一个正式版本支持
* :mag: -- 正在上游接受代码审查
* :wrench: -- 正在做，或者做完了暂时还没提交，先接受社区的初步审查
* :x: -- 还没做

（基于 2022-04-26 的信息整理。）

#### 模拟器和固件

|项目|状态|开发代码库|备注|
|-------|:----:|--------------|-----|
|QEMU（目标）|:mag:|[龙芯分支](https://github.com/loongson/qemu/tree/tcg-dev)|在其他架构上模拟 LoongArch。|
|QEMU（宿主）|:white_check_mark:|-|在 LoongArch 上模拟其他架构。在 7.0 版本发布了。|
|EDK II|:wrench:|[龙芯分支](https://github.com/loongson/edk2)||

#### 内核

|项目|状态|开发代码库|备注|
|-------|:----:|--------------|-----|
|Linux|:mag:|[loongarch-next](https://github.com/loongson/linux/tree/loongarch-next)|[kernel.org 的分支](https://git.kernel.org/pub/scm/linux/kernel/git/chenhuacai/linux-loongson.git/?h=loongarch-next)有一阵没更新了。|
|FreeBSD|:x:|-||
|OpenBSD|:x:|-||
|[RT-Thread](https://www.rt-thread.org)|:x:|-|国产实时操作系统；母公司（上海睿赛德电子科技有限公司）和龙芯公司的关系不错，但暂时没看到有 LoongArch 移植计划。|

#### GNU 工具链

|项目|状态|开发代码库|备注|
|-------|:----:|--------------|-----|
|binutils|:white_check_mark:|[龙芯分支](https://github.com/loongson/binutils-gdb)|2.38 版本添加了初步支持，但不完整；<abbr title="processor supplement ABI">psABI</abbr> 已经改得不兼容了。|
|gcc|:hourglass_flowing_sand:|[龙芯分支](https://github.com/loongson/gcc)|将在 gcc 12.1.0 正式发布。|
|glibc|:mag:|[龙芯分支（v3）](https://github.com/loongson/glibc/tree/loongarch_2_36_upstream_v3)||

#### 其他工具链组件、语言

|项目|状态|开发代码库|备注|
|-------|:----:|--------------|-----|
|musl|:wrench:|-||
|llvm|:wrench:|[龙芯分支](https://github.com/loongson/llvm-project)|分支的代码**不是**最新；关注 [SixWeining](https://reviews.llvm.org/p/SixWeining/) 以获取最新动态。|
|rust|:x:|-|被 LLVM 阻挡。|
|go|:mag:|[龙芯分支](https://github.com/loongson/go/tree/loong64-master)||
|dotnet|:hourglass_flowing_sand:|-|LoongArch64 支持[已经合并](https://github.com/dotnet/runtime/issues/59561)；将在 7.0 正式发布。|
|openjdk|:x:|-|状态未知。|
|v8|:white_check_mark:|-|[已经通过审查、合并](https://chromium-review.googlesource.com/c/v8/v8/+/3089095)；在 9.5.3 版本发布了。|

#### 其他基础设施项目

|项目|状态|开发代码库|备注|
|-------|:----:|--------------|-----|
|libbsd|:white_check_mark:|-|LoongArch64 支持[已经合并](https://gitlab.freedesktop.org/libbsd/libbsd/-/commit/15200ec7ac97e3f169b6c2f378f0ec2f94663c9f)；在 0.11.6 版本发布了。|
|libffi|:mag:|[GitHub PR](https://github.com/libffi/libffi/pull/678)||
|libunwind|:hourglass_flowing_sand:|-|LoongArch64 支持[已经合并](https://git.savannah.nongnu.org/cgit/libunwind.git/commit/?id=c5f1d12c77dea6a60740730c675fc56b3c52b86a)。|
|strace|:white_check_mark:|-|LoongArch64 支持[已经](https://github.com/strace/strace/pull/205)[合并](https://github.com/strace/strace/pull/207)；在 5.17 版本发布了。|
|systemd|:white_check_mark:|[LoongArch64 组织分支](https://github.com/loongarch64/systemd)|基本支持已经进入 v250 版本，以及为 LoongArch64 新增定义了一些[可发现分区类型][dpt]。|
|util-linux|:white_check_mark:|-|新的[可发现分区类型][dpt]已经合并。在 2.38 版本发布了。|

[dpt]: https://systemd.io/DISCOVERABLE_PARTITIONS/


### 我准备移植我的软件到 LoongArch，有什么需要准备的吗？

**您不需要特别准备！**

LoongArch 生态建设的预期是成为一个“正常”的软硬件平台。
您怎么为其他平台（如 x86、ARM）做开发，除了那些本质上就与平台相关的事情之外，在 LoongArch 上您就怎么做。

如果您使用高级语言进行具体领域的业务研发，您大体上总是不需要关注平台底层的技术细节。
这些事情已经主要由开源社区（包括全世界使用龙芯的企业和个人开发者）完成了。

如果您本身即是基础软件的开发者，或者属于需要偶尔关注底层技术细节的上层开发者，
龙芯公司提供的[龙芯架构文档][loongarch-doc-mainpage-html]是很好的出发点。

[loongarch-doc-mainpage-html]: https://loongson.github.io/LoongArch-Documentation

### LoongArch 的目标元组（target tuple）叫啥？

这里需要区分下 GNU target tuples 和 Debian multi-arch tuples，因为二者不完全相同，尤其在目标支持多个 ABI 的情况下 Debian multi-arch tuples 一定会体现具体 ABI。
完整的目标元组形如 `ARCH-VENDOR-OS-ENV`，但由于近现代大多数架构并不使用 vendor 字段，因而人们也经常将其省略，即得到形如 `ARCH-OS-ENV` 的目标三元组（target triplets）。

最常见的 LoongArch 系统配置是 LP64D ABI 的 Linux 系统，libc 为 glibc。
根据[《龙芯架构工具链约定》][tc-conventions-doc-html]，
这个配置的 Debian multiarch tuple 叫 `loongarch64-linux-gnuf64`。
相应的 GNU 目标元组目前叫 `loongarch64-unknown-linux-gnu`，其中 `unknown` 的部分有时也可省略。
（省略的 ABI 浮点与扩展后缀代表取该 ARCH 最常见的 ABI 配置。）

> 注：您可能见过[这个 2020 年末的 gnuconfig 变更][gnuconfig-202012]，这里的写法和《龙芯架构工具链约定》的最新写法有所不同：
> 没有考虑 ABI 浮点、扩展后缀，还多出一个神秘的 `loongarchx32` 检查。
> 这是由于此处记录了龙芯公司的研发们在 LoongArch 开发的最早期对其 ABI 的理解：
> 三个 ARCH 取值 `loongarch32` `loongarch64` `loongarchx32`
> 分别与 MIPS 的三个 ABI o32 n64 n32 一一对应。
> 当然，后来人们意识到既然另起炉灶了就不要无脑抄 MIPS 了，于是根据 RISC-V ABI
> 重新设计了目前的 LoongArch ABI；所谓的 LoongArch “x32” ABI 永远不会被实现了。

[gnuconfig-202012]: https://git.savannah.gnu.org/gitweb/?p=config.git;a=commitdiff;h=c8ddc8472f8efcadafc1ef53ca1d863415fddd5f;hp=05734c3b30b02196506617b4e4d4b70b3bf4bb72

### LoongArch 的 GOARCH 叫啥？

[2021 年中，社区和龙芯公司在这个问题上吵了一架][golang-go-46229] :satisfied:

最终结果是龙芯团队接受了社区意见，因而 LA64 的 GOARCH 已经确定为 `loong64` 了。
因为各种地方的 32 位支持都暂时没做，所以目前也不存在 `loong32` 的写法。

[golang-go-46229]: https://github.com/golang/go/issues/46229

### 如何快速上手 LoongArch 汇编？

手册、ABI 规范是你的好朋友 :wink:

LoongArch 的汇编语言，语法上基本是简化版的 MIPS 汇编，但也有几点重大区别。
本文作者个人体会，具体写作时，使用“脑子想着 RISC-V，手上写着 MIPS 语法”的方式可以快速上手；结合手册阅读，十分容易掌握。

* 与 MIPS 相同，寄存器都要带 `$` 前缀。（与 RISC-V 不同。）
* 与 RISC-V 相同，ABI 也将寄存器分为 `$a*` `$t*` `$s*` 三大类。（与 MIPS 不同，没有单独的 `$v*`，也没有 `$k*`。）
* PIC 写法与 RISC-V 相同，与 MIPS 不同。（abicall 调用约定是受 R6 之前的 MIPS 指令集功能限制而不得已的产物，没有带到新时代的必要。）
* TLS（线程本地存储）写法与 RISC-V 相同。（与 MIPS 不同，LoongArch 有专门的 `$tp` 寄存器了，不用 `rdhwr` 绕了。）
* 与 MIPS 相同，寄存器移动指令也叫 `move`（与 x86、RISC-V 不同，不叫 `mov` 或者 `mv`。）
* 与多数架构相同，空操作也叫 `nop`。（是 `andi $zero, $zero, 0` 的语法糖。）
* 与 MIPS 相同，过程调用返回也叫 `jr $ra`。（是 `jirl $zero, $ra, 0` 的语法糖。与 RISC-V 不同，截至 2022.02.13，没有 `ret` 的语法糖。）
* 与 MIPS 不同，代表内存地址的寄存器操作数不要加括号。（`ld $a0, 16($a1)` 变成 `ld.d $a0, $a1, 16`。）
* 装载立即数的伪指令也要加宽度后缀。（基本 `li.w` 就够用了，很少装载 64 位数。）
* 大部分指令操作数的书写顺序都是先寄存器后立即数，每组内从低位到高位。按照手册语法有特例！

除此之外，由于龙芯公司在手册定稿前没有征询更大范围社区的意见，目前版本的手册（v1.00）对指令的命名、语法都存在一些不一致、误导性乃至错误的描述。
这些也整理在 [loongarch-opcodes] 项目的文档中了。

> 笔者评论：
>
> 该项目中的修改意见早些时候已经反馈回龙芯公司相应团队，得到的回复大致意思是“手册发布了不好修改了，别的公司比如 Intel 或者 ARM 也没有这样的先例，开发者花些精力习惯就好” :smirk:
> 搞得好像龙芯公司的研发人员都有 Intel 或者 ARM 那么多的研发经验是吧？一遍就把事情都做对了？
>
> 尽管如此，本文作者以及认同该项目观点的同学们仍然在努力沟通、积极推动该项目中各方面的改进措施落地，力求在 LoongArch 为更多开发者所知之前填掉尽量多的坑，不要让后人们把我们踩过的坑和钉子再踩一遍。

### 我用 C/C++ 语言，怎么写 CFLAGS？怎么针对 LoongArch 及其基础特性做条件编译？

请参阅[《龙芯架构工具链约定》][tc-conventions-doc-html]。

[tc-conventions-doc-html]: https://loongson.github.io/LoongArch-Documentation/LoongArch-toolchain-conventions-CN.html

### 我没有 LoongArch 硬件，我的软件该怎么测试？

大部分情况下，您可以使用 QEMU 完成测试。
系统级模拟（模拟一台完整的龙芯架构计算机）与用户态模拟（基于当前宿主系统的 Linux 内核提供一个龙芯架构的 Linux 系统调用界面）均可以支持。
QEMU 的使用方法不属于本文范畴，请参考其他在线资料。

注：截至 2022-03-06，LoongArch 的 target 支持没有合入 QEMU 主线，这意味着您需要自行编译[龙芯的开发分支][qemu-loongson-tcg-dev]。

[qemu-loongson-tcg-dev]: https://github.com/loongson/qemu/tree/tcg-dev

## 关于使用

### LoongArch 的 Gentoo ARCH 叫啥？

根据 [2021 年 8 月的上游沟通][gentoo-dev-mail-202108]，Gentoo 将把 LoongArch 叫作 `ARCH=loong`。
这也就意味着你以后就写类似于 `ACCEPT_KEYWORDS="~loong"` 这样的配置了。

跟 Go 的情况不一样，这回没吵起来 :rofl:

[gentoo-dev-mail-202108]: https://archives.gentoo.org/gentoo-dev/message/388a4b7428461660e89c8eae8c292f32

### LoongArch 系统用的啥固件（BIOS）？怎么管理启动项？用啥引导器？

BIOS 是个过时一万年的概念，怎么还有人这么叫 :facepalm:

撇开这个不谈，桌面、服务器 LoongArch 系统都遵循 UEFI 固件规范，并使用 ACPI 传递设备信息。
与先前从未推入上游的 MIPS UEFI 实现不同，LoongArch 的 UEFI、ACPI 实现都走完了正规上游流程，
将在两部规范的下一次更新中公开亮相。
在此也向龙芯的固件团队表示祝贺！

由于 LoongArch 的 UEFI 实现是相当标准的，这也意味着 LoongArch 系统的启动项管理姿势、引导器使用姿势与 x86、ARM64 等其他 UEFI 平台完全相同：
你在别的平台怎么用（efibootmgr、systemd-boot、grub2、Linux EFI stub 等等），你在 LoongArch 上就怎么用！

### LoongArch 系统能用啥显卡？

目前（2022-03-06）没有 SoC 形态的 LoongArch CPU，因此 LoongArch 系统中一定存在一块桥片。
截至该时间点，可与现存唯一 LoongArch CPU——龙芯 3A5000 搭配使用的桥片仅有龙芯 7A1000 一种，
该桥片集成了一个基于 Vivante GC1000 的 GPU block，搭配龙芯自制的显示控制器 block 使用。
目前该集显的上游工作正在推进中。（etnaviv 不能直接使用。）

关于独显的兼容性，实际上一般而言只要系统上安装有相应的固件（一般无脑安装 linux-firmware 包即可），任何 **使用开源驱动的显卡** 都可正常工作。
当然，由于老黄大概率不会给 LoongArch 专门编译一份闭源驱动，而开源的 nouveau 又非常拉胯（也怪老黄），近几年的 N 卡基本就别想了。
AMD Yes！

### LoongArch 系统能用啥声卡/网卡/采集卡/鼠标/键盘/硬盘/……？

只要这硬件有 Linux 开源驱动，或者要么你够拽要么厂商大发慈悲，总之愿意给 LoongArch 提供闭源驱动，你就能用。
如果不能用，找到你周围的龙芯用户社区，反馈这个事情，一定会有开发者看到 :wink:

## 关于生态

### 有哪些 Linux 发行版提供 LoongArch 支持了？

得益于龙芯公司优先提供的硬件与团队协作等资源，LoongArch 的商业生态建设非常迅速。

截至 2022-03-06，已有多种（中国大陆境内实体开发的）商业 Linux 发行版提供了 LoongArch port（包括但不限于，按字母顺序排列）：

- Kylin（由[麒麟软件][kylin-website]开发）
- Loongnix（由[龙芯公司][loongson-website]开发）
- UOS（由[统信软件][uniontech-website]开发）

[kylin-website]: https://kylinos.cn
[uniontech-website]: https://www.uniontech.com

[Loongnix][loongnix-home] 声称自己是“龙芯开源社区推出的 Linux 操作系统”，
但由于该“龙芯开源社区”实际外部参与者寥寥、部分软件包不开源（尤指工具链；当前的 LoongArch Loongnix 甚至有向量支持！）等原因，
该发行版实质上也属于商业发行版。

[loongnix-home]: http://www.loongnix.cn

在 LoongArch 指令集手册等文档发布、以及工具链等基础软件的龙芯分支（fork）开源后，社区发行版也加快了移植的脚步。
截至 2022-03-06 已经出现了以下的发行版移植项目（包括但不限于，字母顺序排列）：

- Arch Linux
- CLFS
- [Gentoo][gentoo-loongarch-home]

[gentoo-loongarch-home]: https://wiki.gentoo.org/wiki/Project:LoongArch

### 为什么我不能在社区发行版上运行 WPS Office 等软件？（“旧世界”“新世界”是怎么一回事？）

截至 2022-03-06，所有商业发行版与所有社区发行版互不兼容。
社区发行版上构建的所有二进制软件，以及部分以源码、字节码形式存在的高级语言软件（如 Python、Java 写作的软件）不能在商业发行版上运行，反之亦然。
目前第三方软件开发商提供的闭源软件（如 WPS Office 等）都是在商业发行版上构建的，在社区发行版上有极大的概率不能直接工作。

这个情况一般被称作 **“新旧世界”** 的兼容问题。
因为龙芯公司在向开源社区发表 LoongArch 之前已经在幕后完成了所有商业动作，
所以开源生态又叫“新世界”；
与之相对的，所有商业发行版及其附属生态即构成“旧世界”。
两个世界在未来会得到统一，但目前可以被视作两个平行宇宙。目前看来兼容的技术难度非常大。

至于为何会出现两个世界，以及有哪些方法可以做到兼容，就说来话长了 ;-) 所有细节会在不久后的另一篇文章中专门讲述。

### 市面上有哪些 LoongArch 硬件可以买到？

虽然龙芯产品的国际购买渠道自从 2F 时代之后就已基本不复存在（那时龙芯产品的国际营销主要是意法半导体在做），
但至少在中国大陆地区，已经有多种搭载 LoongArch CPU 的产品可以在公开渠道方便地买到。
例如，龙芯 3A5000 有 ATX 主板、整机、笔记本形态的产品，3C5000L 有机架式服务器形态的产品。

由于涉及商业，本文不便提供任何具体的购买渠道或链接，但您总可以自行在某宝、某东、某鱼等平台上搜索“龙芯”关键词。

注意：由于目前龙芯产品产量较小，无法靠规模效应摊薄成本，这些产品会比各项指标近似的 x86、ARM 等“主流”产品贵上许多。加之生态建设早期会有许多基础性的问题亟待解决，因此 **不建议只想买来使用的非开发者用户冲动购买**。

### 怎么认识其他 LoongArch 同好？

有人用的技术就有交流社区，LoongArch 当然不例外（本文作者和伙伴们又不是猫）。

网上有许多地方都可以讨论龙芯、LoongArch 等等相关话题，人多的公开场合包括但不限于：

- ~~龙芯开源社区论坛~~（原先位于 bbs.loongnix.cn，龙芯公司已将其关闭）
- [非官方 LoongArch 社区](https://bbs.loongarch.org)（bbs.loongnix.cn 的精神续作；主要以中文交流）
- [百度贴吧龙芯吧](https://tieba.baidu.com/f?kw=%E9%BE%99%E8%8A%AF&ie=utf-8)（仅中文交流）
- [Telegram Loongson group](https://t.me/loongson_users)（中文 & English；主要以中文交流，但群友英语水平较高）
- QQ 群 922566903

可能还有其他讨论龙芯话题的 QQ 群，但由于本文作者不使用 QQ，因此不知道群号。（欢迎知道的朋友给作者私聊或者提 PR 补充！）

注：这些公开场合相比技术交流更适合灌水。
由于围绕龙芯有一群观念较为极端的最终用户粉丝，就事论事的技术交流万一涉及一些敏感话题点，在以上公开场合不一定会有效率。
但如果您具备相应的技术交流态度、技能，您应该自己也能找到开发者的交流场所，因此此处就暂时不提供了 ;-)
