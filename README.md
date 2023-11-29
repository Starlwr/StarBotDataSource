<div align="center">

# StarBotDataSource

[![PyPI](https://img.shields.io/pypi/v/starbot-bilibili-datasource)](https://pypi.org/project/starbot-bilibili-datasource)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11-blue)](https://www.python.org)
[![License](https://img.shields.io/github/license/Starlwr/StarBotDataSource)](https://github.com/Starlwr/StarBotDataSource/blob/master/LICENSE)
[![STARS](https://img.shields.io/github/stars/Starlwr/StarBotDataSource?color=yellow&label=Stars)](https://github.com/Starlwr/StarBotDataSource/stargazers)

**StarBot 推送配置数据源**
</div>

## 用途

* 已内置 字典数据源(DictDataSource) 和 JSON 数据源(JsonDataSource) 实现
* 可自行实现其他来源的推送配置数据源

## 快速开始
### 安装

```shell
pip install starbot-bilibili-datasource
```

### 开发

通过继承抽象类 DataSource 并实现其中的 load 抽象方法，即可实现其他来源的推送配置数据源

```python
from typing import NoReturn

from loguru import logger
from starbot_datasource import DataSource


class CustomDataSource(DataSource):
    """
    自定义推送配置数据源实现
    """
    async def load(self) -> NoReturn:
        """
        初始化配置
        """
        if self.ups:
            return

        logger.info("已选用 自定义来源 作为 Bot 数据源")
        logger.info("开始从 自定义来源 中初始化 Bot 配置")
        
        # 在此实现初始化逻辑
        pass

        logger.success(f"成功从 自定义来源 中导入了 {len(self.ups)} 个 UP 主")
```

## 鸣谢

* [StarBotExecutor](https://github.com/Starlwr/StarBotExecutor): 一个基于订阅发布模式的异步执行器
