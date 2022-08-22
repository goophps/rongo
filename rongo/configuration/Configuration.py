from ..facades import Loader
from ..utils.structures import data
from ..exceptions import InvalidConfigurationLocation, InvalidConfigurationSetup


class Configuration:
    # Foundation configuration keys
    reserved_keys = [
        "application",
        "auth",
        "broadcast",
        "cache",
        "database",
        "filesystem",
        "mail",
        "notification",
        "providers",
        "queue",
        "session",
    ]

    def __init__(self, application):
        self.application = application
        self._config: dict = data()

    def load(self):
        """At boot load configuration from all files and store them in here."""
        config_root = self.application.make("config.location")
        for module_name, module in Loader.get_modules(
                config_root, raise_exception=True
        ).items():
            params = Loader.get_parameters(module)
            for name, value in params.items():
                self._config[module_name] = {name.lower(): value}

        # check loaded configuration
        if not self._config.get("application"):
            raise InvalidConfigurationLocation(
                f"Config directory {config_root} does not contain required configuration files."
            )

    def merge_with(self, path, external_config):
        """Merge external config at key with project config at same key. It's especially
        useful in Masonite packages in order to merge the configuration default package with
        the package configuration which can be published in project.

        This functions disallow merging configuration using foundation configuration keys
        (such as 'application').
        """
        if path in self.reserved_keys:
            raise InvalidConfigurationSetup(
                f"{path} is a reserved configuration key name. Please use an other key."
            )
        if isinstance(external_config, str):
            # config is a path and should be loaded
            params = Loader.get_parameters(external_config)
        else:
            params = external_config
        base_config = {name.lower(): value for name, value in params.items()}
        merged_config = {**base_config, **self.get(path, {})}
        self.set(path, merged_config)

    def set(self, path, value):
        self._config[path] = value

    def has(self, path: str) -> bool:
        if ('.' not in path) and (path.lower() not in self._config.keys()):
            return False

        if self.get(path):
            return True
        else:
            return False

    def all(self):
        return self._config

    def get(self, path: str = None, default=None):
        # 无参时，获取所有
        if not path:
            return self._config

        # 不包含一点，直接下标返回
        if '.' not in path:
            return self._config[path.lower()]

        names: list = path.split('.')
        names[0] = names[0].lower()
        config: dict = self._config

        # 按.拆分成多维数组进行判断
        for value in names:
            if value in config.keys():
                config = config[value]
            else:
                return default

        return config
