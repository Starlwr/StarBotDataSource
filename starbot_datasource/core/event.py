from enum import Enum


class EventType:
    """
    事件类型枚举，基于本项目开发时，可通过继承此类的方式扩展事件类型
    """
    DataSourceEvent = "DataSourceEvent"
    """数据源事件"""


class DataSourceEvent(Enum):
    """
    数据源事件类型枚举
    """
    DataSourceAdded = "DataSourceAdded"
    """数据源主播新增"""

    DataSourceRemoved = "DataSourceRemoved"
    """数据源主播移除"""

    DataSourceUpdated = "DataSourceUpdated"
    """数据源主播更新"""
