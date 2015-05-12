---
layout: post
title: '这个博客是怎样搭建的'
date: 2015-05-11 21:43:50
---

## 缘起

实际上, 早在 2013 年我就产生了开博的打算, 当时 GitHub Pages 已经算是知名度相当高的服务了.
于是我注册了域名, 建立了 Pages 的 repo, 开始研究一些静态站点生成的东西.
然而 GitHub Pages 采用的静态站点生成器是 Ruby 阵营的 Jekyll, 因为懒得配置 Ruby
开发环境的缘故, 就一直没有开工. 毕竟我平时不写 Ruby, 单纯为了写博客配一个环境,
怎么想都是小题大作吧. 然而静态站点一定是要用工具自动生成的; 手工维护 HTML 模板和
CSS 的不优雅程度更甚于专门配置一遍 Jekyll. 因为当时本科学习即将结束, 事情很多,
就一直拖着没时间写这么一个工具, 于是拖到了现在.

中间 2014 年 10 月份的时候, 掺和了 [PyCon China][pycon-china] 的网站建设, 听说了有
[staticjinja][] 这样的工具. 因为上半年做毕设接触了 Node.js 前端开发, 便产生了用
Python 搭建前端开发环境和构建系统的想法. 然而在随后的工作中, 发现 Python
的前端开发支持并没有想象中的良好, [pyScss][] 这样的关键项目与 Ruby 或者 Node.js
生态系统中的 [等价][ruby-sass] [项目][node-sass] 并未实现真正意义上的并驾齐驱 (parity).
当时在 CPyUG 社区内进行了讨论, 为了构建网站的静态部分, 要不要引入 Node.js 组件;
讨论的结果是为了简化部署流程, 维持纯 Python 的方案. 幸好踩到的坑都可以规避 (work around),
也给上游提交了补丁, 这一套静态站也是平稳地上了线.

当时对静态站点生成器的理解, 是一个类似 Grunt 的结构, 本质上由多个互相独立的任务组成.
至于知道以 Gulp 为代表的流式构建系统, 那是后来看到我一位入了前端坑的本科同学写的[介绍文章][gulp-intro]之后的事情了.
那时我已经比较熟悉 Grunt 的思维方式了, 就导致个人对 Gulp 始终没法理解,
但毕竟基于流的处理方式能避免读写临时文件的 I/O, 这一点性能优势倒是很快就体会到了,
于是就决定抽时间好好研究下 Gulp.

于是时间到了 2015 年的 4 月底, 我想着利用 "五一" 的假期顺便把博客做了吧, 试着起了一个
Gulp 的前端项目骨架, 这次 Gulp 的文档一下就看懂了.

我想是时候把这个坑填上了.

[pycon-china]: http://cn.pycon.org/
[staticjinja]: https://github.com/Ceasar/staticjinja
[pyScss]: https://github.com/Kronuz/pyScss
[ruby-sass]: https://github.com/sass/sass
[node-sass]: https://github.com/sass/node-sass
[gulp-intro]: http://www.cnblogs.com/myqianlan/p/4195999.html


## 思路

一个静态站点, 无非是由 HTML、CSS 组成的一堆文件, 可能还加上一些不涉及动态内容的 JS.
而构成站点实际内容的每个 HTML 页面里, 相当一部分却是公共的页面结构, 因此手工维护显然是不靠谱的.
解决这个问题早就有了现成方案 -- 模板系统 (templating). 然而手写 HTML 总之是比较蛋疼的;
尤其是使用过 Jade 这种模板语言之后给人的感受, 就像写过 Sass 之后再也不想手写裸
CSS 的感觉一样. 那么我们的想法就是:

* Jade -&gt; HTML
* Sass -&gt; CSS

这两步使用 Node.js 完成, 因为这样我就可以绕过 Python 前端工具比较弱的限制了.

我们的文章使用熟悉的 Markdown 撰写, Markdown 是编译成 HTML 的, 这部分内容要以某种方式综合到上一步生成的静态模板里.
其实在浏览器端用 JS 渲染 Markdown 的话也是可以的; 不过比较正统的方式还是一次性把所有工作都做完.
考虑到大部分现成的模板语言, 其标记本身都是直接写在 HTML 里的, 那我们为何不把标记写进 Jade 模板里,
这样 Jade 看见的是文本, 而编译的结果不就是另一个模板语言的合法输入了吗?

* Jade -&gt; Jinja2
* Markdown -&gt; HTML 片段
* Jinja2 -&gt; 完整 HTML 页面

选用 Jinja2 是考虑到以下几点:

* 语法和 Django 模板几乎一样, 写起来很爽, 我熟悉的另一个模板语言 Mako 写起来更像 PHP 的感觉, 代码跟输出是混在一起的, 相比之下就不够优雅
* Jekyll 的模板也是类似的语法, 对面阵营的小伙伴们也熟悉, 有群众基础
* 这货貌似已经比 Mako 快了 (Mako 首页曾经声称自己性能最高, 但现在已经变成了 "非常接近 Jinja2")
* Jade 貌似不方便扩展? 而且前一步是用 Node.js 完成的, 之后还是想用 Python

这就是整体的实现思路了.


## 实现

### Node.js 生成模板

并没有什么有趣的内容, 在此基本略过. 这部分代码位于博客 repo 的 `_src/` 目录下,
编译结果输出到 `_templates/` 目录 (被 .gitignore 了), 又加了个 BrowserSync
调试的功能, 其他的确实没什么了.


### Python 静态网页生成器

这是主要工作; 代码在 `_generator/` 目录里, 实际上是个独立的项目, 只不过暂且没什么闲情逸致推到 PyPI 上而已...
项目名字叫 Pybble (发音若 pebble), 是 `py-blog` 简化发音而来的.

Pybble 的架构是受 Gulp 启发的, 也是基于流的结构. 处理流程放在 `pybble.process` 包里 (`process` 这个名字也许会换掉, 不过先这么用着好了):

```python
# process/base.py
from ..stream import SkipFile


class BaseProcess(object):
    '''Base class for process passes.'''

    name = None
    anticausal = False

    def __init__(self, prev):
        self.prev = prev

    def run(self):
        '''Process a stream of StreamedFiles.'''
        return list(self.run_iter())

    def run_iter(self):
        if self.prev is None:
            # we're source
            for sf in self.stream_source():
                yield sf

            return

        # buffer input if we're anticausal
        if self.anticausal:
            input_files = self.prev.run()
            for sf in self.process_buffered(input_files):
                yield sf

            return

        # stream from the previous process
        for sf in self.prev.run_iter():
            try:
                yield self.process_file(sf)
            except SkipFile:
                # skip this file
                pass

    def process_file(self, sf):
        # base impl does nothing
        return sf

    def process_buffered(self, files):
        return files

    def stream_source(self):
        '''Provide the stream source if asked to be the source process.'''

        # base impl returns empty iterable
        return []
```

核心思路就是这样, 由多个 processes 相互连接构成一条流, 其中也允许一些 processes
看到所有文件而非流式处理, 就可以实现一些生成目录、标签这样的需要预先读取所有输入的功能了.
具体的实现都在 `pybble.process` 包里, 这里就不摘抄了... 比起具体流程的实现,
我们更关心这些流程是如何串起来的, 在 Pybble 里我们是通过配置文件来控制数据流的.
从命令行入口 (`pybble.cli`) 调用 `build` 命令时, 我们通过 `pybble.conf` 包加载
YAML 格式的配置文件, 里面就包含了 0 或多条流的定义; 这些定义将由 `pybble.driver`
包转化为相应的一串 process 类实例:

```python
# driver/__init__.py
from .. import process

import six


def stream_from_config(config):
    '''Instantiate linked processes from a stream config.'''

    return six.moves.reduce(_process_from_config, config, None)


def _process_from_config(sofar, process_decl):
    '''Instantiate a process with the given config.'''

    name, options = process_decl['name'], process_decl.get('args', {})
    return process.get_process(name, options, sofar)


# process/__init__.py
def get_process(name, params, prev_process=None):
    return _KNOWN_PROCESSES[name](prev_process, **params)
```

这里略去了注册流程类的内容... 如你所见, 就是一个实例化 processes 并相互连接的过程.

```python
# driver/__init__.py (continued)
class StreamDriver(object):
    '''Stream driver driving one or more streams.'''

    def __init__(self, streams, callback=None):
        self.streams = streams
        self.callback = callback

    @classmethod
    def from_config(cls, config, **kwargs):
        streams = [stream_from_config(stream_decl) for stream_decl in config]
        return cls(streams, **kwargs)

    def execute(self):
        nb_streams = len(self.streams)
        result_queue = queue.Queue(nb_streams)
        threads = [
                StreamDriverThread(process, str(idx), result_queue)
                for idx, process in enumerate(self.streams)
                ]

        for thread in threads:
            thread.start()

        for i in range(nb_streams):
            result = result_queue.get()
            if self.callback is not None:
                self.callback(result)

        # this shouldn't be necessary but do it anyway
        for thread in threads:
            thread.join()
```

多线程执行, 一个线程对应一条流, 于是我们可以实现很多条流同时运行了. 这里暂时无视掉
Python 的 GIL... 所幸 Python 在进行 I/O 操作时会释放 GIL, 对于 I/O-bound 的
Pybble 而言, 只能单线程跑 CPU-bound 的渲染过程对性能的影响应该并不大.

关于 Pybble 的配置, 文件名我参考了 Travis CI 的 `.travis.yml` 和 Jekyll 的
`_config.yml`, 取了一个十分山寨的 `_pybble.yml`, 在里头跑了两条流, 一条是编译 HTML 页面,
一条是拷贝静态 assets. 至于为什么不直接让 Gulp 输出成品的静态 assets 到 `static/`
目录呢? 这是考虑万一有需要再次预处理 assets 中的内容 (比如在 CSS 里注入点生成内容什么的),
就不必改目录结构了.


### Wrapping it up

为了少打字, 我又写了一个简单的 Makefile, 这样就可以打 `make` 构建整个站点啦.
当然, 相比 Jekyll 的服务器端自动运行, Pybble 只能在本地运行, 相应地每次更新完内容都要多做一次 commit,
显得十分不优雅; 但毕竟这一点无法 work around, 就忍了吧. 至于为什么我没有放一个
`.nojekyll` 完全禁用 Jekyll? 我测试过, 显然禁用了 Jekyll 会造成所有跟内容无关的文件都出现在网站目录下,
包括所有的配置文件和构建系统相关的内容... 出于强迫症, 我觉得留着 Jekyll 让它实现一个选择性拷贝的功能还是不错的, 所以就把 `.nojekyll` 给 revert 掉了.


## 后记

其实这一套系统还可以做到更多, 比如支持个标签啦分类什么的, 本质上跟实现首页文章索引没什么区别;
加个评论模块也很方便, 实际上评论模块对站点生成器而言就是一段静态代码, 直接写进模板就好.
不过目前来看, 先做这么多吧, 还有很多事情要做呢, 知乎上好像还有好多坑没填呢... (逃
