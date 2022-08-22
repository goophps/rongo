from .Provider import Provider
from .. import helper
from ..configuration import config
from ..foundation import Manager, Application


class CacheProvider(Provider):
    def __init__(self, application: "Application"):
        self.application = application

    def register(self):
        # 创建缓存，然后绑定到容器
        cache = Manager(config("cache.stores")).driver()
        helper.bind("cache", cache)

    def boot(self):
        pass
