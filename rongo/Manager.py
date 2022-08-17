import json
import importlib


class Manager:
    """
    驱动创建者
    """

    def __init__(self, config: dict = None):
        # 所有已实现的可用驱动，也就是子类实例
        self.drivers: dict = {}
        # 整个配置文件
        self.config: dict = config

    def get_options(self, name: str) -> dict:
        """
        获取当前实例需要的具体配置
        :param name: 配置类型名
        :return:
        """
        if name is None or name == "default":
            name = self.config.get("default")

        return self.config.get('stores').get(name)

    def driver(self, name: str = 'default'):
        """
        获取具体驱动的实例，如果不存在，会自动创建。
        :param name:
        :return:
        """
        if name not in self.drivers.keys():
            self.drivers.update({name: self.create_driver(name)})

        return self.drivers[name]

    def create_driver(self, name: str):
        """
        创建驱动(通过反射，创建具体实例)
        :param name: 驱动类型
        :return:
        """
        class_path = self.resolve_class(name)
        class_index = class_path.rfind('.')
        # 用反射实例化对象
        m = importlib.import_module(class_path)
        class_name = getattr(m, class_path[class_index + 1:])
        # 创建对象
        obj = class_name(**self.init_parameter(name))
        obj.config = self.config
        return obj

    def init_parameter(self, name: str):
        """
        构造函数需要传入的参数
        :return:
        """
        return {'options': self.get_options(name)}

    def resolve_class(self, name: str) -> str:
        """
        当前驱动类型名
        :param name: 驱动类型名
        :return:
        """
        # 必须配置backend参数
        backend = self.get_options(name).get('backend')
        if backend is None:
            raise ValueError("please configure: backend")

        # todo 判断驱动是否存在

        # 必须包含点
        if '.' in backend:
            return backend
        else:
            raise ValueError("Driver [%s] not supported." % backend)

    @staticmethod
    def serialize(value):
        if isinstance(value, (str, int, float)):
            return value
        try:
            return json.dumps(value)
        except json.decoder.JSONDecodeError:
            return value

    @staticmethod
    def un_serialize(value):
        if isinstance(value, (str, int, float)):
            return value

        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value
