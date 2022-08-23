from rongo.container import Container


def app(name: str or object = None, *arguments):
    """
    快速获取容器中的实例
    :param name: 类或标识，不能传入实例。 默认获取当前应用实例
    :return:
    """
    instance = Container.getInstance()

    # 为空，则获取应用实例
    if not name:
        return instance.make('app', *arguments)
    # 传入一个key, 直接检索
    elif isinstance(name, str):
        return instance.make(name, *arguments)
    # 只能传入类，不能传入实例
    else:
        # 判断是否存在,如果存在，则去检索
        if instance.has(name) is True:
            return instance.make(name, *arguments)
        else:
            # 如果不存在，先解析，再绑定,再检索
            return instance.simple(instance.resolve(name, *arguments)).make(name, *arguments)


def bind(name: str, class_obj: object = None):
    """
    绑定一个类到容器
    :param name: 标识
    :param class_obj: 要绑定的类、实例、数据
    :return:
    """
    return Container.getInstance().bind(name, class_obj)
