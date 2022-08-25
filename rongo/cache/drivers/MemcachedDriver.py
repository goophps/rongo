from ..Cache import Cache
from pymemcache.client.base import Client


class MemcachedDriver(Cache):
    """
    redis驱动
    """

    # 类属性。 所有实例共享
    options = {
        'host': '127.0.0.1',
        'port': 6379,
        'timeout': 10,
        'expire': 0,
        'prefix': '',
        'tag_prefix': 'tag:',
    }

    def __init__(self, options: dict):
        self.options.update(options)
        super().__init__(self.options)
        self.handler = Client(f"{self.options['host']}:{self.options['port']}", timeout=self.options['timeout'],
                              connect_timeout=self.options['timeout'])

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
        return False if name is None else bool(self.handler.get(self.get_cache_key(name)))

    async def get(self, name: str, default=None):
        """
        读取缓存
        :param name: 缓存key
        :param default: 默认值(无值时)
        :return:
        """
        value = self.handler.get(self.get_cache_key(name), default)
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

        result = self.handler.set(key, value, expire)

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
        return self.handler.incr(self.get_cache_key(name), step)

    async def decrement(self, name: str, step: int = 1) -> int:
        """
        自减(针对数值缓存)
        :param name: 缓存key
        :param step: 步长
        :return: 一个新值
        """
        return self.handler.decr(self.get_cache_key(name), step)

    async def delete(self, name: str) -> bool:
        """
        删除缓存
        :param name:
        :return:
        """
        return self.handler.delete(self.get_cache_key(name))

    async def clear(self) -> bool:
        """
        清除缓存(清除当前数据库)
        :return:
        """
        return self.handler.flush_all()

    async def clear_tag(self, keys: list) -> bool:
        """
        删除缓存标签
        :param keys: 缓存标识列表
        :return:
        """
        return self.handler.delete_many(keys)

    async def locked(self, name: str) -> bool:
        """
        上锁
        :param name: 锁标识
        :return:
        """
        key = self.get_cache_key(name)
        return bool(self.handler.add(key, 1))

    async def unlock(self, name: str) -> bool:
        """
        解锁
        :param name: 锁标识
        :return:
        """
        return await self.delete(name)

    async def get_multiple(self, keys: list, default=None) -> dict:
        # 每个key进行处理
        key_map = {
            self.get_cache_key(key): key for key in keys
        }
        result: dict = self.handler.get_many(key_map.keys())
        # 反处理回用户的key，加上数据，以键值对方式返回
        return {self.resolve_cache_key(k): (self.un_serialize(v) if v else default) for k, v in result.items()}

    async def set_multiple(self, values: dict, expire: int = None) -> bool:
        # 设置多值
        result = self.handler.set_many(
            {self.get_cache_key(key): self.serialize(value) for key, value in values.items()}, expire)
        return result

    async def delete_multiple(self, keys: list) -> bool:
        # 每个key进行处理
        key_map = {
            self.get_cache_key(key): key for key in keys
        }
        return self.handler.delete_many(key_map.keys())
