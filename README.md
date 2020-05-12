# 一款基于 NoneBot 的多功能 QQ 聊天机器人

这个项目作为 2019-2020 第二学期数据结构课程设计大作业选题，由我的同学 [@8421BCD](https://github.com/8421BCD) 、 [@HoralG](https://github.com/HoralG) 和我 [@Singularity0909](https://github.com/Singularity0909/) 共同完成，是一款基于 NoneBot 的功能型 QQ 聊天机器人核心，具有智能闲聊、过滤有害信息、提供天气预报查询服务等常用功能，目前以机器人方天宇 (QQ: `2737676753`) 作为表现层。

[NoneBot](https://nonebot.cqp.moe/) 是一套基于 [CoolQ](https://cqp.cc/) 的 Python 异步 QQ 机器人框架，它会对 QQ 机器人收到的消息进行解析和处理，并以插件化的形式分发给消息所对应的命令处理器和自然语言处理器来完成具体的功能。

## 配置运行

本项目基于 NoneBot ，因此在尝试运行本项目前请先查阅文档了解 NoneBot 的基本使用方法。

```bash
# 克隆项目
git clone https://github.com/Singularity0909/awesome-bot.git && cd awesome-bot

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate # Windows
source ./venv/bin/activate # Linux/macOS

# 安装依赖
pip install -r requirements.txt

# 运行
python bot.py
```

注意，在运行项目前请先在项目根目录下创建目录 `tmp` ，并将项目根目录下的 `config.py.sample` 重命名为 `config.py` 并完成以下配置。

```python
# config.py
from nonebot.default_config import *

HOST = '127.0.0.1' # 监听 IP，默认为 127.0.0.1
PORT = 8080 # 监听端口，默认为 8080
SUPERUSERS = {} # 超级用户的 QQ 账号
NICKNAME = {'', '', ''} # 机器人的昵称
COMMAND_START = {'', '/', '$'} # 命令的起始字符，默认为空字符、/ 或 $
API_ROOT = 'http://127.0.0.1:5700' # 调用 CQHTTP API 所指定的 IP 和端口，注意要与 CQHTTP 配置一致，默认为 127.0.0.1:5700
APP_ID = '' # 调用腾讯 AI 功能的 APPID
APP_KEY = '' # 调用腾讯 AI 功能的 APPKEY
IMG_DIR = '' # CoolQ 图片消息存放路径，例如 D:\CoolQ Pro\data\image
```

## 功能模块

### 垃圾文本信息过滤

此功能仅限群聊且无需 @，如需自动撤回违规信息请为机器人开启管理员权限。

检测过程包含两种模式：AC 自动机 (Aho-Corasick automaton) 和朴素贝叶斯文本分类 (Naive Bayesian Classifier)。

有关 AC 自动机的实现可以参考我的一篇[博文](https://www.macrohard.cn/archives/22/)，敏感词库可自行在 [patterns.txt](/awesome/data/patterns.txt) 中配置。

朴素贝叶斯文本分类部分的工作由 [@8421BCD](https://github.com/8421BCD) 完成，目前非法完整句识别情况如下。

[参考文章](https://zhuanlan.zhihu.com/p/25835417) [项目仓库](https://github.com/8421BCD/Naive-Bayes-Classifier)

![](https://oss.macrohard.cn/img/screenshot/20200511122803.png)

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200511120735.gif)

### 色情暴恐图片信息过滤

此功能仅限群聊且无需 @，如需自动撤回违规信息请为机器人开启管理员权限。

依托腾讯领先的 DeepEye 图片鉴黄技术，准确快速输出每张目标图片属于“正常”、“性感”、“色情”的概率，有效帮助用户鉴别色情图片。该技术大幅提升了色情内容的打击覆盖面和打击效率，成倍地解放甄别人力，助力网络环境更健康。

腾讯暴恐图片识别基于腾讯领先的深度学习引擎，对用户上传的图片进行自动甄别，暴恐识别算法会返回“疑似暴恐”的字段，对血腥、暴力等图片进行自动打击，用AI捍卫互联网安全，助力建立安全、健康的互联网环境。

获取详情可访问[此处](https://ai.qq.com/product/terror.shtml)，如需使用请在 `config.py` 中填写腾讯 AI 的 APPID 及 APPKEY 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512192229.gif)

### 智能闲聊

此功能在私聊和群聊中均可使用，在群聊中需要 @ 或以机器人昵称开头发送信息。

腾讯闲聊服务基于 AI Lab 领先的 NLP 引擎能力、数据运算能力和千亿级互联网语料数据的支持，同时集成了广泛的知识问答能力，可实现上百种自定义属性配置，以及男、女不同的语言风格及说话方式，从而让聊天变得更睿智、简单和有趣。

获取详情可访问[此处](https://ai.qq.com/product/nlpchat.shtml)，如需使用请在 `config.py` 中填写腾讯 AI 的 APPID 及 APPKEY 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512123951.gif)

### 复读机

此功能仅限群聊且无需 @ 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512125109.gif)

### 天气预报

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【weather / 天气 / 查天气 / 天气预报】+ 空格 + 城市名，若关键词不在开头则调用自然语言处理。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512130754.gif)

### 翻译

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【translate / 翻译 / 翻译一下】+ 空格 + 需要翻译的文本，若文本是中文则翻译结果为英文，否则翻译结果均为中文。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512131804.gif)

### 剪切板

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【pastebin / 剪切板 / 贴代码 / 粘贴代码】，随后分别发送代码语言及内容。

目前语法仅支持纯文本、C/C++、Java、Python、Bash、Markdown、JSON、Go 。

文本共享服务及其 API 由 [@Lucien](https://github.com/LucienShui) 提供。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512133136.gif)

### 知乎日报

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【zhihu / 知乎 / 知乎日报】。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512133646.gif)

### 狗屁不通生成器

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【bullshit / 狗屁不通 / 狗屁不通生成器】+ 空格 + 主题。

核心功能引用自 [@meng ke](https://github.com/menzi11) 的项目 [BullshitGenerator](https://github.com/menzi11/BullshitGenerator) 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512134418.gif)

### 每日一句

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【daily / 每日一句】。

内容来源：[爱词霸](http://news.iciba.com/views/dailysentence/) 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512134926.gif)

### 一言

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【hitokoto / 一言】。

内容来源：[一言](https://hitokoto.cn/) 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512135229.gif)

### 笑话

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【joke / 笑话 / 讲个笑话 / 来个笑话】。

内容来源：[RollToolsApi](https://www.mxnzp.com) 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512135837.gif)

### 土味情话

此功能在私聊和群聊中均可使用，在群聊中无需 @ 。

命令关键词：【lovelive / 土味情话】。

内容来源：[渣男：说话的艺术](https://lovelive.tools/) 。

[**测试效果**](https://oss.macrohard.cn/img/screenshot/20200512135827.gif)
