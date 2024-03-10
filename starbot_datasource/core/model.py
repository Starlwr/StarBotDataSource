from typing import Optional, List, Union

from pydantic import BaseModel


class LiveOn(BaseModel):
    """
    开播推送配置
    可使用构造方法手动传入所需的各项配置
    或使用 LiveOn.default() 获取功能全部开启的默认配置
    """

    enabled: bool = False
    """是否启用开播推送。默认：False"""

    message: str = ""
    """
    开播推送内容模板。
    专用占位符: {uname} 主播昵称，{title} 直播间标题，{url} 直播间链接，{cover} 直播间封面图。
    通用占位符: {next} 消息分条，{atall} @全体成员，{at=114514} @指定成员，
              {urlpic=链接} 网络图片，{pathpic=路径} 本地图片，{base64pic=base64字符串} base64图片。
    默认：""
    """

    @classmethod
    def default(cls):
        """
        获取功能全部开启的默认 LiveOn 实例
        默认配置：启用开播推送，推送内容模板为 "{uname} 正在直播 {title}\n{url}{next}{cover}"
        """
        return LiveOn(enabled=True, message="{uname} 正在直播 {title}\n{url}{next}{cover}")


class LiveOff(BaseModel):
    """
    下播推送配置
    可使用构造方法手动传入所需的各项配置
    或使用 LiveOff.default() 获取功能全部开启的默认配置
    """

    enabled: bool = False
    """是否启用下播推送。默认：False"""

    message: str = ""
    """
    下播推送内容模板。
    专用占位符: {uname} 主播昵称。
    通用占位符: {next} 消息分条，{atall} @全体成员，{at=114514} @指定成员，
              {urlpic=链接} 网络图片，{pathpic=路径} 本地图片，{base64pic=base64字符串} base64图片。
    默认：""
    """

    @classmethod
    def default(cls):
        """
        获取功能全部开启的默认 LiveOff 实例
        默认配置：启用下播推送，推送内容模板为 "{uname} 直播结束了"
        """
        return LiveOff(enabled=True, message="{uname} 直播结束了")


class LiveReport(BaseModel):
    """
    直播报告配置，直播报告会在下播推送后发出，下播推送是否开启不会影响直播报告的推送
    可使用构造方法手动传入所需的各项配置
    或使用 LiveReport.default() 获取功能全部开启的默认配置
    """

    enabled: bool = False
    """是否启用直播报告。默认：False"""

    logo: Optional[str] = None
    """主播立绘的路径，会绘制在直播报告右上角合适位置。默认：None"""

    logo_base64: Optional[str] = None
    """主播立绘的 Base64 字符串，会绘制在直播报告右上角合适位置，立绘路径不为空时优先使用路径。默认：None"""

    time: bool = False
    """是否展示本场直播直播时间段和直播时长。默认：False"""

    fans_change: bool = False
    """是否展示本场直播粉丝变动。默认：False"""

    fans_medal_change: bool = False
    """是否展示本场直播粉丝团（粉丝勋章数）变动。默认：False"""

    guard_change: bool = False
    """是否展示本场直播大航海变动。默认：False"""

    danmu: bool = False
    """是否展示本场直播收到弹幕数、发送弹幕人数。默认：False"""

    box: bool = False
    """是否展示本场直播收到盲盒数、送出盲盒人数、盲盒盈亏。默认：False"""

    gift: bool = False
    """是否展示本场直播礼物收益、送礼物人数。默认：False"""

    sc: bool = False
    """是否展示本场直播 SC（醒目留言）收益、发送 SC（醒目留言）人数。默认：False"""

    guard: bool = False
    """是否展示本场直播开通大航海数。默认：False"""

    danmu_ranking: int = 0
    """展示本场直播弹幕排行榜的前多少名，0 为不展示。默认：0"""

    box_ranking: int = 0
    """展示本场直播盲盒数量排行榜的前多少名，0 为不展示。默认：0"""

    box_profit_ranking: int = 0
    """展示本场直播盲盒盈亏排行榜的前多少名，0 为不展示。默认：0"""

    gift_ranking: int = 0
    """展示本场直播礼物排行榜的前多少名，0 为不展示。默认：0"""

    sc_ranking: int = 0
    """展示本场直播 SC（醒目留言）排行榜的前多少名，0 为不展示。默认：0"""

    guard_list: bool = False
    """是否展示本场直播开通大航海观众列表。默认：False"""

    box_profit_diagram: bool = False
    """是否展示本场直播的盲盒盈亏曲线图。默认：False"""

    danmu_diagram: bool = False
    """是否展示本场直播的弹幕互动曲线图。默认：False"""

    box_diagram: bool = False
    """是否展示本场直播的盲盒互动曲线图。默认：False"""

    gift_diagram: bool = False
    """是否展示本场直播的礼物互动曲线图。默认：False"""

    sc_diagram: bool = False
    """是否展示本场直播的 SC（醒目留言）互动曲线图。默认：False"""

    guard_diagram: bool = False
    """是否展示本场直播的开通大航海互动曲线图。默认：False"""

    danmu_cloud: bool = False
    """是否生成本场直播弹幕词云。默认：False。默认：False"""

    @classmethod
    def default(cls):
        """
        获取功能全部开启的默认 LiveReport 实例
        默认配置：启用直播报告，无主播立绘，展示直播时间段和直播时长，展示粉丝变动，展示粉丝团（粉丝勋章数）变动，展示大航海变动
                展示收到弹幕数、发送弹幕人数，展示收到盲盒数、送出盲盒人数、盲盒盈亏，展示礼物收益、送礼物人数
                展示 SC（醒目留言）收益、发送 SC（醒目留言）人数，展示开通大航海数
                展示弹幕排行榜前 3 名，展示盲盒数量排行榜前 3 名，展示盲盒盈亏排行榜前 3 名，展示礼物排行榜前 3 名
                展示 SC（醒目留言）排行榜前 3 名，展示开通大航海观众列表
                展示盲盒盈亏曲线图，展示弹幕互动曲线图，展示盲盒互动曲线图，展示礼物互动曲线图，
                展示 SC（醒目留言）互动曲线图，展示开通大航海互动曲线图，
                生成弹幕词云
        """
        return LiveReport(enabled=True, logo=None, logo_base64=None,
                          time=True, fans_change=True, fans_medal_change=True, guard_change=True,
                          danmu=True, box=True, gift=True, sc=True, guard=True,
                          danmu_ranking=3, box_ranking=3, box_profit_ranking=3, gift_ranking=3, sc_ranking=3,
                          guard_list=True, box_profit_diagram=True,
                          danmu_diagram=True, box_diagram=True, gift_diagram=True, sc_diagram=True, guard_diagram=True,
                          danmu_cloud=True)


class DynamicUpdate(BaseModel):
    """
    动态推送配置
    可使用构造方法手动传入所需的各项配置
    或使用 DynamicUpdate.default() 获取功能全部开启的默认配置
    """

    enabled: bool = False
    """是否启用动态推送。默认：False"""

    message: str = ""
    """
    动态推送内容模板。
    专用占位符: {uname} 主播昵称，{action} 动态操作类型（发表了新动态，转发了新动态，投稿了新视频...），
              {url} 动态链接（若为发表视频、专栏等则为视频、专栏等对应的链接），{picture} 动态图片。
    通用占位符: {next} 消息分条，{atall} @全体成员，{at=114514} @指定成员，
              {urlpic=链接} 网络图片，{pathpic=路径} 本地图片，{base64pic=base64字符串} base64图片。
    默认：""
    """

    @classmethod
    def default(cls):
        """
        获取功能全部开启的默认 DynamicUpdate 实例
        默认配置：启用动态推送，推送内容模板为 "{uname} {action}\n{url}{next}{picture}"
        """
        return DynamicUpdate(enabled=True, message="{uname} {action}\n{url}{next}{picture}")


class Platform(BaseModel):
    """
    推送平台类
    """
    name: str
    """推送平台唯一标识符，请使用 平台名称/自定义名称(建议使用推送平台实现所在的代码仓库名) 的格式，并注意唯一性，例：QQ/StarBot"""

    account: Union[int, str]
    """机器人账号"""

    def __eq__(self, other):
        if isinstance(other, Platform):
            return self.name == other.name and self.account == other.account
        return False

    def __hash__(self):
        return hash(self.name) ^ hash(self.account)


class PushTarget(BaseModel):
    """
    推送目标类
    """

    id: Union[int, str]
    """推送目标标识符，一般为账号或群号"""

    platform: Platform
    """推送平台"""

    live_on: LiveOn = LiveOn()
    """开播推送配置。默认：LiveOn()"""

    live_off: LiveOff = LiveOff()
    """下播推送配置。默认：LiveOff()"""

    live_report: LiveReport = LiveReport()
    """直播报告配置。默认：LiveReport()"""

    dynamic_update: DynamicUpdate = DynamicUpdate()
    """动态推送配置。默认：DynamicUpdate()"""

    def __eq__(self, other):
        if isinstance(other, PushTarget):
            return self.id == other.id and self.platform == other.platform
        return False

    def __hash__(self):
        return hash(self.id) ^ hash(self.platform)


class Up(BaseModel):
    """
    主播类
    """

    uid: int
    """主播 UID"""

    targets: List[PushTarget]
    """主播所需推送的推送目标"""

    def __eq__(self, other):
        if isinstance(other, Up):
            return self.uid == other.uid
        return False

    def __hash__(self):
        return hash(self.uid)

    def is_need_connect(self) -> bool:
        """
        根据开播、下播、直播报告开关，判断是否需要连接直播间

        Returns:
            是否需要连接直播间
        """
        return any([
            any(map(lambda conf: conf.enabled, map(lambda group: group.live_on, self.targets))),
            any(map(lambda conf: conf.enabled, map(lambda group: group.live_off, self.targets))),
            any(map(lambda conf: conf.enabled, map(lambda group: group.live_report, self.targets)))
        ])
