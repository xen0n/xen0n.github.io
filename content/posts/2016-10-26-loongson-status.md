---
title: '关于独立自主与生态系统 (1): 2016 龙芯现状'
date: 2016-10-26T15:44:00+08:00
draft: false
---

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">知识共享署名-相同方式共享 4.0 国际许可协议</a>进行许可。

应[百度龙芯吧][loongson-tieba]吧友的热情（填坑）要求，此为第一篇填坑之作，
主要描述作者个人从开源社区参与者角度所观察到的龙芯生态系统.
预计本系列将总共写作三篇；
接下来作者将分析 AArch64（ARM64）这个新生架构的生态系统搭建过程，
最后重新回到国产 CPU、自主标准与生态系统之间各种联系与坑的探讨.

[loongson-tieba]: http://tieba.baidu.com/f?kw=%E9%BE%99%E8%8A%AF&ie=utf-8

以下文字时而技术而严肃，时而思辨而感性，这是作者第一次开大坑，希望各位多多指教.

那我们开始吧，从代码开始.

**勘误**

* 结语中原关于 POWER8 与龙芯 3A4000/5000 同时研制的说法系措辞错误，实际要表达的意思是 PowerPC 标准开放不久因此同时经历生态系统建设. 与龙芯 3A4000/5000 同步研制的型号是 POWER10/11. 感谢 [@meJustPlay](http://tieba.baidu.com/home/main?un=meJustPlay&ie=utf-8) 的指正！


## 代码

代码是开源社区存在的前提和交流的基础，先从这里看起.

### 参与深度与广度

整体上，龙芯在代码方面显得外部参与不足；一个首要的原因是硬件普及度不高.
我们用列表的形式梳理一下.

* 非 x86 架构造成不兼容 Windows 导致普通用户对其不感兴趣，
* 导致感兴趣人群与 Linux 高级用户重合，而
    - 中国 Linux 用户
        - 本就稀少，日常使用者更少；
        - 龙芯 2E/2F 产品性能孱弱，形态不佳（上网本），停产；
        - 龙芯 3A 产品性能可以接受，然而价格不具备竞争力；
    - 外国 Linux 用户
        - 支持 x86 （一些 Linux 游戏玩家）的被 x86 捆绑；
        - 支持 MIPS 或至少感兴趣的用户缺乏龙芯的购买渠道；
        - 不可否认一部分用户对中国存在意识形态偏见，认为一切中国处理器都是“政府审查”“国安局后门”“剽窃西方知识产权”等等“阴谋论产物”；
* 最后拥有龙芯设备的非官方、非商业玩家只有以下 Linux 用户：
    - 中国龙芯支持者，
    - 中外 Linux/MIPS 移植者与打包者.

这也就限制了有能力向龙芯软件生态系统做贡献的用户数量.
实际上我们也观察到，为龙芯提供基础移植与适配优化的都是熟悉的面孔，电子邮件地址都以
loongson.cn 或者 lemote.com 结尾.
这并不是一件好事，大家都清楚龙芯的人员规模并不庞大，至少没有庞大到单靠一家公司即可撑起一个操作系统的程度.
我们注意到龙芯并不缺乏合作伙伴（[Loongnix][partner-loongnix]、[梦兰][partner-lemote]）；然而这些玩家几乎都是闭源企业，而我们在谈论开源生态，因此忽略不计.

[partner-loongnix]: http://www.loongnix.org/index.php/%E5%90%88%E4%BD%9C%E8%80%85
[partner-lemote]: http://www.lemote.com/html/about/links/

既然龙芯的生态系统建设目前来看主要玩家就是龙芯官方，我们不妨把目光转向 Loongnix
项目. 从 [Loongnix 的代码仓库][loongnix-cgit]可以感受到，这个项目还是把重点放在龙芯 3 号系列的桌面体验上.
它涵盖了以下几个大类的基础库和应用：

[loongnix-cgit]: http://www.loongnix.org/cgit/

* 固件
    - PMON
    - U-Boot（非重点）
* 内核
    - Linux (2.6.32, 3.10, 4.4)
* 工具链
    - binutils (2.24)
    - gcc (4.4, 4.8, 4.9)
    - glibc (2.20)
    - LLVM/Clang（非重点）
* 基础库
    - zlib
* 基础图形库
    - jpeg, libpng
    - libdrm, libXft, Xorg, pixman, mesa
    - Qt4, Qt5
* 浏览器
    - Firefox (24, 40, 45)
    - Chromium (31, 39, 52)
* 多媒体
    - FFmpeg/libav
    - libvpx, openh264
    - mplayer

考虑到龙芯的人力与财力如此受限，却能够完成如此之多如此之广泛的适配工作，堪称了不起的成就.
然而这其中存在许多隐患，这要结合具体代码具体分析.


### 代码细节

简单来讲：

* 不要赶时间；
* 没有谁要承担责任，但所有人都多多少少脱离不了责任；
* 尽管如此，有些东西不是一朝一夕能够解决的，有些时候不要在意一城一地的得失；
* 技术负债（technical debt）都是一点一滴积累出来的，希望所有从业人员谨记
    - 破窗效应，
    - 马蹄铁的铁钉与国家兴亡之间的关系.

一言以蔽之，龙芯的官方人员在用开发闭源软件的心态来开发开源软件，这导致龙芯适配代码的质量普遍较低.
具体体现在 Git 操作上、提交内容上、开发方法论上，就是一团乱麻，各种错误和混沌交织在一起，互为因果：

* Git 库不做正确的 fork，而只是随便解包一个 release 就当成根提交，造成
    - 合并上游补丁变得困难，提交历史不清，使得
    - 无法高效跟踪上游开发，merge/rebase 上游动态，使得
    - 自制补丁不能跟住上游，并且
    - 随着时间推移，向上游提交并被接受显得愈发困难. 这就导致了
* 各种软件，尤其最基础的软件（Linux、工具链等）
    - 不能保持同步，只能跟住一两个稳定版，并且还可能落后（Linux 内核），
    - 有时与上游产生重复劳动；重要 bug 修复上不去、下不来
        - Linux 多个 3A2000 适配补丁其实上游已经有了
        - 4.7 上游第一次合并 3A2000 支持补丁在梦兰板子上不能启动，说明有些关键补丁没上去
        - 4.4 以来上游对 MIPS KVM 以及大量驱动等的优化没下来
        - 显然前两天爆出的 Dirty COW 修复也没下来
        - GCC o32 奇数号浮点寄存器问题上游已经在 `-march=loongson3a` 解决，龙芯的解决方案是过分简单的（对所有 `march` 选项都打开了）
        - binutils 龙芯扩展 128 位访存指令操作码修复没上去
        - GCC 128 位访存序跋优化没上去
        - GCC 上游的浮点寄存器序跋生成适配没下来
    - 由于一些重要修复上不去的原因，导致了更多的重复劳动和合并冲突
        - ffmpeg 与 mplayer 汇编优化中显然有避免使用错误寄存器，而让编译器自己分配寄存器的提交
        - 可惜合并冲突了，因为上游在优化的时候并没有这么想
* 复制粘贴编程
    - PMON 的 target 定义
    - GCC 128 位访存序跋优化的原提交
* 知其然不知其所以然编程
    - binutils 修复 LL/SC `sync` 屏障，[一开始的做法][binutils-llsc-loongnix]对已经有 `sync` 的地方会多插一个
    - [我的修复][binutils-llsc-mine]在正确的位置（实际添加指令的地方）跟踪汇编器状态
    - [Loongnix 修复][binutils-llsc-loongnix-take2]在错误的地方跟踪状态（太高层了！），导致[碰到了标签就悲剧的情况][binutils-llsc-loongnix-tragedy]
    - 至于提交消息只写了个 Fixed bug 的情况这个之后再详细说

[binutils-llsc-mine]: https://github.com/xen0n/binutils-gdb/commit/25f26fc06e904323434981037e93a9df7b131ee2
[binutils-llsc-loongnix]: http://www.loongnix.org/cgit/binutils-2.24/commit/?id=6305c1a63ea663d2016d0872c66ec5ed5e7aa559
[binutils-llsc-loongnix-take2]: http://www.loongnix.org/cgit/binutils-2.24/commit/?id=7ceddd13425ef91b8261dd72c99b5d71566fd828
[binutils-llsc-loongnix-tragedy]: http://www.loongnix.org/cgit/binutils-2.24/commit/?id=e2adbabdfa052937333811e77aac4d90980d868a

以上是简单的吐槽，是作者 8-9 月份拿到 3A2000 板子兴趣盎然地适配过程中观察到的现象.
提到的问题在作者自己的分支中都多多少少得到了解决（工作量特别大的，比如 Linux 移植，作者也偷懒了；大部分提交没有改），欢迎龙芯官方参考与合作.

这里并没有贬低龙芯工作人员，没有任何这个意思；虽然作者还没有参加工作，但作者同样接过单子，同样被赶过
deadline，最严重的时候一周只有 2 天左右可以睡觉，个中辛苦 IT 从业人员都清楚.
作者只是如实描述作者在龙芯代码库的见闻，多数其实是闭源代码的共性，作者自己少量不开源的项目也存在同样问题（滑稽）.
然而这种质量的代码不可能被上游接受，结果所谓的开源合作就退化成自说自话，这就引出了我们下一个要讲的点.


## 交流与标准

AArch64 架构初始适配的时候，ARM 工程师、发行版志愿者、手机厂商站在一起，用英语交流，这是一个年轻的架构.

Google 刚刚宣布 Fuchsia 操作系统不久，[开发者][rust-fuchsia-1][与 Rust 社区][rust-fuchsia-2][站在一起][rust-fuchsia-3]，用英语交流，这是两个年轻的项目.

[rust-fuchsia-1]: https://github.com/rust-lang/rust/pull/37261
[rust-fuchsia-2]: https://github.com/rust-lang/rust/pull/37313
[rust-fuchsia-3]: https://github.com/rust-lang/rust/pull/37387

Intel、AMD、nVidia 等硬件厂商推出新 CPU 抑或 GPU 架构的时候，工程师与编译器社区、图形社区站在一起，用英语交流，这是一群成熟的行业玩家.

与此同时，龙芯等厂商在中国，跟一群闭源厂商，关上门用汉语交流. （申威有军事背景，而我们在讨论开源；依然忽略不计.）

如果实力暂时无法与业内老牌玩家同台竞技，暂时不能像电信行业一样制定自己的标准，至少也应该在标准的制定过程中发出声音.
这样至少我们能够获得谈判的筹码；毕竟标准制定过程都是开放的，如果真的受到无视或者排挤，我们不妨抓住机会进行一波宣传攻势，开源社区会听见你的声音.
而你不去交流，即使开展交流，语言却是破碎的英语，姿态却是丢下一包（提交历史不清、质量肮脏、文档注释的英语破碎……）这样的代码就走，
这样只会损害一个社区官方角色的公信力，对捍卫社区利益毫无帮助.

英语维基百科的技术条目质量一直很高，然而感受下[龙芯的条目][loongson-wiki]，英语世界甚至连 3A3000 存在都不知道，更不知道 Tick-Tock、LoongISA 等等龙芯的基础战略.
由于这些项目的领导结构都不以国人为主，很多我们常用的软件和标准制定者团队也不以国人为主，这就造成一种信息不对称，标准制定的时候不会考虑到你的诉求.
须知诉求的满足并不必然需要“亲爹”，AArch64 和 Fuchsia 的例子固然极端（分别由 Linaro 和 Google 做亲爹），但就以
Rust 项目而言，完全社区开发的 Haiku 操作系统也能[得到][rust-haiku-1][支持][rust-haiku-2]，这就说明我们的不发声找不到借口.

无视标准和参考实现，相应地，标准和参考实现也无视你.

龙芯声称支持的 x86/ARM 协助二进制翻译指令，只有指令名称，具体实现只有龙芯合作伙伴才能看到；QEMU 二进制加速永远停留在论文上.

龙芯 2F 的多媒体加速指令，为 pixman 实现龙芯加速的贡献者[大倒苦水][2f-pixman]，“龙芯 2F 也包括一个 64 位的 SIMD 指令集扩展，跟 MMX 很像……
为什么我不重复使用现有无数软件已经依赖的界面，而非要创建一个不兼容的界面呢？”他指的是 `loongson.h` 这个跟 x86 的 `mmintrin.h` 等一大组头文件作用一样的编译器
intrinsic 函数定义文件. 法律上完全没有问题，因为你在编译器里只是创作那个头文件的衍生作品，跟你硬件如何实现你相应的指令完全没有关系；明明用法差不多，却不实现大家之前都用的界面，这就增加了所有人的工作量.

LoongISA 的 3 操作数乘除法指令，省去了令人心碎的 `mflo` `mfhi` 操作，提高了流水线效率.
然而上文提到，西方世界根本不知道 LoongISA 存在，龙芯官方也不提交上游，于是除了 Loongnix 用户之外的其他用户都不能享受到这些指令.

AArch64（ARM64）想做下一个 x86，但现有的行业标准都是 x86 中心主义，于是他们动手把 ACPI 和 EFI 标准在自己的架构上定义了一遍.
龙芯也有成为下一个 x86 的梦想，至少在中国；龙芯没有完整的 ACPI 支持（至少我在内核里看不到），没有明确的 MIPS EFI 绑定（据说昆仑固件是 EFI 界面的，但一方面我拿不到，另一方面昆仑固件和
PMON 引导的是同样的内核，而内核中我能看到的平台引导代码都是龙芯自制的[固件-内核接口规范][loongson-firmware-intf]代码，这说明
EFI 就算实现了也没有被使用），虽然有个标准，但这对
MIPS 作为整个阵营的竞争力没有太大帮助.

[loongson-wiki]: https://en.wikipedia.org/wiki/Loongson
[rust-haiku-1]: https://github.com/rust-lang/rust/pull/36727
[rust-haiku-2]: https://github.com/rust-lang/rust/pull/36965
[2f-pixman]: http://mattst88.com/blog/2012/05/17/Optimizing_pixman_for_Loongson:_Process_and_Results/
[loongson-firmware-intf]: http://www.loongnix.org/index.php/%E5%9B%BA%E4%BB%B6%E4%B8%8E%E5%86%85%E6%A0%B8%E6%8E%A5%E5%8F%A3%E8%A7%84%E8%8C%83

龙芯 3A4000 乃至 3A5000 生产研发之际，业已开放的 PowerPC 与新生事物 AArch64 的生态系统也在迅猛成长，谷歌大小设备通吃的 Fuchsia 也在逐渐凝固下来……
而 MIPS 阵营依然面临着碎片化，君正主打低功耗，而其指令集覆盖不如龙芯；龙芯支持自主指令集扩展，而自己不开放，别家又不支持（想支持也不知道怎么支持啊）；
MIPS 东家 Imagination 带着一帮小弟搞 MIPS64r6，microMIPS，龙芯和君正又都不支持……


## 结语

似乎全自主的技术路线终究敌不过胜者通吃和规模效应？

那 ARM/Android 当初是怎么顽强生存下来的？

苹果为何能实现 M68k 到 PowerPC 到 x86 的两次华丽转身？

好像站在各自的立场，它们当初也面临着相似的生死考验，为什么我们就活不下来他们就可以？

在本系列的下一篇中，作者将尝试描述 AArch64 架构的发展时间线，并简单分析它背后的原动力.

在任何困境中不要放弃希望，想想两万五千里长征，想想新世纪初的韬光养晦.

或者换一种思路，就像《三体》中描述的一样，何况我们的敌人完全并非不可战胜：

    “是地球人与三体人的技术水平差距大呢，还是蝗虫与咱们人的技术水平差距大？”

    把人类看做虫子的三体人似乎忘记了一个事实：虫子从来就没有被真正战胜过。

    “我们快回去吧，有好多工作要做呢。”


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
