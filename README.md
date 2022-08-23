# Rongo
Rongo provides Service Container, Service Providers, Facades, Caching, Queues and Jobs, Broadcasting, Mail, Configuration management, 
Env file management..., combined with modern asynchronous micro-frameworks (fastapi, sanic), 
to become a very good and easy-to-use full-scale stack web framework.

Rongo提供容器、服务提供者、Facade、缓存、队列、广播、邮件、配置管理、env文件管理...,与现代异步微框架(fastapi、sanic)结合，
成为一个性能很好的非常好用的全栈 Web 框架。

### 简介
1、Rongo，与 Thinkphp Laravel 相同的架构，使用注册树模式构造了一个容器，程序启动时，把所有功能模块按需加载进入容器;

2、全部基于异步协程 asyncio 开发，性能很好;

3、代码的注释清晰、完整。

### 快速入门
创建并激活一个虚拟环境，支持 Python 3.7+ 
```
# 安装
pip install rongo

# 启动 -- 在你的应用入口文件里 (config_path是配置文件路径，具体模板可以直接去开发文档里抄)
import rongo.foundation
rongo.foundation.Application(config_path='config').register()

# 使用
from rongo.facades import Cache
await Cache.set('age', 18)
```

### 什么时候可以用于生产环境？
现在还处于初步开发阶段，等版本号到0.1.0的时候，就可以用于生产环境了。
版本0.1.0之前，会把基本功能写完；并把单元测试写完，测试覆盖率至少90%以上；以及一份完整的开发手册。

### 为什么有Rongo?
它很像框架，但还称不上框架。 本人特别喜欢 Thinkphp Laravel 这两个 PHP 框架，成熟稳定，功能齐全，但又做到了轻量，按需加载。 
python 语言方面的框架，成熟、稳定、性能好、又好用、又全面的框架，很少，几乎没有。 

我最早发现的是 Masonite， 跟我喜欢的两个 PHP 框架很像，功能全面， 架构方面也都是在框架启动时通过注册树模式把所有服务加载到内存中。 开发文档写得很好，很清晰。
我研究了它的功能，还参与翻译了开发手册，也看了底层代码。发现有些基本功能是缺失的，比如 ORM 模块无法定义联合索引； 还发现些常用的功能，有BUG， 我参与修复了其中一个BUG；
它底层代码，有点不太会用设计模式但又用得模有样的感觉；性能不好，比如它的 Cache 模块，循环 get 1万次1.5秒，我重写后 Rongo 是1秒。

后来我发现了 Django，它的热度非常高，据说成熟稳定，于是我决定好好研究它， 想着以后写 Python 方面的程序就用它。
但我经过整整一两个月的阅读文档、实践，依然学不会，不知是框架太难用，还是我太笨。个人感觉，Django 体系太杂，古老又杂乱无章。

后来我迷上了异步微框架，FastAPI，感觉发现了新大陆。性能特别好，代码特别清晰，类型提示特别完整，入参检测非常严谨又方便好用，深度自动化API文档。
学习成本也小，我用了一晚上把开发文档看了一遍，第二天写了会儿代码，基本就上手了。但在我心目中缺点是，它只是个微框架，只有 web 框架最基本的验证、请求和响应相关。

所以，有了Rongo

### 许可 License
Rongo 是在 MIT 许可下获得许可的开源软件。

The Rongo is open-sourced software licensed under the MIT license.




