from ..Cache import Cache
from redis import asyncio as aredis
import redis


class RedisDriver(Cache):
    """
    redis驱动
    """

    # 类属性。 所有实例共享
    options = {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 0,
        'timeout': 10,
        'expire': 0,
        'prefix': '',
        'tag_prefix': 'tag:',
    }

    def __init__(self, options: dict):
        self.options.update(options)
        super().__init__(self.options)
        self.handler = aredis.Redis(host=self.options['host'], port=self.options['port'], db=self.options['db'],
                                    password=self.options['password'], socket_timeout=self.options['timeout'],
                                    socket_connect_timeout=self.options['timeout'])

    def handler(self):
        """
        获取缓存句柄
        :return:
        """
        return self.handler

    async def has(self, name: str) -> bool:
        """
        判断缓存
        :param name: 缓存key
        :return:
        """
        return await self.handler.exists(self.get_cache_key(name)) if True else False

    async def get(self, name: str, default=None):
        """
        读取缓存
        :param name: 缓存key
        :param default: 默认值(无值时)
        :return:
        """
        value = await self.handler.get(self.get_cache_key(name))
        if not value:
            return default

        return self.un_serialize(value)

    async def set(self, name: str, value, expire: int = None) -> bool:
        """
        设置缓存
        :param name: 缓存key
        :param value: 值
        :param expire: 过期时间(秒)
        :return:
        """
        key = self.get_cache_key(name)
        expire = self.get_expire_time(expire)
        value = self.serialize(value)

        if expire > 0:
            result = await self.handler.setex(key, expire, value)
        elif expire == 0:
            result = await self.handler.set(key, value)
        else:
            # 时间小于零，则删除缓存
            result = await self.handler.delete(key) > 0
        if result is True:
            return True
        else:
            return False

    async def increment(self, name: str, step: int = 1) -> int:
        """
        自增(针对数值缓存)
        :param name: 缓存key
        :param step: 步长
        :return: 一个新值
        """
        return await self.handler.incrby(self.get_cache_key(name), step) > 0

    async def decrement(self, name: str, step: int = 1) -> int:
        """
        自减(针对数值缓存)
        :param name: 缓存key
        :param step: 步长
        :return: 一个新值
        """
        return await self.handler.decrby(self.get_cache_key(name), step) > 0

    async def delete(self, name: str) -> bool:
        """
        删除缓存
        :param name:
        :return:
        """
        return await self.handler.delete(self.get_cache_key(name)) > 0

    async def clear(self) -> bool:
        """
        清除缓存(清除当前数据库)
        :return:
        """
        return await self.handler.flushdb()

    async def clear_tag(self, keys: list) -> bool:
        """
        删除缓存标签
        :param keys: 缓存标识列表
        :return:
        """
        return await self.handler.delete(*keys) > 0

    async def append(self, name: str, value) -> bool:
        """
        追加TagSet数据
        :param name: 缓存标识
        :param value: 数据
        :return:
        """
        key = self.get_cache_key(name)
        return await self.handler.sadd(key, value) > 0

    async def get_tag_items(self, tag: str) -> list:
        """
        获取这个缓存标签包含的缓存key
        :param tag: 缓存标签
        :return:
        """
        name = self.get_tag_key(tag)
        key = self.get_cache_key(name)
        return await self.handler.smembers(key)

    async def locked(self, name: str) -> bool:
        """
        上锁
        :param name: 锁标识
        :return:
        """
        key = self.get_cache_key(name)
        return await self.handler.setnx(key, 1)

    async def unlock(self, name: str) -> bool:
        """
        解锁
        :param name: 锁标识
        :return:
        """
        key = self.get_cache_key(name)
        return await self.delete(key)
