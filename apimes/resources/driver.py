import abc

class Driver(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def subscribe(self, topic, q_name):
        return

    @abc.abstractmethod
    def unsubscribe(self, topic, q_name):
        return

    @abc.abstractmethod
    def publish(self, topic, data):
        return

    @abc.abstractmethod
    def get_message(self, topic, q_name):
        return
