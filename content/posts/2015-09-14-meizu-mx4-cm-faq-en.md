---
title: 'CyanogenMod for Meizu MX4: FAQ #1'
date: 2015-09-14T16:35:00+08:00
draft: false
---

## Status on bootloader lock circumvention

As you've already known, ordinary version of Meizu MX4 has its bootloader
locked, thus only stock Flyme images are allowed to boot. Due to the
implementation of MTK <s>secure</s> restricted boot, the device will be
hard-bricked if the RSA signature verification failed. You can't even
recharge the battery as the verification code runs very early, even earlier
than initialization of peripherals. Flashing using SP Flash Tool wouldn't
work either because the Boot ROM (BROM) is locked on the hardware level.

Nevertheless, 3rd-party Android distros can (and will) be ported to Meizu MX4.
Thanks to Meizu, the Flyme boot sequence is not very different from that of
AOSP, and that means we can mix-and-match stock `boot` and 3rd-party `system`
partitions (albeit with loss of features requiring e.g. init script
modification). Another thought might be porting `kexec` to stock kernel,
booting a second identical kernel but with our own initramfs. We can only use
an identical kernel as the source is unavailable, but fortunately they haven't
disabled the module support, which is nice.

Progress so far:

*   Non-working: **DO NOT TRY** directly flashing the following partitions
    using images extracted from Meizu MX4 Ubuntu Edition.

    - `preloader` (`/dev/block/mmcblk0boot0`)
    - `lk`
    - `seccfg`
    - `secro`
    - `flashinfo`

    This way, although theoretically sound (as it *seems* to replace all code
    involved in boot process), still hard-bricks the phone, probably caused by
    the BROM which is unaccessible from Linux. The only way to access
    the BROM seems to be specialized debugging equipments, but doing so has
    legal risks. I bricked two phones provided by volunteers recruited from
    Weibo, so just don't try this.

*   Working: modifying base system to get it to boot on MTK/Flyme `boot.img`

    This is mainly about noticing the differences between AOSP and MTK
    `boot.img` components (`init`, init scripts, `healthd`), and working
    around the differences in base system, which we can freely modify.
    However, because the `boot.img` is left untouched, some features may be
    harder to implement, specifically those relying on `init` services.
    CM superuser management is one magnificent example of this; all volunteers
    who flashed the 1st testing system image lost their root access despite
    my explicit starting the `su` daemon via an executable run as `root` but
    non-existent on CM. Also the requirement of modified base system is not
    really elegant, so I'm currently experimenting with the 3rd method --

*   Unknown: `kexec`-ing with replaced initramfs

    I've found [an implementation on XDA][kexec-xda], but that one seems to be
    based on an CAF 3.4 kernel, which is plain unusable on a MTK 3.10 kernel.
    After an extensive coding session the code finally compiles and loads,
    but the kernel instantly panics after that. In the following days I'll
    try to do the work from scratch with the open-sourced MX4 Ubuntu Edition
    kernel, to see if this is indeed feasible.

[kexec-xda]: http://forum.xda-developers.com/showthread.php?t=2495152


## Possibility of Ubuntu Touch on ordinary MX4

The `lk` implementation of MX4 Ubuntu Edition passes a few more parameters
on kernel command-line compared to that of orinary MX4. You might think the
parameters are just decorations and can be safely thrown away, but the
parameters look like this:

```
systempart=/dev/disk/by-partlabel/system datapart=/dev/disk/by-partlabel/userdata fixrtc
```

Ermmmm...

On top of the `lk` differences, Ubuntu Touch also facilitates its own kernel
image and boot sequence, effectively requiring an unlocked bootloader to
successfully boot.

Anyway, if the `kexec` way of circumventing the bootloader succeeded, Ubuntu
Touch can then be installed on ordinary MX4. Otherwise it seems pretty difficult...


## Compatibility with YunOS edition MX4's

The hardware is (nearly) identical, so there isn't even a problem in the first
place.  However there are reports of bricked phones after cross-flashing
between YunOS (Y) and general (A) versions of Flyme OS, so I wouldn't be 100%
sure about the compatibility. Will look into this later.


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
