from rongo.container import Container


class Facade(type):
    def __getattr__(self, attribute, *args, **kwargs):

        return getattr(Container.getInstance().make(self.key), attribute)
