from rongo.container import Container


def app(name: str = '', *arguments):
    """
    快速获取容器中的实例
    :param name: 类名或标识 默认获取当前应用实例
    :return:
    """
    return Container.getInstance().make(name, *arguments)


def bind(name: str = '', class_obj: object = None):
    """
    绑定一个类到容器
    :param name: 类名或标识
    :param class_obj: 要绑定的类或实例
    :return:
    """
    return Container.getInstance().bind(name, class_obj)
