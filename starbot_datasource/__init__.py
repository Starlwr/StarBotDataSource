import platform

from .core.event import *
from .core.datasource import *

if 'windows' in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
