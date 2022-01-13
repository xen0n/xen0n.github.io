---
title: 'CyanogenMod for 魅族 MX4: CM12.1 20160112 测试包发布'
date: 2016-01-12T18:08:00+08:00
draft: false
aliases:
    - /2016/01/12/meizu-mx4-cm-12.1-userdebug-8/
---


## 声明

**刷机需要打开 root 并进行危险操作, 鉴于魅族设备的特性, 有使您的手机变砖的风险.
您选择刷机并使用本 ROM 即意味着您接受由此行为可能带来的一切后果,
本 ROM 作者概不负责.**

**本人开发此 ROM 完全出于个人需求及兴趣, 如在使用过程中碰到 bug 等问题请理性反馈,
本人有决定是否修复及修复方式, 时间等的权利.**

本 ROM 系基于 CyanogenMod 12.1 编译, 使用了大量开源社区的成果. 这些资源包括但不限于:

* [kirill8000](http://4pda.ru/forum/index.php?showuser=4461476) 和 [kkk4](http://4pda.ru/forum/index.php?showuser=610367) 的 MX4 BL 解锁工作
* [@axet](https://github.com/axet) 和 [@fire855](https://github.com/fire855) 的 MTK 移植工作
* [@DerTeufel](https://github.com/DerTeufel) 提供的关于 MTK GPS 的信息
* cofface 的 CWM recovery
* 阿木大神 的一键解锁工具制作
* @ccfxny ([微博](http://weibo.com/ccfxny), [GitHub](https://github.com/ccfxny)) 前辈的鼎力支持


## 文章更新记录

* 2016/01/12 18:08 首次发布


## 较上一版的改动

* **修复** 蓝牙不能正常连接; 蓝牙音频无声 (感谢 @ccfxny!)
* **修复** 某些情况下 WiFi 连接无法获取 IP 地址
* **修复** 恢复出厂设置不会清空内部存储了; 其实很久之前就修复了只是没有测试
* **新增** 闭源组件与内核同步至 Flyme 5.6.1.12 beta 版本 (感谢 @ccfxny!)
* **新增** 代码同步至 2015/01/12 版本
* **新增** 系统底层库 `libui.so` 由使用 MTK 版变为源码编译, 效果待考察
* **移除** 由于一些用户反应稳定性下降, 不再内置 Xposed, 取而代之将随包转载亲测可用的 Xposed 卡刷包, 请**刷入系统包之后马上刷入 Xposed**


## 已知未修复的 bugs

严重 bug 不代表马上会修复, 实际上存留时间长的 bug 无非两种原因, 一是机制复杂,
二是无法重现. 请参见上文关于 bug 修复的声明.

* 部分用户最小音量过大
* 部分用户系统重启后需较长时间才能连接移动网络, 甚至需要开关飞行模式
* 部分用户无法自动配置短信中心 (SMSC) 号码
* 部分大型应用无法安装
* 待补充


## 下载

* [百度云][baidupan]
* [360 云盘下载链接][360-yunpan] 提取码：`78c8`

安卓版 MX4 用户请下载 `mx4` 目录下的内容, Ubuntu 版请下载 `arale` 目录下的内容. 由于上次更新出现了数次突发状况, 版本情况比较杂乱, 本次更新不提供 OTA 包, 请使用完整包刷入, 还请各位理解.

[baidupan]: http://pan.baidu.com/s/1c1i2RAS
[360-yunpan]: https://yunpan.cn/cuTw6BrNsdE2B


给有需求用户的校验和:

```
# MD5
# MX4
5a48edf754f88edd20dd22abd66f518b  mx4/ApkIDE_MX4_Unlock_BL.apk
904b2000ec9c600bc772c611c6b93ae5  mx4/cm-12.1-20160112-UNOFFICIAL-mx4.zip
7ff821c9c916622206862170a4c0c197  mx4/XposedInstaller_3.0_alpha4.apk
57495f4ef9cd5a2da7f498e371e8f9c9  mx4/xposed-v79-sdk22-arm.zip

# arale
6ba6b4d397ef737d20f5bb03c29e2dd7  arale/recovery-arale-20160112-fixedroot.img
088be1c714a38d95b306c3d82f085c79  arale/cm-12.1-20160112-UNOFFICIAL-arale.zip
7ff821c9c916622206862170a4c0c197  arale/XposedInstaller_3.0_alpha4.apk
57495f4ef9cd5a2da7f498e371e8f9c9  arale/xposed-v79-sdk22-arm.zip


# SHA-1
# MX4
399167bb7fcdf61de397b85b96ec95934e0ab1c8  mx4/ApkIDE_MX4_Unlock_BL.apk
b9422604c4532fc08214b99c4ae9560cffcf3ddd  mx4/cm-12.1-20160112-UNOFFICIAL-mx4.zip
3e84a3895a8c0e812bad85b98e5f176266215fb4  mx4/XposedInstaller_3.0_alpha4.apk
5b0b0dd08eb2962c0d8e7620c92ed01de7e04487  mx4/xposed-v79-sdk22-arm.zip

# arale
f316d397e84cf3dea6f13fcd96c170b14a5244b6  arale/recovery-arale-20160112-fixedroot.img
203402cd0385d2770c94798a2f97f6562f9acd46  arale/cm-12.1-20160112-UNOFFICIAL-arale.zip
3e84a3895a8c0e812bad85b98e5f176266215fb4  arale/XposedInstaller_3.0_alpha4.apk
5b0b0dd08eb2962c0d8e7620c92ed01de7e04487  arale/xposed-v79-sdk22-arm.zip


# SHA-256
# MX4
efaf514f8a5429198d2c394ac24becbef959f06933bdb82b00a16812752f8a47  mx4/ApkIDE_MX4_Unlock_BL.apk
6f21b60661e42b50452cfd2c8579394d750f2fd7b0b031c8026831a52eb4ade5  mx4/cm-12.1-20160112-UNOFFICIAL-mx4.zip
835fdfd6244e4981818d2e44ad525575fe24772c5574c639c60cc3c48ba085fe  mx4/XposedInstaller_3.0_alpha4.apk
abe16939a729070800e02d63ab5915492f46cbf2620e2ab96384dc513bf8f6d7  mx4/xposed-v79-sdk22-arm.zip

# arale
8ccbdf4f0a511b3e1ccac95b17a8070c60976e86f65d288dc208e09a96ff8fd1  arale/recovery-arale-20160112-fixedroot.img
6aa49c2ebefb7d22ebf2318f3bd55acd0585cc1f3703aea04ed083bf113b3779  arale/cm-12.1-20160112-UNOFFICIAL-arale.zip
835fdfd6244e4981818d2e44ad525575fe24772c5574c639c60cc3c48ba085fe  arale/XposedInstaller_3.0_alpha4.apk
abe16939a729070800e02d63ab5915492f46cbf2620e2ab96384dc513bf8f6d7  arale/xposed-v79-sdk22-arm.zip


# SHA-512
# MX4
2b1af3ee839190092c75a08a0091ab4b79b7e069534c7004fb8a7dfea1bdc4e25cd3d0da50541f8853387f18a0aeae106c808c91f3bd3e187be9b6033b1d73b5  mx4/ApkIDE_MX4_Unlock_BL.apk
a0983f5003a1d8ac4efa78f74d071fb04f8f9b23f0531f3062b9b7f2af5f17a61107993e3d920ef30a50fd5d4bb86e0b2af8e844a104cff5f1f0e7e06d3e264f  mx4/cm-12.1-20160112-UNOFFICIAL-mx4.zip
1d5fa5c37005ec0fa48cd41358bf60515a6ac44d04136f07f9ba8dda322c46b24abc608e78ba8180486978eb731e2d612a22be6a01f6bf765e9b1eb3f065b391  mx4/XposedInstaller_3.0_alpha4.apk
92975faca43f22a34db38eb3e611b5ffa457ec075b4f419e7eb09bdef97add5bcd80622a802ee66516071e1ea3e5aee3bfc2f652bbaa083c5e33df0f2985bfa6  mx4/xposed-v79-sdk22-arm.zip

# arale
c17e7b750c3b0f9a66fdcf7f621ca660ed4b1e6e0890706423e2b4e7acf5e69f1d9ab161f08f143822bf988635623e7727ca495b3a74d8421863c29786efb11e  arale/recovery-arale-20160112-fixedroot.img
5b2012b96d2a3a54be453872802b8f42d0e379fdc471f11cb301f4d58a268bb928cd85274b17ed7d4cc119be63daf96f387cc8de5e7a81f65d7caa81b74c045c  arale/cm-12.1-20160112-UNOFFICIAL-arale.zip
1d5fa5c37005ec0fa48cd41358bf60515a6ac44d04136f07f9ba8dda322c46b24abc608e78ba8180486978eb731e2d612a22be6a01f6bf765e9b1eb3f065b391  arale/XposedInstaller_3.0_alpha4.apk
92975faca43f22a34db38eb3e611b5ffa457ec075b4f419e7eb09bdef97add5bcd80622a802ee66516071e1ea3e5aee3bfc2f652bbaa083c5e33df0f2985bfa6  arale/xposed-v79-sdk22-arm.zip
```


## 刷机方法

请根据自己当前的系统选择相应的方法操作.

**如您不能理解此教程, 说明您是小白, 建议不要刷入! 第三方系统不同于官方系统, 后续您会遇到更多使用和维护上的挑战. 请自行权衡您的恐惧感和好奇心.**


### 已刷入本 ROM 前一版本的用户

由于时间紧迫加上大部分用户会 root 后对系统文件做出修改, 该版本只有完整包提供, 没有增量包, 不好意思;-)

* 无需双清, 将刷机包放入手机内部存储之后可直接进入 recovery 模式
* 直接刷入即可


### 从 Ubuntu 版 MX4 首次刷入本 ROM 的用户

* Ubuntu 版 MX4 没有 bootloader 锁, 请直接关机后同时按住电源键和音量下键, 进入 fastboot 模式, 刷入 recovery (cofface 版 recovery 暂时有兼容问题, 换成了 CM 自带的)
* 按住音量上键, 在电脑上 `fastboot reboot` 使手机进入恢复模式
* 格式化 data 分区后用 adb 推入卡刷包
* 正常卡刷 (Apply update 之后选第二个选项), 重启


### 从 Flyme 或其他第三方 ROM 刷入本 ROM 的用户

请严格按照指令操作, 尤其是 bootloader 解锁, 否则一定变砖!
魅族机器变砖无法自行救砖, 如果变砖请自行前往当地服务点或返厂救砖, 本人概不负责.
不过一般是免费的 (本人体验; 您的体验可能不同).

如果您已经处于其他第三方系统, 请直接跳过解锁步骤, 双清刷入即可. 否则请首先做解锁操作.


#### 未解锁 BL 用户

* 用官方方法安装 Flyme 4.2.8.2A 系统, 必须是 `4.2.8.2` 系列
* 把两个下载的文件放进手机内部存储
* 安装下载的 `ApkIDE_MX4_Unlock_BL.apk`
* 进入应用, 阅读它的说明文字, 选择一键解锁 BL
* 做下边的操作


#### 已解锁 BL 用户

* **注意**: 每次进入 Flyme 系统都会自动恢复 recovery 分区到官方 recovery, 因此如果解锁 BL 后重启了 Flyme, 需要重新解锁并进入. 其他第三方系统基本不用担心此类问题.
* 进入恢复模式, 操作方法是音量加减选择, 电源键确定
* 双清 (恢复出厂设置), 不使用 TWRP recovery 的话这一步会持续 5 到 15 分钟, 请耐心等待
* 正常卡刷刷入
* 重启


## 一些使用方面的说明

* **首次开机设置**
    - 最好跳过 WiFi 连接步骤, 进到桌面再连. 在那个界面连的话下一步可能会卡住, 反正也需要跳过
    - 可以把使用情况统计关掉
    - 进入系统之后可以去 `设置-关于手机-CyanogenMod 更新` 把 CM 自动更新检查关掉, 在修复所有 bug 之前不会提交官方的 (CM 官方政策) 不会有自动更新
* **手机网络**:
    - 第一次开机很可能没有信号, 请进入桌面之后**打开飞行模式再关闭**, 让电话组件重新初始化
    - FDD 基带 (如联通) 用户可能在重启系统之后出现无 SIM 卡的情况, 解决办法同上
    - 开 4G 网络的方法: 现已修复设置页面不显示 LTE 网络的问题, 现在只需要进入 `设置 - 移动网络 - 首选网络设置` 即可选择首选网络制式了
* **小圆圈相关**
    - 我尝试了在 CM 代码基础上复刻小圆圈功能, 然而可用性不如 Flyme 的实现, 因此没有放出. 主体实现在 `xen0n/android_frameworks_base_mtk` 这个库的 `cm-12.1-mx-circle` 分支下, 欢迎吐槽
    - 启用扩展桌面来隐藏虚拟键会造成大部分国产汉语输入法的输入框偏移, 请自行安装相应 Xposed 插件实现小圆圈策略并修改 `/system/build.prop` 禁用虚拟键 (找到 `qemu.hw.mainkeys` 把 0 改成 1 或者删除该行)
* 想起来了我会来更新的


## 开发者捐赠渠道

* 支付宝账号：`idontknw.wang@gmail.com`

如果您觉得我制作的 ROM/Recovery 对您有帮助, 您可以进行捐赠.
捐赠多少没关系, 您的支持是对我最大的鼓励.


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
