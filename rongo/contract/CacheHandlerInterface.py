from abc import ABCMeta, abstractmethod
from typing import Any


class CacheHandlerInterface(metaclass=ABCMeta):
    """
    缓存接口类
    """

    @abstractmethod
    async def has(self, name: str) -> bool:
        """
        判断缓存
        :param name: 缓存的key
        :return:
        """
        pass

    @abstractmethod
    async def get(self, name: str, default=None) -> Any:
        """
        读取缓存
        :param name: 缓存的key
        :param default: 默认值
        :return:
        """
        pass

    @abstractmethod
    async def set(self, name: str, value, expire: int = None) -> bool:
        """
        设置缓存
        :param name: 缓存的key
        :param value: 值
        :param expire: 过期时间(秒)
        :return:
        """
        pass

    @abstractmethod
    async def increment(self, name: str, step: int = 1) -> int:
        """
        自增(针对数值缓存)
        :param name: 缓存的key
        :param step: 步长
        :return: 一个新值
        """
        pass

    @abstractmethod
    async def decrement(self, name: str, step: int = 1) -> int:
        """
        自减(针对数值缓存)
        :param name: 缓存的key
        :param step: 步长
        :return: 一个新值
        """
        pass

    @abstractmethod
    async def delete(self, name: str) -> bool:
        """
        删除缓存
        :param name: 缓存的key
        :return:
        """
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """
        清除缓存
        :return:
        """
        pass

    @abstractmethod
    async def clear_tag(self, keys: list) -> bool:
        """
        删除缓存标签
        :param keys: 缓存标识列表
        :return:
        """
        pass

    @abstractmethod
    def handler(self):
        """
        获取缓存句柄
        :return:
        """
        pass

    @abstractmethod
    async def locked(self, name: str) -> bool:
        """
        上锁
        :param name: 锁标识
        :return:
        """
        pass

    @abstractmethod
    async def unlock(self, name: str) -> bool:
        """
        解锁
        :param name: 锁标识
        :return:
        """
        pass

