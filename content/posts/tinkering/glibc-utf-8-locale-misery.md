---
title: 'glibc 的 UTF-8 locale 惨剧'
date: 2017-08-19T16:21:38+08:00
draft: false
aliases:
    - /2017/08/19/glibc-utf-8-locale-misery/
文章类别:
    - Linux
    - glibc
    - macOS
    - 折腾
---

## tl;dr

LightDM 会错误设置 `$LANG` 等 locale 环境变量，造成如此配置的系统在 ssh 等传递 locale 相关环境变量情形下丧失与非 glibc 系统如 macOS 的兼容性。

考虑到 LightDM 整体上并没有什么核心竞争力，建议还是换用其他登陆管理器。


## 起因

我一直是一名苹果黑，直到公司给我配了一台 MacBook Pro（虽然这并没有改变我对苹果公司及其产品的整体看法）……因为所有同事也都在用，加上企业 QQ 等等一票应用 Linux 体验不存在或者极差的原因，我也就姑且配了下 Mac 环境。这涉及到判断系统种类并根据判断结果分支，对不同系统设置不同的环境变量等等：

```sh
local is_darwin=false
local is_linux=false
case `uname -s` in
    Darwin) is_darwin=true ;;
    Linux)  is_linux=true ;;
esac
```

一切进行得还算顺利，直到设置 mosh 为止。

`brew install mosh` 之后，因为 Homebrew 默认安装到 `/usr/local` PREFIX 下，需要传入 `--server` 指定 mosh 服务器程序路径，但还是不行：

```
$ mosh hanazono.lan --server=/usr/local/bin/mosh-server
setlocale: Bad file descriptor
setlocale: Bad file descriptor
mosh-server needs a UTF-8 native locale to run.

Unfortunately, the local environment (LC_CTYPE=zh_CN.utf8) specifies
the character set "US-ASCII",

The client-supplied environment (LC_CTYPE=zh_CN.utf8) specifies
the character set "US-ASCII".

LANG="zh_CN.utf8"
LC_COLLATE="C"
LC_CTYPE="C"
LC_MESSAGES="C"
LC_MONETARY="C"
LC_NUMERIC="C"
LC_TIME="C"
LC_ALL=
Connection to hanazono.lan closed.
/usr/bin/mosh: Did not find mosh server startup message. (Have you installed mosh on your server?)
```

这是为什么呢？


## 调查

很显然这是一个服务器不支持 UTF-8 的错误，问题在于现在是 2017 年，怎么可能还有系统不支持 UTF-8……况且从 Mac 里 mosh 其他机器也一切正常，那么问题就应该出在 Linux 一方。

我们看见出错信息里提到了 `zh_CN.utf8` 这个 locale：

```
$ locale
LANG=zh_CN.utf8
LC_CTYPE=zh_CN.utf8
LC_NUMERIC="zh_CN.utf8"
LC_TIME="zh_CN.utf8"
LC_COLLATE="zh_CN.utf8"
LC_MONETARY="zh_CN.utf8"
LC_MESSAGES="zh_CN.utf8"
LC_PAPER="zh_CN.utf8"
LC_NAME="zh_CN.utf8"
LC_ADDRESS="zh_CN.utf8"
LC_TELEPHONE="zh_CN.utf8"
LC_MEASUREMENT="zh_CN.utf8"
LC_IDENTIFICATION="zh_CN.utf8"
LC_ALL=
```

而 Mac 一侧的正常情况应该是：

```
$ locale
LANG="zh_CN.UTF-8"
LC_COLLATE="zh_CN.UTF-8"
LC_CTYPE="zh_CN.UTF-8"
LC_MESSAGES="zh_CN.UTF-8"
LC_MONETARY="zh_CN.UTF-8"
LC_NUMERIC="zh_CN.UTF-8"
LC_TIME="zh_CN.UTF-8"
LC_ALL=
```

嗯……在 Linux 一侧把 `LANG` 和 `LC_CTYPE` `export` 成 `zh_CN.UTF-8` 之后，果然一切正常了。不过退一万步讲，为何这里的 locale 设置从一开始会出问题？

我的 Linux 系统很久之前就换上了 systemd，systemd 会读取 `/etc/locale.conf` 来设置默认 locale 信息。问题在于它的设置没有问题：

```
LANG="zh_CN.UTF-8"
```

不得不提的是，这里用 eselect 或者 localectl 进行选择，默认出来也是 `utf8` 的字符集，此处的 `UTF-8` 是我手工修改的。

那为什么设置了也没用呢？


## 继续深入

既然正确的 locale 设置了也没用，但 [systemd 源码][systemd-locale]却不这么认为（它忠实地转达了我们的设置），我们不妨来看一下有多少进程受到了影响：

[systemd-locale]: https://github.com/systemd/systemd/blob/v234/src/core/locale-setup.c#L62

```sh
for i in `ps -ef --no-headers | awk '{ print $2; }'`; do
    sudo cat /proc/$i/environ | \
        tr '\0' '\n' |
        grep '\.utf8$' > /dev/null 2>&1 && echo $i
done > /tmp/123

ps -ef | grep -P "$(tr '\n' '|' < /tmp/123 | sed 's/\|$//')"
rm /tmp/123
```

随手撸了一个 quick-and-dirty 的检查脚本，看看哪些进程的环境变量里有 `.utf8` 这个片段。运行结果表明：

```
...

xenon     7382     1  0 15:16 ?        00:00:00 /usr/bin/gnome-keyring-daemon --daemonize --login
xenon     7384  7356  0 15:16 ?        00:00:00 /bin/sh /etc/xdg/xfce4/xinitrc -- /etc/X11/xinit/xserverrc
xenon     7401     1  0 15:16 ?        00:00:00 dbus-launch --autolaunch 62b624039cff8b48906360fb00000310 --binary-syntax --close-stderr
xenon     7402     1  0 15:16 ?        00:00:00 /usr/bin/dbus-daemon --fork --print-pid 5 --print-address 7 --session
xenon     7418     1  0 15:16 ?        00:00:00 /usr/bin/dbus-launch --exit-with-session startxfce4
xenon     7419     1  0 15:16 ?        00:00:01 /usr/bin/dbus-daemon --fork --print-pid 5 --print-address 7 --session
xenon     7427  7384  0 15:16 ?        00:00:09 xfce4-session

...
```

可以看见，所有用户登陆之前的进程都没有受影响，而从第一个启动的用户服务开始，整个 GUI 环境都被错误的 locale 变量污染了。可惜的是，这些进程的共同祖先已经结束运行了，否则就能直接看见罪魁祸首了；我们还需要进一步挖掘。

通过检查这些受影响进程的 `/proc/PID/environ` 可以看到，最早一批受影响的服务里面多了一个 `GDM_LANG=zh_CN.utf8` 的变量，而我并没有使用 gdm 而是 LightDM……情况已经比较清晰了。在绕了一些弯路之后，直接在 LightDM 的日志中找到了原因：

```
[+226739.95s] DEBUG: Greeter sets language zh_CN.utf8
```

问题出在 lightdm-gtk-greeter 这里。我有熟练的 grep 技巧，很快找到了最终负责拉取语言列表的代码：

```c
/* lightdm-1.22.0/liblightdm-gobject/language.c:60 */

static void
update_languages (void)
{
    gchar *command = "locale -a";
    gchar *stdout_text = NULL, *stderr_text = NULL;
    gint exit_status;
    gboolean result;
    GError *error = NULL;

    if (have_languages)
        return;

    result = g_spawn_command_line_sync (command, &stdout_text, &stderr_text, &exit_status, &error);

    /* ... */
}
```

嗯……这里调用了 `locale -a` 这个命令。很显然，作者默认它的输出中 `utf8` 才是正确的字符集写法，因为接下来就是

```c
/* lightdm-1.22.0/liblightdm-gobject/language.c:95 */

/* Ignore the non-interesting languages */
if (strcmp (command, "locale -a") == 0 && !g_strrstr (code, ".utf8"))
    continue;
```

这样的一个判断，可以看到代码丢掉了所有不以 `.utf8` 结尾的 locale。那么最后负责设置 `GDM_LANG` 和 `LANG` 等变量的代码就免责了，因为它们仅仅只是忠实地传达了最终来源于此处的信息而已：

```c
/* lightdm-1.22.0/src/seat.c:1000 */

static void
configure_session (Session *session, SessionConfig *config, const gchar *session_name, const gchar *language)
{
    /* ... */

    if (language && language[0] != '\0')
    {
        session_set_env (session, "LANG", language);
        session_set_env (session, "GDM_LANG", language);
    }
}


/* xfce4-session@989cb9b83e xfce4-session/main.c:88 */

static void
setup_environment (void)
{
  /* ... */

  /* this is for compatibility with the GNOME Display Manager */
  lang = g_getenv ("GDM_LANG");
  if (lang != NULL && strlen (lang) > 0)
    {
      g_setenv ("LANG", lang, TRUE);
      g_unsetenv ("GDM_LANG");
    }

  /* ... */
}
```

## 症结

那么“案件事实”应该说已经清楚了，我们把矛头指向 `locale -a`：

```
$ locale -a
C
en_US.utf8
ja_JP.utf8
POSIX
zh_CN.gbk
zh_CN.utf8
zh_TW.utf8
```

果然……为了排除合理怀疑，我们看一下 locale 的配置：

```sh
# /etc/locale.gen

zh_CN.UTF-8 UTF-8
zh_CN.GBK GBK
zh_TW.UTF-8 UTF-8
en_US.UTF-8 UTF-8
ja_JP.UTF-8 UTF-8
```

并确定 locale archive 生成过程不背锅：

```
$ sudo strace -f -e execve locale-gen

...
[pid 25836] execve("/usr/bin/localedef", ["/usr/bin/localedef", "-c", "-i", "zh_CN", "-f", "UTF-8", "-A", "/usr/share/locale/locale.alias", "--prefix", "/", "zh_CN.UTF-8"], 0x18505d0 /* 22 vars */) = 0
...
```

而最后生成的 `/usr/lib/locale/locale-archive` 里面就是错误的名字了，用 strings 可以轻易验证。

注意力转向 localedef，其实现在问题的症结已经很明显了，因为无论是 `locale` 还是 `localedef` 都是 libc 的组件！[果然](https://github.com/bminor/glibc/blob/glibc-2.26/locale/programs/localedef.c#L493-L533)：

```c
/* Normalize codeset name.  There is no standard for the codeset
   names.  Normalization allows the user to use any of the common
   names.  */
static const char *
normalize_codeset (const char *codeset, size_t name_len);
```

原来是 glibc 为了让用户不用死记硬背各种字符集名称的字母大小写、连字符加在哪，自己做了一层标准化，反正“字符集名称没有标准规定”……

其实就连官方都[一直知道这意味着什么][locale-names]，以至于搜索 `glibc locale name` 第一个结果就是它……

[locale-names]: https://www.gnu.org/software/libc/manual/html_node/Locale-Names.html

> **Portability Note:** With the notable exception of the standard locale names ‘C’ and ‘POSIX’, locale names are system-specific.

于是整个情况就是：

* 因为 glibc 内部根本无所谓各种字符集的原本拼写是什么反正都先标准化再用，导致
* glibc 的 `locale -a` 输出丧失与非 glibc 系统的互操作性，而
* Linux 生态系统各处都信赖自己的输入从而不做过多处理，于是
* glibc-特异性的 locale 设置一路渗透到了每一个 GUI 进程，最后
* 在 ssh 带着这些 locale 环境变量去敲 macOS 门的时候
* macOS 的 libc 炸裂了。


## 解决

按照把问题解决在最上游的原则，我们应该在哪里解决问题呢？显然我们不能修改 macOS 系统，因为它很封闭，[locale 相关部分巨坑][locale-keng]，并且我不熟悉；也显然不能在 glibc 层面，因为可能有很多应用都依赖 glibc 的这一“feature”了，那么就只能在 LightDM 一层动手了。

[locale-keng]: https://stackoverflow.com/q/9991603/596531

```diff
--- a/liblightdm-gobject/language.c	2017-08-19 18:02:33.773661324 +0800
+++ b/liblightdm-gobject/language.c	2017-08-19 18:09:08.886669723 +0800
@@ -96,8 +96,18 @@
             if (strcmp (command, "locale -a") == 0 && !g_strrstr (code, ".utf8"))
                 continue;

-            language = g_object_new (LIGHTDM_TYPE_LANGUAGE, "code", code, NULL);
+            /* Use the correct spelling of "UTF-8". */
+            size_t len_head = strlen (code) - 4;
+            size_t len_result = len_head + 6;
+            gchar *fixed_code = (gchar *) g_malloc (sizeof(gchar) * len_result);
+            strncpy (fixed_code, code, len_head);
+            strncpy (fixed_code + len_head, "UTF-8", 5);
+            *(fixed_code + len_result - 1) = '\0';
+
+            language = g_object_new (LIGHTDM_TYPE_LANGUAGE, "code", fixed_code, NULL);
             languages = g_list_append (languages, language);
+
+            g_free (fixed_code);
         }

         g_strfreev (tokens);
```

可见就是很蠢的字符串末尾暴力替换……

还有一段小插曲，重新编译 lightdm 之后怎么注销重新登陆都没用，一度非常沮丧，最后发现 lightdm 主进程从开机之后就没有死过，相反它注视着 X server 来来去去，并随时生出一个子进程指定进去……这么做的一个副作用是任何 greeter 界面里的配置更改都要等到 lightdm 服务重启之后才能生效，导致我试图从 `zh_CN.UTF-8` 临时切换走时发现不能切换，又费了一番周折。

总之，在 `systemctl restart lightdm` 之后，一切重归平静……


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
