import logging
from ConfigParser import SafeConfigParser
from kombu import Connection, Exchange, Queue, Producer

from apimes import utils
from apimes.resources.driver import Driver


LOG = logging.getLogger(__name__)


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
        exchange = Exchange(topic,
                            exchange_type,
                            durable=True,
                            delivery_mode='persistent',
                            auto_delete=True)
        return exchange(channel)

    def get_bound_queue(self, channel, q_name, exchange):
        # the queue is bound to a fanout exchange
        # so the routing_key is ignored
        queue = Queue(q_name,
                      exchange=exchange,
                      routing_key=q_name,
                      auto_delete=False,
                      durable=True)
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

    @utils.can_raise_amqp_error
    def subscribe(self, topic, q_name):
        # Subscriber means create a queue bound to
        # a fanout exchange called like the topic name
        LOG.debug("Subscribe to topic %s and Q %s" % (topic, q_name))
        with self.get_connection() as conn:
            user_queue = self.get_queue_on_exchange(conn,
                                                    topic,
                                                    q_name)
            user_queue.queue_bind()

    @utils.can_raise_amqp_error
    def unsubscribe(self, topic, q_name):
        LOG.debug("Unsubscribe from Q %s" % q_name)
        with self.get_connection() as conn:
            user_queue = self.get_queue_on_exchange(conn,
                                                    topic,
                                                    q_name,
                                                    passive=True)
            user_queue.purge()
            user_queue.delete()

    @utils.can_raise_amqp_error
    def publish(self, topic, data):
        LOG.debug("Publishing message on topic %s" % topic)
        with self.get_connection() as conn:
            channel = conn.channel()
            exchange = self.declare_exchange(channel, topic, 'fanout')
            producer = Producer(channel, exchange=exchange, auto_declare=False)
            producer.publish(data)

    @utils.can_raise_amqp_error
    def get_message(self, topic, q_name):
        LOG.debug("Get message from the Q %s" % q_name)
        with self.get_connection() as conn:
            user_queue = self.get_queue_on_exchange(conn,
                                                    topic,
                                                    q_name,
                                                    passive=True)
            msg = user_queue.get(no_ack=True)

            if not msg:
                LOG.debug("No messages found in %s" % q_name)
                return

            return msg.decode()
