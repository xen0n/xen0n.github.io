---
title: 'Python 奇技淫巧: 一种简单的 Python / Shell 双语程序'
date: 2016-06-04T23:07:51+08:00
draft: false
aliases:
    - /2016/06/04/simple-polyglot-python-trick/
---

最近经常见到 `:` 这个 Shell built-in, 比较好奇, 于是 StackOverflow 了一下.
过程中偶然看到了[这个技巧][js-polyglot-answer], 为了阅读方便把代码转载了过来,
有少许改动 (让程序实际可执行):

[js-polyglot-answer]: http://stackoverflow.com/a/34534006

```sh
#!/usr/bin/env sh
':' //; exec "$(command -v node)" "$0" "$@"
~function() { console.log('hello world'); }
```

```js
#!/usr/bin/env sh
':' //; exec "$(command -v node)" "$0" "$@"
~function() { console.log('hello world'); }
```

如你所见, 这段代码既是合法的 Shell 程序又是合法的 JS 程序, 把它当作 Shell
程序执行的话它的唯一功能是用 Node.js 重新执行一遍自己, 于是以下调用它的方式都能正常工作:

* `./foo`
* `sh ./foo`
* `node ./foo`

结合语法高亮的提示, 不难发现其中关键在于 `:` 相当于一个 `true` 即空操作,
因为 `//` 不是 Shell 的注释所以 Shell 会直接去执行 `exec` 然后自己就变成 Node
了. 而 Node 会无视 shebang 行 (即使 `#` 不是合法的 JS), `//` 又是 JS 注释,
这样 `':'` 就相当于一个它不认识的 `use strict` 一样的东西了, 也被无视.
于是剩下的内容就是一个 IIFE 了, 会被立即执行, 整体的流程比较简单.

那么我们来写一个 Python 版的吧!

```python
#!/bin/sh
':' #; exec "$(command -v python)" "$0" "$@"
print('hello world')
```

嗯... 这样不太合适, 因为 `#` 既是 Python 注释也是 Shell 注释, 这样整个第一行在
Shell 看来就没有 `exec` 了! 但是 Python 只有 `#` 一种注释,
用字符串的话因为引号数量要平衡, 也不能让这一行在 Python 和 Shell 解释不一致,
那怎么办呢?

有没有想到一种同样经常使用在文件开头的 Python 字符串?

对了! 就是它! 文档字符串!

```python
#!/bin/sh
# -*- coding: utf-8 -*-

''':' ; exec "$(command -v python)" "$0" "$@"
'''

print('hello world')
```

```sh
#!/bin/sh
# -*- coding: utf-8 -*-

''':' ; exec "$(command -v python)" "$0" "$@"
'''

print('hello world')
```

Shell 没有三撇的说法, `''':'` 在 Shell 看来是两撇 `''` 加上一个 `':'`,
于是我们同样成功地让 Shell 在第一行就把自己换成 Python 了. 而在 Python 看来,
整个第一行到下一行的三撇都是一整个字符串, 直接无视, 于是我们达到了同样的效果!


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
