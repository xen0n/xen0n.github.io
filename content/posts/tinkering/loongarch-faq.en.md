---
title: "The unofficial yet comprehensive FAQ for LoongArch (last updated 2022-03-30)"
date: 2022-02-12T14:55:00+08:00
draft: false
ShowToc: true
TocOpen: true
categories:
    - LoongArch
    - Loongson
    - tinkering

summary: |
    Things you probably should know about the LoongArch, compiled and written by an independent developer.
    Translated from the Chinese version with the addition of some helpful language and cultural background.
---

## Foreword

The LoongArch has garnered much attention since its public debut in 2021,
disproportionate to its infancy status both in terms of age and market share
(and we are being complimentary here).
Most of public information surrounding this architecture, however, comes from
press releases of [the Loongson Technology Corporation Limited][loongson-website]
(the Loongson Corporation; website is Chinese-only); this is in stark contrast
with all the attention it is receiving from (open-source) communities
worldwide.
This may be enough for those people whose job is primarily attending
conferences telling stories, making (often empty) promises for bringing
investment, but definitely nowhere near satisfactory for ordinary developers
who have to get the actual job done.

[loongson-website]: https://www.loongson.cn/

This FAQ document strives to tell the facts around the LoongArch, in hopes of
being useful to fellow developers.
But commercial things are invariably controversial, so we also make an effort
to take a neutral stance and try to equally present the disagreeing opinions.

This document is being updated from time to time, and changes are always
accompanied with update dates.
The version you are currently reading is last updated at 2022-03-30.
(Dates are always in the YYYY-MM-DD format, for ease of tracking changes
between the original and the translations.)

Disclaimer:
Information presented in this document is all taken from publicly available
sources, except those explicitly marked as opinions.
Opinions are always explicitly marked as such, and are strictly personal and
have nothing to do with the author's employer, Loongson Corporation or any
other entity.
The author is not affiliated with any of the companies part of the Loongson or
MIPS ecosystem.

## Changelog

You can view the change details at [this article's Git history](https://github.com/xen0n/xen0n.github.io/commits/main/content/posts/tinkering/loongarch-faq.en.md).

* 2022-03-30: Updated the upstreaming progress section.
* 2022-03-06: Added several more topics; minor tweaks all over.
* 2022-02-21: (English version only) Added note on the meanings of "loong" and "Loongson".
* 2022-02-20: Added translation to English; synced wording adjustments and layout tweaks with the Chinese original.
* 2022-02-15: Adjusted wording.
* 2022-02-13: Adjusted wording; added information about instruction formats and assembly language.
* 2022-02-12: Initial version.

## About the <abbr title="instruction set architecture">ISA</abbr>

### What's LoongArch?

> The **LoongArch** architecture (LoongArch) is an **I**nstruction **S**et **A**rchitecture (ISA) that has **R**educed **I**nstruction **S**et **C**omputer (RISC) style.
>
> -- *LoongArch Reference Manual, Volume 1: Basic Architecture*

LoongArch is an instruction set architecture designed by the Loongson
Corporation, publicly announced in 2020.
Shipping started in 2021 with the 3A5000 products.

The Chinese name for LoongArch is 龙芯架构 (in Simplified characters, because
the Loongson Corporation is based in Beijing; 龍芯架構 in Traditional
characters), according to the title and first sentence of the original manual.
It just means "Loongson Architecture".

> Note: the word 龙/龍/loong means "[Chinese dragon]", or more precisely, just
> "loong".
> The Chinese dragon never breathes fire, for example.
> (Actually some of them mostly bring about rains and storms when they feel
> like doing so!)
>
> And the character 芯 means "core/chip" in this context, so the
> "龙芯/龍芯/Loongson" name has a literal meaning of "Dragon's Core" or
> "Dragon's Chip".

[Chinese dragon]: https://en.wikipedia.org/wiki/Chinese\_dragon

### What does LoongArch's logo look like?

LoongArch does not have a logo according to public information.
Its trademark is just plain text.

It is actually strange to not have a logo, though, because a good logo
certainly helps a lot in brand promotion. Hope we can see one in 2022!

### What's the etymology of the word LoongArch, and how to pronounce it?

(Note: the English pronunciation described here is American.)

Obviously the word is a portmanteau of "**龙**芯" (*Loong*son) and "*arch*itecture".
Because of this, it should also be pronounced as such, as a mixture of the two
words: /**lʊŋ˧˥**ɕin˥˥/ + /ˈ**ɑɹk**ɪtɛkt͡ʃɚ/ = /ˈlʊŋ˧˥ˌɑɹk/ ("龙Arc", "lóng arc").
<sub>This would be "lóng à ke" in typical Chinglish accent :smirk:</sub>

In practice, the "Arch" part is often just pronounced /ɑɹt͡ʃ/, the same
reason why the word "char" often does not get pronounced as "car".
This pronunciation is acceptable as well.
<sub>This would be "lóng à chi" or "lóng à qu" in typical Chinglish accent :smirk:</sub>

### What are the basic features of LoongArch as an <abbr title="instruction set architecture">ISA</abbr>?

LoongArch is a register-register architecture which:

- supports 32-bit and 64-bit operations,
- is little-endian-only,
- has 32-bit fixed-length instruction words.

#### Some observations

*   **LoongArch opcodes all extend from <abbr title="most significant bit">MSB</abbr> to <abbr title="least significant bit">LSB</abbr>, i.e. are allocated in a "prefix encoding" fashion.**

    This is helpful for conserving the encoding space.
    Of course, it also means that there is no well-defined "opcode" field in
    LoongArch; although the 6 highest bits are currently guaranteed to be part
    of the opcode, and can tell something about instructions' "functional
    classification", there is little more.

    > Author's comments:
    >
    > Prefix encoding is not the optimal choice from a purely technical
    > perspective: suffix encoding achieves the same conservation effect, while
    > also enabling transparent support for compressed instructions on
    > little-endian architectures.
    >
    > Take the RVC extension for example: all information necessary for
    > determining the instruction length is guaranteed to be present in the
    > first byte fetched, thus the decoder can always correctly figure out
    > the instruction length without asking to fetch more bytes than strictly
    > necessary.
    >
    > The LoongArch approach precludes the possibility of shorter instruction
    > words in the same machine mode, because the opcode sits at
    > <abbr title="most significant bit">MSB</abbr> side and has no well-defined
    > segments, making it impossible to see enough of opcode with instruction
    > fetches shorter than 4 bytes.
    > For example, suppose the first instruction after a reset or a jump is
    > 2 bytes long. Fetching 4 bytes is clearly wrong here; but if only 2 bytes
    > are fetched while the instruction is actually 4 bytes long, then the
    > fetch may well only see the
    > <abbr title="least significant bit">LSB</abbr>-portion that are actually
    > operands. But the operand fields are arbitrarily specified by the
    > programmer, and boom! the core runs amok.
    >
    > If this problem was not overlooked in the design phase, then the most
    > probable reason behind the design decision could be that
    > "code density improvements with 16-bit instruction words are not
    > worthwhile for actual business cases".

*   **LoongArch is a rather classical <abbr title="Reduced Instruction Set Computing">RISC</abbr> design.**

    Complete with fixed-length instructions, 32 registers, hard-wired zero register, 3-operand instructions, pure computations that do not touch memory, flat memory model, etc...

*   **Some of the LoongArch operations are more powerful than (pre-R6) MIPS and RISC-V.**

    Jumps and <abbr title="position-independent code">PIC</abbr>-related
    operations have wide immediate fields;
    immediates are loaded in 4 instructions at most without shifting;
    the <abbr title="application binary interface">ABI</abbr> even reserves one
    register for future use, while having enough for almost all cases;
    various bitwise operations lacking in the RISC-V base
    <abbr title="instruction set architecture">ISA</abbr> are present in that of
    LoongArch.

#### On the widths of operations

LoongArch follows the classical approach (as with x86 or MIPS) in defining the
widths for operations: for almost all operations, the operand width of a
specific opcode does not change with the register width, as determined by the
<abbr title="micro-architecture">µarch</abbr> or the current machine mode.
For example, the `add.d` instruction either is illegal in the current machine
mode / on a particular core, or always represents the 64-bit addition
operation.
The `add.w` instruction always exists (because there is no LoongArch core with
at most 16-bit support), and always represents the 32-bit addition operation.

|<abbr title="Micro-architecture">Μarch</abbr>/Machine mode|Instruction|Legal?|Operation represented|
|:------:|:--:|:----:|--------|
|LA32|`add.w`|:o:|32-bit addition|
|LA32|`add.d`|:x:|-|
|LA64|`add.w`|:o:|32-bit addition|
|LA64|`add.d`|:o:|64-bit addition|

Compare this with the RISC-V approach: still using additions for our example,
the `add` instruction always operates on native (XLEN) width operands,
representing the 32-bit addition on RV32 cores, and 64-bit addition on RV64
cores.
Meanwhile, the `addw` instruction brought by RV64 only operates on the lower
32-bit even on RV64 cores, but this instruction does not exist on RV32 cores.

|<abbr title="Micro-architecture">Μarch</abbr>/Machine mode|Instruction|Legal?|Operation represented|
|:------:|:--:|:----:|--------|
|RV32|`addw`|:x:|-|
|RV32|`add`|:o:|Native-width addition (XLEN=32)|
|RV64|`addw`|:o:|32-bit addition|
|RV64|`add`|:o:|Native-width addition (XLEN=64)|

(Trivia: this is one of the biggest mistakes your author made, while
[reverse-engineering LoongArch from scratch][unofficial-reversed-insns]
before Loongson released the <abbr title="instruction set architecture">ISA</abbr>
manual -- assuming that LoongArch specified its operand widths just like RISC-V.
:joy:)

[unofficial-reversed-insns]: https://github.com/loongson-community/docs/tree/master/unofficial/loongarch

### How many instruction formats do LoongArch have?

#### tl;dr

There are 9 *typical* instruction formats.
But in fact there are *39*, based on real effort needed in porting low-level software.

#### Loongson's "official" stance

According to *LoongArch Reference Manual, Volume 1*, there are 9 *typical* instruction formats.

|No immediate|With immediate|
|:--------:|:--------:|
|2R|2RI8|
|3R|2RI12|
|4R|2RI14|
||2RI16|
||1RI21|
||I26|

Which look like this when pictured:

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
            <th rowspan="2">Format</th>
            <th colspan="32">Instruction word</th>
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
        <tr><td>2RI8</td><td class="field-opcode" colspan="14"></td><td colspan="8">imm</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>2RI12</td><td class="field-opcode" colspan="10"></td><td colspan="12">imm</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>2RI14</td><td class="field-opcode" colspan="8"></td><td colspan="14">imm</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>2RI16</td><td class="field-opcode" colspan="6"></td><td colspan="16">imm</td><td colspan="5">rj</td><td colspan="5">rd</td></tr>
        <tr><td>1RI21</td><td class="field-opcode" colspan="6"></td><td colspan="16">imm low</td><td colspan="5">rj</td><td colspan="5">imm high</td></tr>
        <tr><td>I26</td><td class="field-opcode" colspan="6"></td><td colspan="16">imm low</td><td colspan="10">imm high</td></tr>
    </tbody>
    <tfoot>
        <tr><td colspan="33">Note: cells with <code>this background</code> represent opcode bits.</td></tr>
    </tfoot>
</table>

> There are a few instructions whose encoding style is not completely
> equivalent to these 9 typical instruction formats.
> However, the number of such instructions is small and the instructions
> change little, which will not be inconvenient for compiler developers.

"change little" :smirk:

#### The truth

According to the answer above, in fact LoongArch has no *well-defined*
instruction formats or operand slots.
Although most instructions have reasonably consistent encodings, the few that
do require special encoding are encoded almost arbitrarily.

Indeed, people still have to define all the instruction format variants when
developing (dis-)assemblers, because the machine does not care which format is
"more typical" than others; different is different.
We can observe this phenomenon in most open-source projects with this kind of
low-level handling:

* binutils: [MIPS][b-mips]、[RISC-V][b-riscv]、[SPARC][b-sparc]; there may or may not be definitions for the different instruction formats, but there are always complete description for operand slots.
* LLVM: [MIPS][l-mips]、[RISC-V][l-riscv]; significantly more instruction formats defined than the few "basic formats" described on manuals.
* QEMU: [HPPA][q-hppa]、[RISC-V][q-riscv]; ditto.

[b-mips]: https://github.com/bminor/binutils-gdb/blob/binutils-2\_38/opcodes/mips-opc.c
[b-riscv]: https://github.com/bminor/binutils-gdb/blob/binutils-2\_38/opcodes/riscv-opc.c
[b-sparc]: https://github.com/bminor/binutils-gdb/blob/binutils-2\_38/opcodes/sparc-opc.c
[l-mips]: https://github.com/llvm/llvm-project/blob/llvmorg-13.0.0/llvm/lib/Target/Mips/MipsInstrFormats.td
[l-riscv]: https://github.com/llvm/llvm-project/blob/llvmorg-13.0.0/llvm/lib/Target/RISCV/RISCVInstrFormats.td
[q-hppa]: https://gitlab.com/qemu-project/qemu/-/blob/v6.2.0/target/hppa/insns.decode
[q-riscv]: https://gitlab.com/qemu-project/qemu/-/blob/v6.2.0/target/riscv/insn32.decode

If we classify the instruction formats according to the strict rule of
"different bit-fields or different operand types, different format", then
the v1.00 LoongArch base <abbr title="instruction set architecture">ISA</abbr>
has a total of *39 distinct instruction formats*.
The community-maintained [loongarch-opcodes][loongarch-opcodes] project
provides a collection of all publicly known LoongArch instructions, and a
precise naming scheme for instruction formats.
(Disclaimer: your author is the maintainer of this project.)

Here are the 39 precisely defined LoongArch instruction formats
(consult the [loongarch-opcodes documentation][loongarch-opcodes] for meanings of the operand slot names):

[loongarch-opcodes]: https://github.com/loongson-community/loongarch-opcodes

<table class="loongarch-insn-formats">
    <thead>
        <tr>
            <th rowspan="2">Format</th>
            <th colspan="32">Instruction word</th>
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
        <tr><td>CjSd5k16</td><td class="field-opcode" colspan="6"></td><td colspan="16">Sd5k16 low</td><td class="field-opcode" colspan="2"></td><td colspan="3">Cj</td><td colspan="5">Sd5k16 high</td></tr>
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
        <tr><td>JSd5k16</td><td class="field-opcode" colspan="6"></td><td colspan="16">Sd5k16 low</td><td colspan="5">J</td><td colspan="5">Sd5k16 high</td></tr>
        <tr><td>JUd5</td><td class="field-opcode" colspan="22"></td><td colspan="5">J</td><td colspan="5">Ud5</td></tr>
        <tr><td>JUd5Sk12</td><td class="field-opcode" colspan="10"></td><td colspan="12">Sk12</td><td colspan="5">J</td><td colspan="5">Ud5</td></tr>
        <tr><td>JUk8</td><td class="field-opcode" colspan="14"></td><td colspan="8">Uk8</td><td colspan="5">J</td><td class="field-opcode" colspan="5"></td></tr>
        <tr><td>Sd10k16</td><td class="field-opcode" colspan="6"></td><td colspan="16">Sd10k16 low</td><td colspan="10">Sd10k16 high</td></tr>
        <tr><td>Ud15</td><td class="field-opcode" colspan="17"></td><td colspan="15">Ud15</td></tr>
    </tbody>
    <tfoot>
        <tr><td colspan="33">Note: cells with <code>this background</code> represent opcode bits.</td></tr>
    </tfoot>
</table>

As is shown, LoongArch actually has vastly more complex encodings than MIPS or
RISC-V, both of which have about 20 distinct formats at most.
Although some of the LoongArch formats are definitely mergeable (for example
the FdCj and CdFj formats; they are the same if we do not pursue complete
correspondence of operand order in assembler syntax), that ship has sailed;
also the current scheme does conserve a lot of encoding space after all.

### Is the LA464 <abbr title="micro-architecture">µarch</abbr> the same thing as GS464V? Why did it get renamed?

*This answer contains speculations.*

Frankly speaking, the Loongson Corporation does not really put any special
consideration in naming its micro-architectures or cores.
For example, the 3A4000 processor contains 4 GS464V cores, but the cores of
the much earlier 3B1500 are also called GS464V in the documentation.

> Author's comment:
> There is the GS464EV name on [Wikipedia][en-wiki-loongson], and it is coined
> by the community exactly because of the desire to avoid ambiguity.
> The <abbr title="micro-architecture">µarch</abbr> of 3A2000/3A3000 is called
> GS464E; 3A4000, as a "tock"/<abbr title="micro-architecture">µarch</abbr>
> iteration, finally gained usable vector support by implementing
> <abbr title="MIPS&reg; SIMD Architecture">MSA</abbr>,
> hence the GS464EV name.
>
> (The former vector instructions developed in-house are lacking in terms of
> functionality and documentation, so this is why we call
> <abbr title="MIPS&reg; SIMD Architecture">MSA</abbr> "usable".)

[en-wiki-loongson]: https://en.wikipedia.org/wiki/Loongson

As for the LA464/GA464V, there are expressions like
"adjusting <abbr title="instruction set architecture">ISA</abbr> of present
<abbr title="intellectual property">IP</abbr> cores"
(“调整现有 <abbr title="intellectual property">IP</abbr> 核的指令系统”)
that can be seen in earlier public articles or presentations about the
development of the 3A5000 or the LoongArch,
e.g. [the August 2020 keynote by HU Weiwu][hww-pres-202008].
Considering that the 3A4000 and 3A5000 belong to the same tock-tick iteration,
such wording may imply that the 3A5000 is just the 3A4000 with a replaced
decoder.
However, it is not okay to re-use the name, as the instruction set is
incompatible after all; the Loongson Corporation ultimately chose to modify
all of its documentation and open-source code to mass-replace GS464V with LA464
for the new LoongArch model, on August 2021.

[hww-pres-202008]: https://www.bilibili.com/video/BV1BK411T7Za

So, overall it is more appropriate to consider the LA464 and GS464V as a
not-so-similar "pair of twins", with roughly the same micro-architecture, but
different supported <abbr title="instruction set architecture">ISA</abbr>.

> Trivia:
> "GS464" stands for "Godson 4-issue 64-bit".
>
> "Godson", despite its obvious impression for an English speaker, is in fact
> just a sound approximation of "狗剩" (gǒu shèng), "dog leftovers".
> Back in the pre-industrial times, it was believed by some Chinese families
> that newborns with such lowly names are easier to raise;
> this tradition is known in Chinese as "赖名好养活" or "贱名好养活".
>
> The switch to the "LA" prefix is presumably because all "GS" cores
> implemented some variant of MIPS, and the company wanted to cut off this
> relationship, though.

### What's the relationship between LoongArch and MIPS?

(Please note that all <abbr title="Reduced Instruction Set Computing">RISC</abbr>
architectures bear a significant resemblance to each other, because all of them
are made to perform the same thing called "general-purpose computation".)

According to public sources, LoongArch and MIPS cannot interoperate, and there
is no 1:1 correspondence between some of the important architectural features;
though such correspondence exists for many of their instruction semantics.

- LoongArch has entirely different instruction encoding than MIPS.
- LoongArch does not have any form of branch delay slots, while MIPS did not
  gain optional delay-slot-less branches/jumps until R6.
- LoongArch does not feature some of the historical warts of MIPS, for example
  the "wonderful" HI/LO accumulators.
- LoongArch's <abbr title="application binary interface">ABI</abbr> is based on
  that of RISC-V, departing from the MIPS tradition.
  Concepts such as dedicated return value registers and registers reserved for
  kernel use are abolished.

However, there is objective MIPS influence on LoongArch. For example:

- LoongArch uses predicate registers `$fccX` for floating-point comparison and
  branches, which are 8 distinct flag bits; this is the same as MIPS, and
  rarely seen on other modern architectures.
- LoongArch's privileged architecture is similar to that of MIPS. For example,
  the LoongArch <abbr title="Translation Look-aside Buffer">TLB</abbr> has a
  special even/odd entry distinction; this is cumbersome, hence not seen on
  any other prominent architecture but MIPS.
- Some instructions have identical semantics as their MIPS R6 counterparts,
  while similar semantically-identical instructions are not found in any other
  prominent architecture.
  The LoongArch `maskeqz/masknez` and the MIPS R6 `selnez/seleqz` are such an
  example.
- The way some operations are implemented are similar to MIPS R6, only with
  minor changes.
  For example, 64-bit immediates are materialized in 4 segments, and the 4
  instructions used are `lu12i.w/ori/lu32i.d/lu52i.d` for LoongArch (here
  using official mnemonics).
  They only differ from their MIPS R6 counterparts (`lui/ori/dahi/dati`) in
  the length of each segment: for LoongArch it is `12/20/20/12`, while for
  MIPS it is `16/16/16/16`.
  Also, this particular way of materializing immediates is not seen on any
  other prominent architecture.
- The Loongson Virtualization Extension is abbreviated as LVZ which is
  extremely dubious.
  Because "Loongson SIMD Extension" is LSX, "Loongson Advanced SIMD Extension"
  is LASX and "Loongson Binary Translation Extension" is LBT (asymmetry here;
  it should have been called LBTX), the virtualization extension should be
  abbreviated LVX or LV; in no way it is conformant to pick two letters from
  the second word to get LVZ. VZ is MIPS's name for its virtualization ASE!
- The LoongArch assembler syntax is similar to that of MIPS.
  Parentheses around memory operands are removed, but registers still have to
  carry a `$` prefix, and pseudo-instructions such as `move` are named after
  the MIPS counterparts, different from RISC-V etc.
- Early LoongArch ports of fundamental software such as the toolchain or the
  Linux kernel are basically just copy-pastes of MIPS code, mass-replacing
  "MIPS" with "LOONGARCH" along the way.
  (Of course, because the quality of such code is bound to be low, and the two
  architectures are not *that* similar after all, the Loongson Corporation
  stopped doing this not before long.)

### What's the relationship between LoongArch and RISC-V?

(Please note that all <abbr title="Reduced Instruction Set Computing">RISC</abbr>
architectures bear a significant resemblance to each other, because all of them
are made to perform the same thing called "general-purpose computation".)

According to public sources, LoongArch and RISC-V cannot interoperate, and
there is no 1:1 correspondence between some of the important architectural
features; though such correspondence exists for many of their instruction
semantics if certain conditions are met (restricted to 64-bit operation, for
example).

- LoongArch's privileged architecture and memory management are significantly
  different to those of RISC-V.
- The supported operations of LoongArch base <abbr title="instruction set architecture">ISA</abbr>
  are mostly a superset of its RISC-V counterpart.
- RISC-V always sign-extends its immediate operands, while LoongArch
  differentiates based on type of operation (sign-extending for arithmetic
  operations; zero-extending for logical operations).
- LoongArch has opcodes starting from <abbr title="most significant bit">MSB</abbr>,
  precluding compressed instruction words in the RVC way.

There is significant RISC-V influence in the software part of LoongArch, such
as the <abbr title="application binary interface">ABI</abbr> and several
fundamental toolchain pieces.
LoongArch's <abbr title="application binary interface">ABI</abbr> is rather
similar to RISC-V's, and the semantic similarities of instructions are notable
as well.
Often, simple syntactic tweaks to the RISC-V version are all it takes to port
a primitive to LoongArch for some fundamental software.

Some LoongArch instructions have identical semantics as their RISC-V
counterparts; some of the architectural features are similar as well.
For example:

- The <abbr title="position-independent code">PIC</abbr>-related `pcaddu12i`
  behaves the same as the RISC-V `auipc`.
- The register jump `jirl` behaves the same as the RISC-V `jalr`,
  very unlike the MIPS `jalr`.
- The timekeeping instructions `rdtime.*` are semantically similar to their
  RISC-V counterparts in that they all return values from a constant-frequency
  counter.
- LoongArch's privileged resources live in the
  <abbr title="control status register">CSR</abbr> space, and the
  <abbr title="control status register">CSR</abbr> concept obviously comes from
  RISC-V.
  This is already the case back to 3A5000's predecessor, 3A4000.
- RISC-V originally defined 4 privilege levels (from high to low,
  Machine/Hypervisor/Supervisor/User; Hypervisor was later removed), and
  LoongArch defines 4 too (from high to low, PLV0/PLV1/PLV2/PLV3).
  However, LoongArch OSes run at the highest level of PLV0, while it is
  recommended for RISC-V OSes to run at the Supervisor level.

And these are possible influences of RISC-V to LoongArch as well.

### How many <abbr title="application binary interface">ABI</abbr>s do LoongArch have?

LoongArch currently defines 3x2=6 <abbr title="application binary interface">ABI</abbr>s,
according to [the LoongArch ELF psABI][elf-psabi-doc-html].

[Data models][data-models] of which are:

[data-models]: https://en.wikipedia.org/wiki/64-bit_computing#64-bit_data_models

- ILP32 (`int`, `long` and pointers are 32-bit wide; a 32-bit model but not completely excluding 64-bit operations)
- LP64 (`long` and wider types and pointers are 64-bit wide; this is the most common 64-bit data model in Linux space)

And the floating-point support are:

- Soft-float (S)
- Single-precision hard-float (F)
- Double-precision hard-float (D)

Currently only the LP64D <abbr title="application binary interface">ABI</abbr>
is fully supported.
All publicly available commercial distributions for LoongArch are built with
this <abbr title="application binary interface">ABI</abbr>.
If you attempt to use the other <abbr title="application binary interface">ABI</abbr>s,
you are very likely to get all kinds of compilation errors, so usage of these
<abbr title="application binary interface">ABI</abbr>s is not recommended at
this early stage of bring-up.
In particular, the support for the ILP32 <abbr title="application binary interface">ABI</abbr>s
are known to be very incomplete,
and it is extremely likely that builds will just error out immediately if one
ever try.

[elf-psabi-doc-html]: https://loongson.github.io/LoongArch-Documentation/LoongArch-ELF-ABI-EN.html

### What happened to LoongArch's vector extension?

*This answer is speculative because the relevant documentation has not been released.*

The 3A4000 from the end of Loongson's MIPS era contains a complete implementation
of MIPS's <abbr title="MIPS&reg; SIMD Architecture">MSA</abbr> vector extension.
In addition to that, the 3A4000 also has support for the LoongMMI which is
inherited from the 2F era, and the LSX/LASX that never appeared in public
documentation.
Let's summarize all these vector extensions:

- MSA: 128-bit fixed vector width, according to [the MSA64 documentation v1.12][MD00868-1D-MSA64-AFP-01.12].
- LoongMMI: usage extremely similar to the x86 MMX; 64-bit fixed vector width.
- LSX/LASX: public information nearly non-existent aside from a few PPT slides,
  open-source toolchain code only briefly and quietly appearing before being
  redacted.
  LSX should have a fixed vector length of 128-bit, while LASX should have 256.

[MD00868-1D-MSA64-AFP-01.12]: https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MD00868-1D-MSA64-AFP-01.12.pdf

As can be seen, all the implemented vector instructions operate on fixed
vector lengths.
Taking the description of the `LSX` and `LASX` bits in the
*LoongArch Reference Manual, Volume 1*, Section 2.2.10.5 Table 3
"The configuration information accessible by the CPUCFG instruction"
into consideration
("128-bit vector extension" and "256-bit vector extension" respectively),
it is presumed that LoongArch's LSX/LASX are similar to the LSX/LASX from the
MIPS era; at least the vector width should be fixed as well.
The instruction encodings must have been changed, and some instructions may
get added or removed as well;
there is no public documentation and open-source support after all,
so no external code makes use of these,
and compatibility is not a concern in this case.

Note that novel vector extensions in the recent years are all scalable, such
as the AArch64 SVE and the RISC-V RVV:
software is able to dynamically configure the vector unit to pick the vector
width most suitable to the requirement at hand, also meaning software does not
need to be modified to take advantage of wider hardware implementations.
This is generally a welcomed trend,
and we noticed [a change preparing for scalable vectors][loongson-glibc-scalable-vec-clue]
in Loongson's glibc fork.
Considering there may be multiple reasons for not releasing the LSX/LASX to
the public (especially IP concerns), this might mean that LSX/LASX would never
become public, and that a scalable vector implementation similar to RVV would
be available at some future time.

[loongson-glibc-scalable-vec-clue]: https://github.com/loongson/glibc/commit/02cae44d5f05a06cba72458cf33d4a21b3813e3c


### What happened to LoongArch's binary translation extension?

*This answer is speculative because the relevant documentation has not been released.*

Similar to the case of vector extension, we can speculate based on the binary
translation extension from the MIPS era.
Although there is no public instruction encodings nor kernel support, we
actually already had a sneak peek at the extension,
by means of some [academic report][syuu]
or public presentations done by Loongson themselves
([the August 2020 keynote by HU Weiwu][hww-pres-202008],
[the April 2021 presentation by ZHANG Fuxin][foxsen-pres-202104]):

[syuu]: https://www.slideshare.net/syuu1228/hardware-assited-x86-emulation-on-godson-3-5040660
[foxsen-pres-202104]: https://www.bilibili.com/video/BV1KZ4y1c7kQ

- New architectural state of the EFLAGS register is added, along with
  purely EFLAGS-updating counterparts for some basic instructions;
- New architectural state of the TOP register is added, along with the
  corresponding FPU mode bit; semantics of FP register operands is altered to
  be TOP-based if the x87 emulation mode is enabled.

Loongson later added support for other operations too, such as the ARM
conditional execution, and the approach should be similar.
So, the x86 and ARM translation aid of LoongArch is likely to be minor tweaks
to the previous binary translation extension.
As for the translation of MIPS, because both MIPS and LoongArch are classical
<abbr title="Reduced Instruction Set Computing">RISC</abbr> designs,
branch delay slots may be the only hardware aid needed.
(Other weird MIPS features such as HI/LO registers are easily implemented in
software at translation time, because you have to recover the data flow
regardless.)

## About software development

### There seems to be many organizations related to Loongson/LoongArch on GitHub. Which of these are "official"?

You may have seen one of these organizations already:

* The ["Great Loongson Union" (loongson)][org-ls] (your author really dislikes the title btw),
* The [LoongArch porting group (loongarch64)][org-la64], and
* The [Loongson Community (loongson-community)][org-l-c].

[org-ls]: https://github.com/loongson
[org-la64]: https://github.com/loongarch64
[org-l-c]: https://github.com/loongson-community

Long story short: The list is in decreasing "officiality", but as with nearly
everything Loongson, "officiality" may or may not be something you would want.

Or if you prefer the long story...

In the beginning, the Loongson Corporation has no presence on GitHub (or any
of the "international" code forges) at all, so at 2015-07-14, a group of
disgruntled open-source developers set up [the loongarch-community
organization][org-l-c] as a central place for collaboration.
Almost all organization members have no affiliation with the Loongson
Corporation; in part because of this, and in part because this particular way
of making technical decisions and doing things is not agreed by some of the
Loongson people, the Loongson Corporation never officially acknowledged this
organization as its "community", even to this day. You know, it is hard for
the company to officially recognize the community when it housed goodies like
[reverse-engineered docs for the 3A4000's crypto instructions][3a4000-crypto-ase],
[reverse-engineered LoongArch instructions even before the official manual release][unofficial-reversed-insns],
and [collection of other docs][l-c-docs] free for download with the official
website now requiring registration (read: business lead) for access to
any documentation...

[3a4000-crypto-ase]: https://github.com/loongson-community/loongson-3a4000-crypto-ase
[l-c-docs]: https://github.com/loongson-community/docs

Fast forward to 2020, when the LoongArch was already announced at August, but
without any open-source code drops yet; longtime MATE developer and open-source
contributor [@yetist](https://github.com/yetist) was hired by the Loongson
Corporation to work on bringing up the LoongArch.
Seeing that there was not a single *recognized* community out there that their
colleagues would like to participate in, naturally, they set up [the
loongarch64 organization][org-la64] for facilitating early code reviews, at
2020-09-29, just before the National Day holiday.
Many people from different backgrounds are invited to the organization;
many are Loongson employees, but there are also Deepin/UOS employees and
many unaffiliated developers.
Internal procedures are set up to ensure quality of submissions; code review
is required, and at least 3 approvals are required before merging any PR.
Loongson employees are not exempt from the rules, and there has not been any
violation so far.
Although there are low-quality reviews or even blind LGTM's from time to time,
they are invariably caught by the more prudent reviewers.

Later, in 2021 (perhaps triggered by the need to upstream the Go loong64 port,
but your author's memories may be failing him),
some *other* group (maybe a different department) inside Loongson found also the
need for a GitHub organization, and discovered that they had already
registered [the loongson organization][org-ls] back at 2020-01-01 but had not
made any use of it.
For unknown reasons, they did not pursue cooperation with the loongarch64
effort; instead they just quietly began their work on "their" organization.
No invitations was ever extended to non-Loongson employees, and team
structures seemed like replication of the corporate organizational structure.
Code reviews are also mandated and it is the same 3-approvals rule for merging,
but FWIW blind and/or rushed LGTM's are more common than in loongarch64.
There are cases where PRs are merged with little discussion, or closed without
any comment; the latter is already considered impolite in community etiquette.
Changes not "approved" by Loongson are unlikely to be merged, and it seems
there will be a CLA in place for external contributors soon.
All in all, this organization is more about internal collaboration and bug
reporting than community participation; for code contributions, it may be
better to submit directly to the respective "true" upstreams instead.

> Trivia:
> A quick way to compare the openness of the three organizations is to look at
> the access level of your author.
> Your author is an *owner* of the loongson-community organization, an ordinary
> member of the loongarch64 organization *but with write access*, while *not*
> a part of the loongson organization at all; and that tells a lot!

### Are the various LoongArch ports upstreamed already?

There are *many* pieces, all with varying upstream statuses;
some are progressing smoothly, while some are under heated discussion.
Your author has summarized the situation with the tables below.

Table legend:

* :white_check_mark: -- upstreamed and released
* :hourglass_flowing_sand: -- upstreamed, pending release
* :mag: -- under upstream review
* :wrench: -- WIP, or under community pre-review before first upstream submission
* :x: -- TODO

(Based on information as of 2022-03-30.)

#### Emulator and firmware

|Project|Status|Dev repository|Notes|
|-------|:----:|--------------|-----|
|QEMU (target)|:mag:|[Loongson fork](https://github.com/loongson/qemu/tree/tcg-dev)|For emulating LoongArch on other arches.|
|QEMU (TCG host)|:hourglass_flowing_sand:|[xen0n fork](https://gitlab.com/xen0n/qemu/)|For emulating other arches on LoongArch hosts; [patch series](https://patchew.org/QEMU/20211221054105.178795-1-git@xen0n.name/) [already merged](https://gitlab.com/qemu-project/qemu/-/commit/8c5f94cd4182753959c8be8de415120dc879d8f0). Will appear in QEMU 7.0.|
|EDK II|:wrench:|[Loongson fork](https://github.com/loongson/edk2)||

#### Kernels

|Project|Status|Dev repository|Notes|
|-------|:----:|--------------|-----|
|Linux|:mag:|[loongarch-next](https://github.com/loongson/linux/tree/loongarch-next)|The [fork at kernel.org](https://git.kernel.org/pub/scm/linux/kernel/git/chenhuacai/linux-loongson.git/?h=loongarch-next) is outdated.|
|FreeBSD|:x:|-||
|OpenBSD|:x:|-||
|[RT-Thread](https://www.rt-thread.org)|:x:|-|This is an original Chinese RTOS; relationship between its parent company (上海睿赛德电子科技有限公司) and the Loongson Corporation is good, but no LoongArch porting plan has been announced.|

#### GNU Toolchain

|Project|Status|Dev repository|Notes|
|-------|:----:|--------------|-----|
|binutils|:white_check_mark:|[Loongson fork (v4.1)](https://github.com/loongson/binutils-gdb/tree/upstream_v4.1)|Initial support appeared in 2.38, but is incomplete; <abbr title="processor supplement ABI">psABI</abbr> already incompatibly revised meanwhile.|
|gcc|:hourglass_flowing_sand:|[Loongson fork](https://github.com/loongson/gcc)|Will appear in 12.1.0.|
|glibc|:mag:|[Loongson fork (v2.2)](https://github.com/loongson/glibc/tree/loongarch_2_35_dev_v2.2)||

#### Other toolchain pieces/languages

|Project|Status|Dev repository|Notes|
|-------|:----:|--------------|-----|
|musl|:wrench:|-||
|llvm|:wrench:|[Loongson fork](https://github.com/loongson/llvm-project)|The forked repo does *not* contain up-to-date code; follow [SixWeining](https://reviews.llvm.org/p/SixWeining/)'s activities for progress.|
|rust|:x:|-|Blocked by LLVM.|
|go|:mag:|[Loongson fork](https://github.com/loongson/go/tree/loong64-master)||
|dotnet|:wrench:|-|Porting finished but not open-sourced yet.|
|openjdk|:x:|-|Status unknown.|
|v8|:white_check_mark:|-|[Reviewed and merged](https://chromium-review.googlesource.com/c/v8/v8/+/3089095); released in 9.5.3.|

#### Other infrastructure projects

|Project|Status|Dev repository|Notes|
|-------|:----:|--------------|-----|
|strace|:white_check_mark:|-|LoongArch64 support [has been](https://github.com/strace/strace/pull/205) [merged](https://github.com/strace/strace/pull/207); released in 5.17.|
|systemd|:white_check_mark:|[LoongArch64 porting group fork](https://github.com/loongarch64/systemd)|Basic support appeared in v250 along with new [discoverable partition types][dpt] defined for LoongArch.|
|util-linux|:white_check_mark:||Support for the new [discoverable partition types][dpt] already merged. Released in 2.38.|

[dpt]: https://systemd.io/DISCOVERABLE_PARTITIONS/

### I'm going to port my software to LoongArch. What do I need to prepare for?

**You don't have to specially prepare for anything!**

The expectation is for LoongArch to become a "normal" platform for software
and hardware development.
You just do on LoongArch whatever you used to do for other platforms, such as
x86 or ARM, except for those things inherently platform-specific.

If you primarily develop high-level "business logic" with high-level
programming languages, you almost never need to care about low-level technical
details of the platform.
These kind of things are already taken care of by the open-source community,
consisting of all enterprise and individual developers using Loongson products.

If you are an infrastructure developer yourself, or a "business logic" developer
that occasionally needs to care about low-level details here and there,
[the LoongArch documentation][loongarch-doc-mainpage-html] provided by the
Loongson Corporation is a good starting point.

[loongarch-doc-mainpage-html]: https://loongson.github.io/LoongArch-Documentation

### What does LoongArch's target tuple look like?

First of all, we need to differentiate between the GNU target tuples and the
Debian multi-arch tuples, because the two are not always the same;
in particular, for targets supporting multiple
<abbr title="application binary interface">ABI</abbr>s, this fact is guaranteed
to be reflected in the Debian multi-arch tuples.
A complete target tuple looks like `ARCH-VENDOR-OS-ENV`, but the vendor field
is often omitted because few contemporary architectures make use of it, making
it `ARCH-OS-ENV` instead; this short form is also called the *target triplet*.

The most common configuration for a LoongArch system is one running Linux with
the LP64D <abbr title="application binary interface">ABI</abbr> and glibc.
According to [the LoongArch toolchain convention][tc-conventions-doc-html],
the Debian multi-arch tuple for this configuration is `loongarch64-linux-gnuf64`.
The corresponding GNU target tuple is `loongarch64-unknown-linux-gnu`;
the `unknown` part can be dropped.
(The <abbr title="application binary interface">ABI</abbr> suffixes for
floating-point support and extensions can be omitted, if the configuration is
the most common for the given ARCH.)

> Note: You may have seen [this change to gnuconfig from late 2020][gnuconfig-202012],
> which differs from the latest spec:
> no consideration for the <abbr title="application binary interface">ABI</abbr>
> floating-point or extension suffixes, and a mysterious `loongarchx32` check.
> This is because the change reflected the earliest understanding of the
> LoongArch <abbr title="application binary interface">ABI</abbr> inside the
> Loongson Corporation:
> the three ARCH values `loongarch32` `loongarch64` `loongarchx32` corresponds
> 1:1 to the three MIPS <abbr title="application binary interface">ABI</abbr>s
> o32 n64 and n32.
> Of course, people finally realized there is absolutely no reason to blindly
> copy MIPS when you are starting from scratch after all,
> so the <abbr title="application binary interface">ABI</abbr> was re-modeled
> after that of RISC-V;
> the so-called "x32" <abbr title="application binary interface">ABI</abbr> for
> LoongArch will never get implemented as a result.

[gnuconfig-202012]: https://git.savannah.gnu.org/gitweb/?p=config.git;a=commitdiff;h=c8ddc8472f8efcadafc1ef53ca1d863415fddd5f;hp=05734c3b30b02196506617b4e4d4b70b3bf4bb72


### What does LoongArch's GOARCH value look like?

The Loongson Corporation [had an argument][golang-go-46229] with the community
about the topic back in mid-2021. :satisfied:

The Loongson team ultimately accepted the community proposal though, so the
GOARCH for the LA64 is confirmed to be `loong64`.
Because 32-bit support is still missing here and there, there is no such thing
as `loong32` at the moment.

[golang-go-46229]: https://github.com/golang/go/issues/46229

### How do I quickly familiarize myself with LoongArch assembly?

The manual and the <abbr title="application binary interface">ABI</abbr> spec
are your friends :wink:

Syntactically, LoongArch's assembly language is basically a simplified version
of MIPS assembly, but there are a few important differences as well.
Based on personal experiences,
it is easy to quickly on-board oneself by "thinking in RISC-V while writing MIPS";
this, coupled with manual reading, it is easy to master the language as well.

* Registers must be prefixed with `$`, like MIPS.
  (In RISC-V assembly this is not necessary.)
* The <abbr title="application binary interface">ABI</abbr> divides registers
  into three classes `$a*` `$t*` `$s*`, like RISC-V.
  (Different from MIPS; there is no distinct `$v*` nor `$k*`.)
* The way of doing <abbr title="position-independent code">PIC</abbr> is the
  same as RISC-V, different from MIPS.
  (The abicall convention is a compromise to the limited functionality of the
  pre-R6 MIPS <abbr title="instruction set architecture">ISA</abbr>, and as
  such, there is no point carrying it over to the new era.)
* The way of doing <abbr title="thread-local storage">TLS</abbr> is the same as
  RISC-V.
  (Different from MIPS; LoongArch has the dedicated `$tp` register so it is no
  longer necessary to workaround this with things like `rdhwr`.)
* The register move pseudo-instruction is called `move`, like MIPS.
  (Different from x86 or RISC-V; `mov` or `mv` are not recognized.)
* The no-op is spelled `nop` as with most architectures.
  (Syntactic sugar for `andi $zero, $zero, 0`.)
* Return from subroutine is `jr $ra`, like MIPS.
  (Syntactic sugar for `jirl $zero, $ra, 0`; different from RISC-V, there is
  no `ret` as an additional syntactic sugar as of 2022-03-06.)
* Different from MIPS, there are no parentheses around registers that represent
  memory operands.
  (`ld $a0, 16($a1)` becomes `ld.d $a0, $a1, 16`.)
* A width suffix is needed for the `li` pseudo-instruction as well.
  (`li.w` suffices most of the time; it is seldom necessary to load constants
  wider than 32 bits.)
* As for operand ordering of instructions, most follow the rule of registers
  before immediates, and from <abbr title="least significant bit">LSB</abbr> to
  <abbr title="most significant bit">MSB</abbr> in each group.
  Note that there are exceptions if using manual syntax!

Aside from these, there are some known inconsistent, misleading or even
errorneous descriptions existing in the current version (v1.00) of the
<abbr title="instruction set architecture">ISA</abbr>
manual, due to Loongson not soliciting reviews from the wider community before
publishing the manuals.
These are all described in the [loongarch-opcodes] project's documentation.

> Author's comments:
>
> The loongarch-opcodes review feedbacks are already sent back to relevant
> teams at Loongson. But they replied with something like "It's impossible to
> modify the manuals like that now, after publication, in part also because
> there's no precedent of any other company doing this such as Intel or ARM;
> developers just have to take some more time to get accustomed" :smirk:
> As if developers inside Loongson actually had similar expertise as their
> fellow Intel or ARM developers, and that everything is done correct in one
> go.
> Or do they?
>
> Regardless, your author and other friends in support of the project are
> still actively communicating and pushing every fix and improvement forward,
> in hopes of eliminating as many warts as possible before LoongArch is known
> to a wider audience. We do not want future developers to fall for the same
> traps that we had already fallen into.

### I'm using C/C++. How do I specify the CFLAGS on LoongArch? How to conditionally compile for LoongArch and its features?

Please consult [the LoongArch toolchain convention][tc-conventions-doc-html].

[tc-conventions-doc-html]: https://loongson.github.io/LoongArch-Documentation/LoongArch-toolchain-conventions-EN.html

### I don't have LoongArch hardware. How do I test my software on it nevertheless?

You could use QEMU for this most of the time.
Both system emulation (emulating a complete LoongArch computer) and user-mode
emulation (emulating a LoongArch Linux syscall interface on top of the host
Linux kernel) are supported.
Usage of QEMU is outside the scope of this documentation; consult other online
resources for that.

Note: As of 2022-03-06, target support for LoongArch is not upstreamed yet.
This means you would have to compile
[Loongson's development branch][qemu-loongson-tcg-dev] yourself.

[qemu-loongson-tcg-dev]: https://github.com/loongson/qemu/tree/tcg-dev

## About usage

### What's the Gentoo ARCH for LoongArch systems?

Gentoo has assigned `ARCH=loong` for LoongArch, according to [the upstream communication back in August 2021][gentoo-dev-mail-202108].
This means you are going to write things like `ACCEPT_KEYWORDS="~loong"`.

And this time everything went smoothly, unlike the Go situation. :rofl:

[gentoo-dev-mail-202108]: https://archives.gentoo.org/gentoo-dev/message/388a4b7428461660e89c8eae8c292f32

### What firmware/BIOS does LoongArch systems use? How do I manage boot options? What bootloader do I use?

The "BIOS" concept is already obsolete for a millenia, why do people still call firmwares as such? :facepalm:

Aside from that, both desktop and server LoongArch systems comply to the UEFI specification, and both use ACPI to communicate information about devices.
Unlike the earlier ad-hoc MIPS UEFI implementation that was never upstreamed, the UEFI and ACPI implementations for LoongArch have already completed the upstream process, and will be officially supported starting from the next release of the specs. Congratulations to Loongson's firmware team BTW!

The LoongArch UEFI implementation is fairly standard. This means things are more-or-less the same as the other UEFI platforms such as x86 or ARM64, regarding boot options management and bootloader choice and usage.
Whatever (reasonably portable piece) you currently use on the other platforms, like efibootmgr, systemd-boot, grub2, Linux EFI stub, etc., it is (or should be) the same on LoongArch!

### What GPUs can be used on LoongArch systems?

As of 2022-03-06, there is no LoongArch CPU in SoC form, so every LoongArch
system out there invariably includes a bridge chip.
At this time point, there is only one model of bridge chip, the LS7A1000,
that can work with the only LoongArch CPU in existence -- the Loongson 3A5000;
this bridge chip includes a GPU block that is based on the Vivante GC1000,
together with an in-house display controller block.
Upstream work for this integrated GPU is currently in progress.
(The etnaviv driver cannot work as-is.)

As for compatibility of discrete GPUs, basically *any GPU with open-source
driver* will work if the required firmware is present on the system, typically
installed with the linux-firmware package.
Of course this largely eliminates the green camp, because the chance for a
LoongArch blob is slim (blame Jensen Huang), and the open-source nouveau is
borderline unusable (also blame Jensen Huang).
AMD Yes!

### What soundcard/network interface card/capture card/mouse/keyboard/HDD/`$INSERT_YOUR_PERIPHERAL` can be used on LoongArch systems?

You can use the said hardware as long as it has open-source Linux support.
Closed-source drivers that have LoongArch versions are fine too, if the vendor
happen to be so merciful as to provide LoongArch blobs; or if you are some
powerful figure who can persuade the vendor into providing such blobs.

If a particular piece of hardware does not work even if a LoongArch driver
exists, tell us about it in any of the LoongArch user community; you can be
sure a developer will see it. :wink:

## About the LoongArch ecosystem

### Which Linux distributions have been ported to LoongArch?

Thanks to prioritized hardware access and team collaboration provided by the
Loongson Corporation, the commercial development around LoongArch is
progressing very rapidly.

As of 2022-03-06, multiple commercial distributions (developed by China
mainland entities) already provide LoongArch ports.
These include but are not limited to: (in alphabetical order)

- Kylin (from [the Kylin Software Corporation][kylin-website]; website is Chinese-only)
- Loongnix (from [the Loongson Corporation][loongson-website]; website is Chinese-only)
- UOS (from [the UnionTech Corporation][uniontech-website]; website is Chinese-only)

[kylin-website]: https://kylinos.cn
[uniontech-website]: https://www.uniontech.com

[Loongnix][loongnix-home] claims to be the "Linux OS from the Loongson
open-source community", but because there are actually very few external
participants if at all, and some of its packages are not open-source
(especially the toolchain; the current Loongnix LoongArch port even has vector
extension support!), this distribution is in effect a commercial one.

[loongnix-home]: http://www.loongnix.cn

After the publication of the various LoongArch documentation, and
open-sourcing of Loongson forks of fundamental pieces of software,
the porting pace of community distributions has accelerated as well.

There are several ongoing porting efforts as of 2022-03-06, including but
not limited to: (in alphabetical order)

- Arch Linux
- CLFS
- Gentoo

### Why can't I run closed-source software like WPS Office on community distributions? (aka What's this so-called "old world" and "new world"?)

As of 2022-03-06, all commercial LoongArch distributions are incompatible with
all community distributions.
All binary software built on community distributions, and some software
written in high-level languages and existing in forms like source code or
bytecode (such as those written in Python or Java) cannot run on commercial
distributions, and vice versa.
All closed-source software from
<abbr title="independent software vendor">ISV</abbr>s such as WPS Office are
built on commercial distributions, so they are extremely unlikely to work
as-is on community distributions.

This is the so-called compatibility problem between the *old-world* and the *new-world*.
Because the Loongson Corporation finished all commercial moves before
announcing the LoongArch to the open-source community, the open-source
LoongArch ecosystem is *the new world*; in contrast to this, all commercial
distributions and the ecosystem associated make up *the old world*.
The two worlds are to be united eventually, but are two parallel universes for
now; and the technical difficulty of making the two worlds compatible with
each other is enormous.

As for the reason for two worlds and ways to be compatible, that is a long
story ;-)
Let's save this for another article, dedicated to the topic and to be written
shortly.

### What LoongArch hardware can I buy?

Although international ways of purchasing Loongson products has largely died
out after the 2F era (when international marketing of Loongson products were
taken care of by STMicroelectronics),
at least in China mainland, you can easily get your hands on various products
with LoongArch CPUs, all of which are publicly available.
For example, there are ATX boards, prebuilt computers and notebooks with the
3A5000; and there are rack-mounted servers for the 3C5000L.

This document cannot provide any link to actual products or shops, due to your
author having no affiliation with them, but you can always search for "龙芯"
yourself on popular Chinese shopping sites like ○宝, ○东 or ○鱼 (you will know
the exact names if you have literally any clue about the Chinese language and
the Chinese Internet life in general, or just give this document to one of
your helpful Chinese friends :laughing:).

Note: the Loongson products are almost always significantly more expensive
than similarly specced "mainstream" x86 or ARM products, due to the small
production volume. On top of that, there are more fundamental problems for
the Loongson platform to solve at this early stage of development, so it is
*not* recommended for casual users to buy.

### How can I get acquainted with other fellow LoongArch fans?

Communities exist for any technology with users, and LoongArch is no exception
(your author and his friends are not cats, after all).

There are a lot of places on the Internet where Loongson and LoongArch topics
are discussed. Some places frequented by many people are (but not limited to):

- [Forum of the Loongson Open-source Community](http://bbs.loongnix.cn/) (龙芯开源社区论坛) (HTTP-only due to technical reasons; Chinese-only)
- [Loongson Bar on Baidu Tieba](https://tieba.baidu.com/f?kw=%E9%BE%99%E8%8A%AF&ie=utf-8) (百度贴吧龙芯吧) (Chinese-only)
- [Telegram Loongson group](https://t.me/loongson_users)（Chinese & English）
- QQ group 922566903 (Chinese-only)

There may be other QQ groups discussing Loongson topics, but your author does
not use QQ so he does not know the number.
(PM and PRs are welcomed for suggesting more of them!)

Note that these public venues are better suited to general chatter, instead of
serious technical discussion.
Because some of the end-user fans take rather radical technical/political
positions, technical discussions may easily get derailed if any of the more
sensitive topics is inadvertently touched.
However, you should be able to find the appropriate place for communication
between developers if you possess the desired communication attitude and
ability; due to this, links to such places are left out for now. ;-)
