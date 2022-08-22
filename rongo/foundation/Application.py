from __future__ import annotations
import os
import sys
from typing import List, TYPE_CHECKING, Type

from .. import helper
from ..configuration import Configuration, config
from ..container import Container
from ..facades import Config
from ..loader import Loader

if TYPE_CHECKING:
    from rongo.providers import Provider


class Application(Container):
    def __init__(self, base_path: str = '', config_path: str = 'config'):
        """
        应用(目录参数，用/分开，比如 config/admin)
        :param base_path: 根目录
        :param config_path: 配置文件目录
        """
        self.__base_path: str = base_path
        self.__config_path: str = config_path
        self.providers: list = []

    # 框架注册
    def register(self):
        if self.__config_path is ("" or None):
            return None

        # 先绑定些基础
        helper.bind("loader", Loader())
        # 绑定路径
        helper.bind("config.location", self.__config_path)

        # 加载配置文件
        configuration = Configuration(self)
        configuration.load()
        helper.bind("config", configuration)

        # 把所有配置的服务注册进来
        providers: list = config("providers.providers")
        for provider_class in providers:
            provider = provider_class(self)
            provider.register()
            self.providers.append(provider)

        # 把自己绑定到容器
        self.setInstance(self);
        helper.bind('app', self)
        return self

    def get_providers(self) -> List[Provider]:
        return self.providers

    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        # @removed:5.0.0
        if Config.has("application.debug"):
            return bool(Config.get("application.debug"))
        else:
            return True

    def is_dev(self) -> bool:
        """Check if app is running in development mode."""
        return not self.is_running_tests() and os.getenv("APP_ENV") in [
            "development",
            "local",
        ]

    def is_production(self) -> bool:
        """Check if app is running in production mode."""
        return os.getenv("APP_ENV") == "production"

    def is_running_tests(self) -> bool:
        """Check if app is running tests."""

        return "pytest" in sys.modules

    def is_running_in_console(self) -> bool:
        """Check if application is running in console. This is useful to only run some providers
        logic when used in console. We can differenciate if the application is being served or
        if an application command is ran in console."""
        if len(sys.argv) > 1:
            return sys.argv[1] != "serve"
        return True

    def environment(self) -> str:
        """Helper to get current environment."""
        if self.is_running_tests():
            return "testing"
        else:
            return os.getenv("APP_ENV")
