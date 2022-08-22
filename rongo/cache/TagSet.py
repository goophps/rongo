from ..cache import Cache


class TagSet:
    """
    标签集合
    """

    def __init__(self, tag: list, cache: Cache):
        """
        初始化
        :param tag: 缓存标签
        :param cache: 缓存对象实例
        """
        self.tag = tag
        self.driver = cache

    async def set(self, name, value, expire: int = None) -> bool:
        """
        写入缓存
        :param name: 缓存的key
        :param value: 存储的数据
        :param expire: 过期时间
        :return:
        """
        await self.driver.set(name, value, expire)
        await self.append(name)
        return True

    async def append(self, name: str) -> None:
        """
        追加缓存标识到标签
        :param name: 缓存的key
        :return:
        """
        name = self.driver.get_cache_key(name)
        for tag in self.tag:
            key = self.driver.get_tag_key(tag)
            await self.driver.append(key, name)

    async def add(self, name: str, value, expire: int = None):
        """
        如果不存在则写入缓存
        :param name: 缓存的key
        :param value: 存储的数据
        :param expire: 过期时间
        :return:
        """
        result = self.driver.add(name, value, expire)
        await self.append(name)
        return result

    async def clear(self) -> bool:
        """
        清除tag标签的缓存数据
        :return:
        """
        for tag in self.tag:
            # 获取这个标签包含的缓存key
            names = await self.driver.get_tag_items(tag)
            # 把缓存标签里的值当作key, 去把对应的缓存删除
            await self.driver.clear_tag(names)

            # 把标签删除
            key = self.driver.get_tag_key(tag)
            await self.driver.delete(key)

        return True
