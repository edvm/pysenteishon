import abc


class PysenteishonPlugin(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self):
        """Pysenteishon will execute this method when running your
        plugin."""