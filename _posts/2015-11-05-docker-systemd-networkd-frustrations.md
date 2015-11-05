---
layout: post
title: 'Docker 与 systemd-networkd 之间不得不说的故事'
date: 2015-11-05 15:45:00
---

## tl;dr

如果你**使用 systemd-networkd 管理你的网络界面**, 又把这台机器作为 **Docker 容器宿主**的话,
那你很可能会发现你的容器过一段时间就会不能访问外网. 你需要在 `/etc/systemd/network/your.network`
配置里明确告诉 systemd-networkd 开启报文转发:

```ini
# ...

[Network]
# ...
IPForward=yes
```


## 并不愉快的经历

我有一台打算做 Docker 容器宿主的服务器, 然而部署完成不久就发现了一个严重问题 --
容器不能访问外网! 好吧实际上还是可以的... 刚开机就启动的 Docker 容器可以联网,
过一会启动的容器也能, 但再过一会就不行了; 故障时间也不一定, 有时候开机几分钟就断网了,
有时候能撑半个小时, 完全没有规律. 就这样闲置了半年之久!

最近因为做项目, 又有了用容器的需求, 就想着回来调试一下吧; 更新了所有软件到最新版本,
也升级了内核到最新的 Gentoo Hardened 4.2.5 版本, 然而情况并没有变化.
因为刚刚闲了下来, 就彻彻底底地解决这个问题好了, 于是我打开了内核源码 ;-)


## 正常的流量

之前就在机器上抓过一次包, 想看看为什么容器没有收到响应. 因为断网的原因是多种多样的,
可能是报文没有出 `docker0` 界面, 报文没有上到物理界面, 报文没有正确被 NAT 回
Docker 内网地址, 还可能是其他更神奇的原因. 我在容器里 ping 宿主的网关和 DNS
服务器, 在宿主上抓包, 然而看到结果之后我几乎疯掉了...

物理界面上有完整的 ICMP Ping 请求和响应包, 然而 `docker0` 上的响应被吃掉了!

我又通过拼手速, 设法抓到了断网一瞬间前后的网络流量, 仍然没有什么问题;
在某个时间点过后, 响应包就是消失了, 完全不讲道理. 我觉得问题可能出在 Linux 内核本身了.


## 仍然正常的 iptables

Docker 默认的容器联网方式是桥接网络, 就是:

* Docker 启动时初始化一个网桥 `docker0`, 设置 iptables 让预先配置的 Docker 网段能 NAT 到外网
* 容器启动时, 首先创建一对 `vethXXXXXX` 虚拟界面, 一端塞进容器的 netns 里, 一端留在宿主
* 然后把宿主一侧的 veth 界面接入 `docker0`
* 如果有设置端口映射的话, 就为对应的容器 IP 和端口设置 `MASQUERADE` 和 `DNAT`

具体情况各位可以自行在跑 Docker 的机器上看一看 `iptables -nvL` 和 `iptables -t nat -nvL`
的输出, 不过应该区别不大.

因为丢包的话首先就是考虑 iptables 是不是把包给 `DROP` 了, 我显然也是检查了一下,
然而 `DROP` 一次都没有出现... (因为服务器托管在学校网络中心, 我暂时没有单独设置防火墙)

这不科学, 因此我做了这个操作给所有 ICMP 包启用了跟踪:

```sh
# 首先需要加载 xt_LOG 模块, 这样 TRACE 才有效, 实际上 modprobe xt_LOG 就行了
# 然而我直接添加了一条规则, 效果一样
iptables -t nat -I PREROUTING 1 -p icmp -j LOG
iptables -t raw -A PREROUTING -p icmp -j TRACE
iptables -t raw -A OUTPUT -p icmp -j TRACE
```

继续拼手速打出了断网前后的 trace 对比 (把 IP 和硬件地址打码了, 并且改了 Docker 的网段):

```
[  118.520085] TRACE: raw:PREROUTING:policy:2 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=64 ID=60758 PROTO=ICMP TYPE=0 CODE=0 ID=35 SEQ=64
[  118.520091] TRACE: mangle:PREROUTING:policy:1 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=64 ID=60758 PROTO=ICMP TYPE=0 CODE=0 ID=35 SEQ=64
[  118.520097] TRACE: mangle:FORWARD:policy:1 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=63 ID=60758 PROTO=ICMP TYPE=0 CODE=0 ID=35 SEQ=64
[  118.520101] TRACE: filter:FORWARD:rule:1 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=63 ID=60758 PROTO=ICMP TYPE=0 CODE=0 ID=35 SEQ=64
[  118.520105] TRACE: filter:DOCKER:return:2 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=63 ID=60758 PROTO=ICMP TYPE=0 CODE=0 ID=35 SEQ=64
[  118.520109] TRACE: filter:FORWARD:rule:2 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=63 ID=60758 PROTO=ICMP TYPE=0 CODE=0 ID=35 SEQ=64
[  118.520112] TRACE: mangle:POSTROUTING:policy:1 IN= OUT=docker0 SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=63 ID=60758 PROTO=ICMP TYPE=0 CODE=0 ID=35 SEQ=64
```

和

```
[  275.429990] TRACE: raw:PREROUTING:policy:2 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=64 ID=60797 PROTO=ICMP TYPE=0 CODE=0 ID=39 SEQ=2
[  275.431901] TRACE: mangle:PREROUTING:policy:1 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=64 ID=60797 PROTO=ICMP TYPE=0 CODE=0 ID=39 SEQ=2
```

噫... 断在了 `mangle` 表的 `PREROUTING` 和 `FORWARD` 两条链之间. `iptables -t mangle -nL`...

```
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination

```

啊... (掩面)


## 完全正常的 iptables 和 IPv4 路由

我编译了很多次内核, 打出更多的调试信息, 到意识到真正问题为止我做了如下的改动:

```diff
diff -ur a/net/ipv4/ip_input.c b/net/ipv4/ip_input.c
--- a/net/ipv4/ip_input.c	2015-10-31 17:10:54.000000000 +0800
+++ b/net/ipv4/ip_input.c	2015-11-05 10:48:11.713066532 +0800
@@ -341,6 +341,8 @@
 	if (!skb_dst(skb)) {
 		int err = ip_route_input_noref(skb, iph->daddr, iph->saddr,
 					       iph->tos, skb->dev);
+		if (unlikely(skb->nf_trace))
+			pr_info("ip_rcv_finish: ip_route_noref=%d\n", err);
 		if (unlikely(err)) {
 			if (err == -EXDEV)
 				NET_INC_STATS_BH(dev_net(skb->dev),
@@ -349,6 +351,9 @@
 		}
 	}

+	if (unlikely(skb->nf_trace))
+		pr_info("ip_rcv_finish: survived routing\n");
+
 #ifdef CONFIG_IP_ROUTE_CLASSID
 	if (unlikely(skb_dst(skb)->tclassid)) {
 		struct ip_rt_acct *st = this_cpu_ptr(ip_rt_acct);
@@ -374,6 +379,9 @@
 	return dst_input(skb);

 drop:
+	if (unlikely(skb->nf_trace))
+		pr_info("ip_rcv_finish: whoops\n");
+
 	kfree_skb(skb);
 	return NET_RX_DROP;
 }

diff -ur a/net/ipv4/netfilter/iptable_mangle.c b/net/ipv4/netfilter/iptable_mangle.c
--- a/net/ipv4/netfilter/iptable_mangle.c	2015-08-31 02:34:09.000000000 +0800
+++ b/net/ipv4/netfilter/iptable_mangle.c	2015-11-05 10:48:11.692066533 +0800
@@ -61,6 +61,8 @@

 	ret = ipt_do_table(skb, NF_INET_LOCAL_OUT, state,
 			   dev_net(out)->ipv4.iptable_mangle);
+	if (unlikely(skb->nf_trace))
+		pr_info("ipt_mangle_out: ipt_do_table=%d\n", ret);
 	/* Reroute for ANY change. */
 	if (ret != NF_DROP && ret != NF_STOLEN) {
 		iph = ip_hdr(skb);
@@ -70,6 +72,8 @@
 		    skb->mark != mark ||
 		    iph->tos != tos) {
 			err = ip_route_me_harder(skb, RTN_UNSPEC);
+			if (unlikely(skb->nf_trace))
+				pr_info("ipt_mangle_out: ip_route_me_harder=%d\n", err);
 			if (err < 0)
 				ret = NF_DROP_ERR(err);
 		}
@@ -84,14 +88,28 @@
 		     struct sk_buff *skb,
 		     const struct nf_hook_state *state)
 {
-	if (ops->hooknum == NF_INET_LOCAL_OUT)
-		return ipt_mangle_out(skb, state);
-	if (ops->hooknum == NF_INET_POST_ROUTING)
-		return ipt_do_table(skb, ops->hooknum, state,
+	int phase;
+	unsigned int ret;
+	if (ops->hooknum == NF_INET_LOCAL_OUT) {
+		phase = 0;
+		ret = ipt_mangle_out(skb, state);
+		goto out;
+		}
+	if (ops->hooknum == NF_INET_POST_ROUTING) {
+		phase = 1;
+		ret = ipt_do_table(skb, ops->hooknum, state,
 				    dev_net(state->out)->ipv4.iptable_mangle);
+		goto out;
+		}
 	/* PREROUTING/INPUT/FORWARD: */
-	return ipt_do_table(skb, ops->hooknum, state,
+	phase = 2;
+	ret = ipt_do_table(skb, ops->hooknum, state,
 			    dev_net(state->in)->ipv4.iptable_mangle);
+
+	out:
+	if (unlikely(skb->nf_trace))
+		pr_info("iptable_mangle_hook: phase=%d ret=%u\n", phase, ret);
+	return ret;
 }

 static struct nf_hook_ops *mangle_ops __read_mostly;

diff -ur a/net/ipv4/netfilter/ip_tables.c b/net/ipv4/netfilter/ip_tables.c
--- a/net/ipv4/netfilter/ip_tables.c	2015-10-31 17:10:54.000000000 +0800
+++ b/net/ipv4/netfilter/ip_tables.c	2015-11-05 10:48:11.690066533 +0800
@@ -429,6 +429,9 @@
  	xt_write_recseq_end(addend);
  	local_bh_enable();

+	if (unlikely(skb->nf_trace))
+		pr_info("TRACE: acpar.hotdrop=%d verdict=%d\n", acpar.hotdrop, verdict);
+
 #ifdef DEBUG_ALLOW_ALL
 	return NF_ACCEPT;
 #else
```

然后重启进修改过的内核, 给 ICMP 包启用跟踪, 看到了这样的结果:

```
[   89.207465] TRACE: raw:PREROUTING:policy:2 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=255 ID=47320 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=25
[   89.209365] ip_tables: TRACE: acpar.hotdrop=0 verdict=1
[   89.210310] TRACE: mangle:PREROUTING:policy:1 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=255 ID=47320 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=25
[   89.212222] ip_tables: TRACE: acpar.hotdrop=0 verdict=1
[   89.213162] iptable_mangle_hook: phase=2 ret=1
[   89.214087] IPv4: ip_rcv_finish: ip_route_noref=0
[   89.214994] IPv4: ip_rcv_finish: survived routing
[   89.215891] TRACE: mangle:FORWARD:policy:1 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=254 ID=47320 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=25
[   89.217741] ip_tables: TRACE: acpar.hotdrop=0 verdict=1
[   89.218679] iptable_mangle_hook: phase=2 ret=1
[   89.219605] TRACE: filter:FORWARD:rule:1 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=254 ID=47320 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=25
[   89.221493] TRACE: filter:DOCKER:return:2 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=254 ID=47320 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=25
[   89.223402] TRACE: filter:FORWARD:rule:2 IN=eno1 OUT=docker0 MAC=xxx SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=254 ID=47320 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=25
[   89.225315] ip_tables: TRACE: acpar.hotdrop=0 verdict=1
[   89.226257] TRACE: mangle:POSTROUTING:policy:1 IN= OUT=docker0 SRC=xxx DST=10.111.1.2 LEN=84 TOS=0x00 PREC=0x00 TTL=254 ID=47320 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=25
[   89.228144] ip_tables: TRACE: acpar.hotdrop=0 verdict=1
[   89.229073] iptable_mangle_hook: phase=1 ret=1
```

和

```
[   90.209849] TRACE: raw:PREROUTING:policy:2 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=255 ID=47321 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=26
[   90.212000] ip_tables: TRACE: acpar.hotdrop=0 verdict=1
[   90.212974] TRACE: mangle:PREROUTING:policy:1 IN=eno1 OUT= MAC=xxx SRC=xxx DST=xxx LEN=84 TOS=0x00 PREC=0x00 TTL=255 ID=47321 DF PROTO=ICMP TYPE=0 CODE=0 ID=34 SEQ=26
[   90.214932] ip_tables: TRACE: acpar.hotdrop=0 verdict=1
[   90.215900] iptable_mangle_hook: phase=2 ret=1
[   90.216854] IPv4: ip_rcv_finish: ip_route_noref=0
[   90.217795] IPv4: ip_rcv_finish: survived routing
```

我擦泪... 这路由结果明明是对的... iptables 也正确放行了... 那为何没有 forward 呢?


## 最后知道真相的我眼泪掉下来

```diff
diff -ur a/net/ipv4/route.c b/net/ipv4/route.c
--- a/net/ipv4/route.c	2015-10-31 17:10:54.000000000 +0800
+++ b/net/ipv4/route.c	2015-11-05 10:48:11.713066532 +0800
@@ -1717,11 +1717,15 @@
 	fl4.daddr = daddr;
 	fl4.saddr = saddr;
 	err = fib_lookup(net, &fl4, &res, 0);
+	if (unlikely(skb->nf_trace))
+		pr_info("ip_route_input_slow: fib_lookup err=%d IN_DEV_FORWARD(in_dev)=%d\n", err, IN_DEV_FORWARD(in_dev));
 	if (err != 0) {
 		if (!IN_DEV_FORWARD(in_dev))
 			err = -EHOSTUNREACH;
 		goto no_route;
 	}
+	if (unlikely(skb->nf_trace))
+		pr_info("ip_route_input_slow: res.type=%d\n", res.type);

 	if (res.type == RTN_BROADCAST)
 		goto brd_input;
@@ -1741,6 +1745,9 @@
 	if (res.type != RTN_UNICAST)
 		goto martian_destination;

+	if (unlikely(skb->nf_trace))
+		pr_info("ip_route_input_slow: passed!\n");
+
 	err = ip_mkroute_input(skb, &res, &fl4, in_dev, daddr, saddr, tos);
 out:	return err;

```

其实在写完这个更改之后我已经意识到问题了, 因为我中间搜索了很多内容, 其中包括观察到
`/proc/net/snmp` 里 `InAddrErrors` 会随着丢掉的包数量增加, 而这个量对应的内核状态
`IPSTATS_MIB_INADDRERRORS` 只在一个地方增加:

```c
/* net/ipv4/route.c */

static int ip_error(struct sk_buff *skb)
{
        struct in_device *in_dev = __in_dev_get_rcu(skb->dev);
        struct rtable *rt = skb_rtable(skb);
        struct inet_peer *peer;
        unsigned long now;
        struct net *net;
        bool send;
        int code;

        /* IP on this device is disabled. */
        if (!in_dev)
                goto out;

        net = dev_net(rt->dst.dev);
        if (!IN_DEV_FORWARD(in_dev)) {
                switch (rt->dst.error) {
                case EHOSTUNREACH:
                        IP_INC_STATS_BH(net, IPSTATS_MIB_INADDRERRORS);
                        break;

                case ENETUNREACH:
                        IP_INC_STATS_BH(net, IPSTATS_MIB_INNOROUTES);
                        break;
                }
                goto out;
        }

        /* ... */

out:    kfree_skb(skb);
        return 0;
}
```

嗯... 这说明 `IN_DEV_FORWARD(in_dev)` 必然为假, 就是说 `/proc/sys/net/ipv4/conf/xxx/forwarding`
居然不是 `1`? 我之前不相信这个可能性, 所以打了很多日志, 但是现在看来真相只有一个了!
因为调试的时候观察到只要一运行 `tcpdump` 容器就会断网, 我就重启机器简单测试了一下:

```
# cat /proc/sys/net/ipv4/conf/eno1/forwarding
1
# tcpdump -i docker0 -s 65535 -w 111.pcap
(...)
^C
# cat /proc/sys/net/ipv4/conf/eno1/forwarding
0
```

给我块豆腐... 那除了内核, 还会有谁关心网络界面的参数设置呢? 很容易就能联想到
systemd-networkd 了... 果然在 `man systemd.network` 里对于 `IPForward` 参数有说明:

> Note: unless this option is turned on, or set to `"kernel"`, **no IP forwarding
> is done on this interface, even if this is globally turned on in the kernel**,
> with the `net.ipv4.ip_forward`, `net.ipv4.conf.all.forwarding`, and
> `net.ipv6.conf.all.forwarding` sysctl options.

(格式是我加上的, 方便阅读)

于是做了开头的 one-line fix, 重启, 问题消失. 前后花掉了 3 天时间思考和调试.
看起来生产环境用上 systemd-networkd 的人不多啊... 否则怎么可能至今没有文章介绍这个坑呢?


## 追记: 不定期断网的原因追踪

解决了断网问题之后, 我继续思考了一下为什么 systemd-networkd 会不定期跟内核同步.
稍微熟悉一点 systemd 的各位都知道, systemd 严重依赖事件驱动, 那么原因应该就是有事件触发了
systemd-networkd 的状态同步代码. 在 systemd 源码里简单 `grep` 了一圈, [果然][network-link.c]:
`link_set_ipv4_forward` (和另一个负责 IPv6 的函数) 只会被 `link_configure` 调用,
又只会被 `link_initialized_and_synced` 调用, 又只会被 `link_initialized` 调用,
这个函数不是 `static` 的所以应该有别的地方去调用它了, 很可能是个 uevent 监听循环.
因为比起研究 systemd 我还有更有意思的事情要做 (比如好好折腾一下 Docker 之类的),
就没有继续挖掘下去了, 而是写了这篇分析文章. 希望对各位都有帮助!


[network-link.c]: https://github.com/systemd/systemd/blob/master/src/network/networkd-link.c#L1802


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
