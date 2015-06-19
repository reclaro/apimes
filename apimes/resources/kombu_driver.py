from ConfigParser import SafeConfigParser
from kombu import Connection, Exchange, Queue, Producer

from apimes import utils
from apimes.resources.driver import Driver


class Kombu_driver(Driver):

    def __init__(self):
        config = SafeConfigParser()
        config.read("apimes.conf")
        self.host = config.get('rabbit', 'rabbit_host')
        self.user = config.get('rabbit', 'rabbit_user')
        self.pwd = config.get('rabbit', 'rabbit_password')
        self.port = config.get('rabbit', 'rabbit_port')

    def get_connection(self):
        conn = Connection('amqp://%s:%s@%s:%s//' % (self.user,
                                                 self.pwd,
                                                 self.host,
                                                 self.port))
        return conn

    def get_bound_exchange(self, channel, topic, exchange_type):
        exchange = Exchange(topic, exchange_type)
        return exchange(channel)

    def get_bound_queue(self, channel, q_name, exchange):
        # the queue is bound to a fanout exchange
        # so the routing_key is ignored
        queue = Queue(q_name,
                      exchange=exchange,
                      routing_key=q_name,
                      auto_delete=False,
                      durable=False)
        bound_queue = queue(channel)
        return bound_queue

    def declare_exchange(self, channel, topic, ex_type='fanout'):
        exchange = self.get_bound_exchange(channel, topic, 'fanout')
        exchange.declare()
        return exchange

    def declare_queue(self, channel, q_name, exchange, passive=False):
        queue = self.get_bound_queue(channel, q_name, exchange)
        queue.queue_declare(passive=passive)
        return queue

    def get_queue_on_exchange(self, conn, topic, q_name, passive=False):
        channel = conn.channel()
        exchange = self.declare_exchange(channel, topic)
        user_queue = self.declare_queue(channel,
                                        q_name,
                                        exchange,
                                        passive=passive)
        return user_queue

    def subscribe(self, topic, q_name):
        # Subscriber means create a queue bound to
        # a fanout exchange called like the topic name
       with self.get_connection() as conn:
            user_queue = self.get_queue_on_exchange(conn,
                                                    topic,
                                                    q_name)
            user_queue.queue_bind()

    @utils.can_raise_channel_error
    def unsubscribe(self, topic, q_name):
        with self.get_connection() as conn:
            channel = conn.channel()
            #TODO valutare se mettere anache per exchange la passive
            # se non c'e' evitiamo di crearlo e non puo' esserci la coda
            #NO se esiste il modo di cancellare l'exchange con auto_delete.
            #ocio che si deve cancellare lo exchange se e' stato creato
            #solo per questa coda che non esiste, dovrebbe fare il tutto
            #l'auto_delete
            user_queue = self.get_queue_on_exchange(conn,
                                                    topic,
                                                    q_name,
                                                    passive=True)
            user_queue.purge()
            user_queue.delete()

    def publish(self, topic, data):
        with self.get_connection() as conn:
            channel = conn.channel()
            exchange = self.declare_exchange(channel, topic, 'fanout')
            producer = Producer(channel, exchange=exchange, auto_declare=False)
            producer.publish(data)

    @utils.can_raise_channel_error
    def get_message(self, topic, q_name):
        with self.get_connection() as conn:
            user_queue = self.get_queue_on_exchange(conn,
                                                    topic,
                                                    q_name,
                                                    passive=True)
            msg = user_queue.get(no_ack=True)

            if not msg:
                return

            return msg.decode()
