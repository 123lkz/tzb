# 日志管理模块使用指南

本文档介绍如何在爬虫项目中使用新的日志管理模块生成每次运行新的日志文件。

## 功能特点

* 每次运行自动生成新的日志文件，文件名包含时间戳
* 同时输出到控制台和文件
* 支持多个不同的日志器，方便区分不同模块的日志
* 提供统一的日志格式和级别配置
* 自动创建日志目录

## 基本用法

### 在脚本入口处配置根日志器

```python
from recruitment_spider.utils.log_manager import configure_root_logger

# 配置根日志器，spider_name参数用于生成日志文件名
logger = configure_root_logger("spider_name")
logger.info("这是使用根日志器的日志消息")
```

### 在模块中获取特定日志器

```python
from recruitment_spider.utils.log_manager import get_logger

# 第一个参数是日志器名称，第二个参数是爬虫名称（用于生成文件名）
logger = get_logger(__name__, "spider_name")
logger.info("这是模块中的日志消息")
```

### 设置不同的日志级别

```python
import logging
from recruitment_spider.utils.log_manager import get_logger

# 配置DEBUG级别的日志器
logger = get_logger(__name__, "spider_name", level=logging.DEBUG)
logger.debug("这是一条调试日志")
logger.info("这是一条信息日志")
```

## 日志文件位置

日志文件保存在项目根目录下的`logs`文件夹中，文件名格式为：`{spider_name}_{timestamp}.log`。

例如：`boss_spider_20240320_153045.log`

## 已集成的文件

以下文件已经集成了新的日志管理模块：

1. `recruitment_spider/run_recruitment_spider.py` - 主启动脚本
2. `run_boss_spider.py` - BOSS直聘爬虫专用启动脚本
3. `run_zhilian_spider.py` - 智联招聘爬虫专用启动脚本
4. `recruitment_spider/spiders/base_spider.py` - 爬虫基类
5. `recruitment_spider/utils/proxy_manager.py` - 代理管理器

## 示例代码

查看 `recruitment_spider/log_example.py` 了解完整的使用示例。

## 注意事项

1. 确保环境变量 `PROJECT_ROOT` 已正确设置，日志管理模块依赖此环境变量来确定日志文件路径
2. 日志管理模块会自动创建 `logs` 目录，无需手动创建
3. 如果您需要在现有代码中集成日志管理模块，请替换 `logging.basicConfig()` 调用为对应的 `configure_root_logger()` 或 `get_logger()`

## 常见问题

**Q: 如何在不同的爬虫中使用不同的日志文件？**

A: 在每个爬虫的入口脚本中，使用不同的 `spider_name` 参数调用 `configure_root_logger()`。

**Q: 如何修改日志格式？**

A: 目前日志格式在 `log_manager.py` 中统一配置，如需修改，请编辑该文件中的 `formatter` 定义。

**Q: 如何查看历史日志？**

A: 所有日志文件都保存在 `logs` 目录下，不会被覆盖，可以随时查看。 