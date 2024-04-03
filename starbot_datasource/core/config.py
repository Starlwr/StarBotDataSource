import json
from json import JSONDecodeError
from typing import Dict, Any, Type, Optional

from loguru import logger

from ..exception.DataSourceException import DataSourceException


class Config:
    """
    全局配置类
    """

    __config: Dict[str, Any]

    def __init__(self):
        try:
            with open("config.json", encoding="utf-8") as file:
                self.__config = json.loads(file.read())
        except Exception as ex:
            if isinstance(ex, FileNotFoundError):
                logger.error("配置文件 config.json 不存在")
            elif isinstance(ex, UnicodeDecodeError):
                logger.error("配置文件 config.json 编码不正确, 请将其转换为 UTF-8 格式编码")
            elif isinstance(ex, JSONDecodeError):
                logger.error("配置文件 config.json 内容格式不正确")
            else:
                logger.error(f"读取配置文件 config.json 异常 {ex}")
            raise DataSourceException("读取配置文件 config.json 异常")

    def get(self, attribute: str, _type: Type, default: Optional[Any] = None) -> Optional[Any]:
        """
        获取配置项的值

        Args:
            attribute: 配置项，多个配置项之间可使用.分隔
            _type: 预期类型，若类型不匹配会产生警告，并尝试进行自动转换
            default: 默认值，若要获取的配置项不存在或类型转换失败，返回默认值。默认：None

        Returns:
            配置项的值，若要获取的配置项不存在或类型转换失败，返回默认值
        """
        keys = attribute.split(".")
        conf = self.__config

        for key in keys:
            if not isinstance(conf, dict):
                logger.warning(f"配置项 {attribute} 不存在, 已使用默认值: {default}, 请补全配置文件 config.json")
                return default

            if key not in conf:
                logger.warning(f"配置项 {attribute} 不存在, 已使用默认值: {default}, 请补全配置文件 config.json")
                return default

            conf = conf[key]

        if isinstance(conf, _type):
            return conf

        logger.warning(
            f"配置项 {attribute} 数据类型不正确, 预期类型: {_type}, 实际类型: {type(conf)}, 请检查配置文件 config.json"
        )

        try:
            auto_cast_value = _type(conf)
            logger.success(f"配置项 {attribute} 数据类型自动转换成功")
            return auto_cast_value
        except Exception:
            logger.warning(f"配置项 {attribute} 数据类型自动转换失败, 已使用默认值: {default}, 请检查配置文件 config.json")
            return default


config: Config = Config()
