class Singleton(object):
    """
    单例模式，任何类继承此类即可实现单例
    """
    __object = None

    def __new__(cls):
        if cls.__object is None:
            cls.__object = object.__new__(cls)
        return cls.__object


