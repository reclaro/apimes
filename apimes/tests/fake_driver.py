from apimes.resources.driver import Driver

class Fake_driver(Driver):
    def subscribe(self,topic, q_name):
        pass

    def unsubscribe(self, topic, q_name):
        pass

    def publish(self, topic, message):
        pass

    def get_message(self, topic, q_name):
        pass
