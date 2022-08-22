import builtins
import datetime
import hashlib
import time
from abc import ABCMeta
from functools import wraps

from .TagSet import TagSet
from ..contract.CacheHandlerInterface import CacheHandlerInterface
from typing import Any

from ..foundation import Manager


class Cache(Manager, CacheHandlerInterface, metaclass=ABCMeta):
    """
    缓存基类。 所有子类，都得承继此类
    """

    def __init__(self, options: dict = None):
        super().__init__()
        self.options = options
        self.tags = {}

    def store(self, name="default"):
        """
        连接或者切换缓存
        :param name: 驱动名
        :return: 驱动实例
        """
        return self.driver(name)

    def get_expire_time(self, expire: int = None) -> int:
        """
        获取过期时间
        :param expire: 过期时间
        :return:
        """

        if expire is None:
            return self.options.get('expire')
        else:
            return expire

    def get_cache_key(self, name: str) -> str:
        """
        获取缓存key
        :param name: 缓存key
        :return:
        """
        return self.options['prefix'] + name

    async def pull(self, name: str) -> Any:
        """
        读取缓存并删除
        :param name: 缓存key
        :return:
        """
        result = await self.get(name)
        if result:
            await self.delete(name)
            return result
        return None

    async def push(self, name: str, value, limit: int = 1000) -> bool:
        """
        追加（列表）缓存
        :param name: 缓存key
        :param value: 存储的数据
        :param limit: 限制最大数量
        :return:
        """
        item = await self.get(name, [])

        if isinstance(item, list) is not True:
            raise ValueError('only list cache can be push')

        item.append(value)
        if len(item) > limit:
            item.pop(0)

        # 保留顺序去重，再存入
        return await self.set(name, list(set(item)).sort(key=item.index))

    async def append(self, name: str, value) -> bool:
        """
        追加TagSet数据
        :param name: 缓存的key
        :param value: 存储的数据
        :return:
        """
        return await self.push(name, value)

    async def add(self, name: str, value: Any, expire: int = None) -> bool:
        """
        如果不存在则写入缓存
        :param name: 缓存的key
        :param value: 存储的数据
        :param expire: 过期时间
        :return: 成功写入返回true，如果已存在则返回false
        """
        if await self.has(name):
            return False
        timestamp = datetime.datetime.now().timestamp()
        while timestamp + 5 > datetime.datetime.now().timestamp() and self.has(name + '_lock'):
            # 锁定中，等待
            time.sleep(200)

        try:
            await self.set(name + '_lock', True)
            await self.set(name, value, expire)
            await self.delete(name + '_lock')
        except Exception:
            await self.delete(name + '_lock')
            raise

        return True

    def tag(self, name: str or list) -> TagSet:
        """
        缓存标签
        :param name: 标签名(字符串，或列表)
        :return:
        """

        name_arr: list = [name] if isinstance(name, str) else name
        key = '-'.join(name_arr)
        if key not in self.tags:
            self.tags[key] = TagSet(name_arr, self)

        return self.tags[key]

    async def get_tag_items(self, tag: str) -> list:
        """
        获取标签包含的缓存标识
        :param tag: 标签名
        :return:
        """
        name = self.get_tag_key(tag)
        return await self.get(name, [])

    def get_tag_key(self, tag: str) -> str:
        """
        获取实际标签名
        :param tag: 标签名
        :return:
        """
        return self.options['tag_prefix'] + hashlib.md5(tag.encode('utf-8')).hexdigest()

    async def get_multiple(self, keys: list, default=None) -> dict:
        """
        批量读取缓存
        :param keys: 多个key(多个不重复的key,所以用集合)
        :param default: 默认值
        :return: 多个key value，返回一个字典
        """
        result = {}

        for key in keys:
            result[key] = await self.get(key, default)

        return result

    async def set_multiple(self, values: dict, expire: int = None) -> bool:
        """
        批量设置缓存
        :param values: 缓存数据(多个key value，所以用字典)
        :param expire:
        :return:
        """
        for key in values:
            result = await self.set(key, values[key], expire)
            if result is False:
                return False

        return True

    async def delete_multiple(self, keys: list) -> bool:
        """
        批量删除缓存
        :param keys: 多个key
        :return:
        """
        # 先去重
        sets = builtins.set(keys)
        for key in sets:
            result = self.delete(key)
            if result is False:
                return False

        return True

    async def lock(self, name: str):
        """
        装饰器锁(自动上锁解锁)
        :param name: 锁标识
        :return:
        """
        async def decorate(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if await self.locked(name) is True:
                    # 捕获异常
                    try:
                        # 执行函数
                        result = func(*args, **kwargs)
                        # 解锁
                        await self.unlock(name)
                        return result
                    except Exception:
                        # 解锁
                        await self.unlock(name)
                        # 重新抛出异常
                        raise
                else:
                    return None

            return wrapper

        return decorate
