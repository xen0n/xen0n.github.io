---
title: '从零开始搭建一个 Kubernetes 集群(0): 预告'
date: 2018-07-09T19:38:00+08:00
draft: false
aliases:
    - /2018/07/09/k8s-from-scratch-0/
文章类别:
    - 杂项
    - 坑
---

这个博客荒废了好久，主要是中间毕业了有了工作，之前的 MIPS 相关内容也更新停滞了。不过最近因为稍微多了一点时间（稍微！），准备开个新坑，不得不自建一个 Kubernetes 集群——

想着反正整个过程也是极其漫长，而且万一新坑做成了肯定还是需要多加几个集群的，怕到时候再忘记怎么搭，不得不重来一遍，那么就写一个流水账吧。毕竟鄙人这么多年实践下来，最擅长的文体还是流水账。

不定期更新（操作多少更新多少），目标是搭建一个如下的集群：

* Gentoo、Ubuntu 两种宿主发行版
* Docker 最新 ce 版本（反正跟 [rkt][] 都是 Go 写的，没什么区别，现在还没见过 Rust 的 OCI runtime 实现）
* Kubernetes 最新稳定版本（截至写作时为 1.11）
* [CNI-Genie][] + [Calico][] IPv6-only 内网，同时为个别节点提供 IPv4 连通性（通过网关什么的）
* 存储还没想好，估计先放在某台机器上
* 加入一个 GPU 节点，[支持 CUDA][]
* （理想状态）支持 amd64/mips64el 双架构，如果能做到的话考虑找台 arm64 设备来凑凑热闹

[rkt]: https://github.com/rkt/rkt
[CNI-Genie]: https://github.com/Huawei-PaaS/CNI-Genie
[Calico]: https://www.projectcalico.org/
[支持 CUDA]: https://github.com/NVIDIA/nvidia-container-runtime

至于能实现多少我们就拭目以待吧……


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
