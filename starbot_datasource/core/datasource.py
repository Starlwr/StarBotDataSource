import abc
import asyncio
import json
import os
from json import JSONDecodeError
from typing import List, Dict, Union, Optional, NoReturn, Set

from loguru import logger
from pydantic import ValidationError
from starbot_executor import executor

from ..core.event import EventType, DataSourceEvent
from ..core.model import Up
from ..exception.DataSourceException import DataSourceException


class DataSource(metaclass=abc.ABCMeta):
    """
    推送配置数据源基类
    """

    def __init__(self):
        self.ups: Set[Up] = set()
        self.uids: Set[int] = set()
        self.__up_map: Dict[int, Up] = {}

    def __getitem__(self, key):
        return self.__up_map[key]

    @abc.abstractmethod
    async def load(self) -> NoReturn:
        """
        读取配置，基类空实现
        """
        pass

    def add(self, up: Up) -> NoReturn:
        """
        动态添加主播

        Args:
            up: 主播实例
        """
        if up.uid in self.uids:
            raise DataSourceException(f"数据源中不可含有重复的主播 (UID: {up.uid})")

        self.ups.add(up)
        self.uids.add(up.uid)
        self.__up_map[up.uid] = up

        executor.dispatch(up, EventType.DataSourceEvent, DataSourceEvent.DataSourceAdded)

    def remove(self, uid: int) -> NoReturn:
        """
        动态移除主播

        Args:
            uid: 主播 UID
        """
        if uid not in self.uids:
            raise DataSourceException(f"主播 (UID: {uid}) 不存在于数据源中")

        up = self.__up_map.get(uid)
        self.ups.remove(up)
        self.uids.remove(uid)
        self.__up_map.pop(uid)

        executor.dispatch(up, EventType.DataSourceEvent, DataSourceEvent.DataSourceRemoved)

    def update(self, up: Up) -> NoReturn:
        """
        动态更新主播

        Args:
            up: 主播实例
        """
        if up.uid not in self.uids:
            raise DataSourceException(f"主播 (UID: {up.uid}) 不存在于数据源中")

        old = self.__up_map.get(up.uid)
        self.ups.remove(old)
        self.uids.remove(old.uid)
        self.__up_map.pop(old.uid)
        self.ups.add(up)
        self.uids.add(up.uid)
        self.__up_map[up.uid] = up

        executor.dispatch(up, EventType.DataSourceEvent, DataSourceEvent.DataSourceUpdated)


class DictDataSource(DataSource):
    """
    使用字典初始化的推送配置数据源
    """

    def __init__(self, dict_config: Union[List[Dict], Dict]):
        super().__init__()
        self.__config = dict_config

        if isinstance(self.__config, dict):
            self.__config = [self.__config]

    async def load(self) -> NoReturn:
        """
        从字典中初始化配置
        """
        if self.ups:
            return

        logger.info("已选用 Dict 作为 Bot 数据源")
        logger.info("开始从 Dict 中初始化 Bot 配置")

        for up in self.__config:
            try:
                self.add(Up(**up))
            except ValidationError as ex:
                raise DataSourceException(f"提供的配置字典中缺少必须的 {ex.errors()[0].get('loc')[-1]} 参数")

        logger.success(f"成功从 Dict 中导入了 {len(self.ups)} 个 UP 主")


class JsonDataSource(DataSource):
    """
    使用 JSON 初始化的推送配置数据源
    """
    def __init__(self, json_file: str, auto_reload: Optional[bool] = True, auto_reload_interval: Optional[int] = 5):
        super().__init__()
        self.__config = None

        self.__json_file = json_file
        self.__auto_reload = auto_reload
        self.__auto_reload_interval = auto_reload_interval

    async def load(self) -> NoReturn:
        """
        从 JSON 字符串中初始化配置
        """
        if self.ups:
            return

        logger.info("已选用 JSON 作为 Bot 数据源")
        logger.info("开始从 JSON 中初始化 Bot 配置")

        try:
            modify_time = os.path.getmtime(self.__json_file)
            with open(self.__json_file, encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            raise DataSourceException("JSON 文件不存在, 请检查文件路径是否正确")
        except UnicodeDecodeError:
            raise DataSourceException("JSON 文件编码不正确, 请将其转换为 UTF-8 格式编码后重试")
        except Exception as ex:
            raise DataSourceException(f"读取 JSON 文件异常 {ex}")

        try:
            self.__config = json.loads(content)
        except Exception:
            raise DataSourceException("JSON 文件内容格式不正确")

        if isinstance(self.__config, dict):
            self.__config = [self.__config]

        for up in self.__config:
            try:
                self.add(Up(**up))
            except ValidationError as ex:
                raise DataSourceException(f"提供的配置字典中缺少必须的 {ex.errors()[0].get('loc')[-1]} 参数")

        logger.success(f"成功从 JSON 中导入了 {len(self.ups)} 个 UP 主")

        if self.__auto_reload:
            executor.create_task(self.__auto_reload_task(modify_time))

    async def __auto_reload_task(self, modify_time: float) -> NoReturn:
        """
        JSON 文件内容发生变化时自动重载配置

        Args:
            modify_time: 配置文件修改时间
        """
        while True:
            await asyncio.sleep(self.__auto_reload_interval)
            try:
                new_modify_time = os.path.getmtime(self.__json_file)

                if new_modify_time == modify_time:
                    continue

                modify_time = new_modify_time

                logger.info(f"数据源配置已更新, 开始重载配置")

                with open(self.__json_file, encoding="utf-8") as file:
                    content = file.read()

                conf = json.loads(content)
                if isinstance(conf, dict):
                    conf = [conf]

                new_ups = []
                for up in conf:
                    new_ups.append(Up(**up))

                new_up_set = set(new_ups)
                if len(new_up_set) != len(new_ups):
                    raise DataSourceException("数据源中不可含有重复的主播")

                self.__config = conf

                added_ups = new_up_set - self.ups
                removed_ups = self.ups - new_up_set

                tip = [f'{act}了 {len(ups)} 个主播' for act, ups in [('新增', added_ups), ('移除', removed_ups)] if ups]
                if tip:
                    logger.info(f"检测到 {', '.join(tip)}")
                else:
                    logger.info("未检测到新增或移除的主播, 开始重载已存在主播的配置")

                for up in new_up_set.union(self.ups):
                    if up in added_ups:
                        self.add(up)
                    elif up in removed_ups:
                        self.remove(up.uid)
                    else:
                        self.update(up)

                logger.success("数据源配置重载成功")
            except FileNotFoundError:
                logger.error("数据源配置 JSON 文件不存在")
            except UnicodeDecodeError:
                logger.error("数据源配置 JSON 文件编码不正确, 请将其转换为 UTF-8 格式编码")
            except JSONDecodeError:
                logger.error("数据源配置 JSON 文件内容格式不正确")
            except DataSourceException as ex:
                logger.error(ex.msg)
            except Exception as ex:
                logger.error(f"数据源自动重载任务异常 {ex}")
            finally:
                continue
