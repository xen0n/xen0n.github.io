---
title: '《开局一个二进制，从零开始的 LoongArch 指令集推导》——第一回 软件包'
date: 2021-02-17T22:52:00+08:00
draft: false
aliases:
    - /2021/02/17/reversing-loongarch-1/
---

> 本 LoongArch 指令集研究工作在百度贴吧龙芯吧同步连载。
>
> 本研究中涉及的逆向工程仅出于学习、研究目的。本研究工作未得到任何龙芯、麒麟等软硬件厂商的任何形式帮助。
>
> 本研究属于个人行为，与本人雇主或任何其他主体无关。

众所周知，几大常见国产商业发行版的软件源地址都是公开的，只要你自己装过，或者询问过有这系统的朋友，都可以知道。

商业发行版的软件源不同于许多社区发行版，往往可以见到一些商业软件的移植版；会受生态问题困扰的软件自然是不开源的（开源软件的适配、打包工作，社区自己就自带干粮做了），社区发行版由于运营主体模糊，也不易与商业公司达成再分发的协议。所以很多时候虽然你能看到不少软件、驱动，甚至有的软件你也能用上，也只能看个乐呵。

是假期前的一天，楼主漫无目的地在网上闲逛，走进了麒麟的软件源，嗬！有一个叫 `binary-loongarch64` 的目录！

麒麟是一个 Debian 系发行版，软件源的目录结构类似如下：

* `https://example.com/<系统代号>/`
    - `dists/<版本号>/<repo 名>/` 这下面存放各种包的元数据
        - `binary-<架构名>` 二进制包的索引
        - `source` 源码包的索引
        - ...
    - `pool/` 软件包的存放地点
        - `a` `b` ... `z` 按包的首字母分目录存放，为了避免单个目录过大
        - `liba` `libb` ... `libz` 单独抽出来也是为了避免 `l` 目录过大

虽然很多国内发行版都不提供源码包，麒麟也是一样，但至少这一次我们有机会一睹真正 LoongArch 二进制的真容！

事不宜迟，马上下载 `http://archive.kylinos.cn/kylin/KYLIN-ALL/dists/10.1/main/binary-loongarch64/Packages.bz2` 文件。

直接 `bunzip2` 解压缩之后，是一堆包的元数据，单个包的信息类似这样：（这里取了 Ubuntu 的包数据展示）

```
Package: coreutils
Architecture: amd64
Version: 8.30-3ubuntu2
Multi-Arch: foreign
Priority: required
Essential: yes
Section: utils
Origin: Ubuntu
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Original-Maintainer: Michael Stone <mstone@debian.org>
Bugs: https://bugs.launchpad.net/ubuntu/+filebug
Installed-Size: 7196
Pre-Depends: libacl1 (>= 2.2.23), libattr1 (>= 1:2.4.44), libc6 (>= 2.28), libselinux1 (>= 2.1.13)
Filename: pool/main/c/coreutils/coreutils_8.30-3ubuntu2_amd64.deb
Size: 1249368
MD5sum: e8e201b6d1b7f39776da07f6713e1675
SHA1: 1d4ab60c729a361d46a90d92defaca518b2918d2
SHA256: 99aa50af84de1737735f2f51e570d60f5842aa1d4a3129527906e7ffda368853
Homepage: http://gnu.org/software/coreutils
Description: GNU core utilities
Task: minimal
Description-md5: d0d975dec3625409d24be1238cede238
```

很明显，只要过滤出 `Architecture: loongarch64` 的包名和对应的 `.deb` 包路径就好了。

实际上会有很多包由于是脚本语言写作，或者是纯数据，因此是架构无关的，`Architecture` 字段会取 `all`。

因为按照命名规范，架构名一定会在文件名中出现，所以投机取巧一下，直接 `grep` 出满足 `^Filename: .*loongarch64` 的行，然后切掉头，拼上软件源的基础 URL 前缀就可以了。

这样我们从 `main` 和 `universe` 两个库获得了一共 497 个 LoongArch 软件包，一行一个，放进一个文件，使用 `wget` 的 `-i` 选项可以很方便地批量下载。

全部下载之后，定睛一看，咦？没有 `linux`，没有 `binutils`，没有 `gcc`，也没有 `glibc`！

得，什么都没有，自己搞吧，自己动手丰衣足食……好在为数不多的几个包里，还有 `libpython2.7` 和 `libpython2.7-dbg`，有个通用编程语言实现，还是聊胜于无，至少能看到的指令种类应该不缺了。
