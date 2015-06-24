from ConfigParser import SafeConfigParser
from functools import wraps
from re import search
from socket import error as conn_error

from stevedore import driver

from apimes import exceptions
from amqp.exceptions import ChannelError

def can_raise_amqp_error(func):
    @wraps(func)
    def manage_exception(self, topic, q_name):
        try:
            return func(self, topic, q_name)
        except ChannelError as channel_ex:
            #log error
            return exceptions.InvalidSubscription()
        except conn_error:
            return 500

    return manage_exception

def is_valid_name(name):
    """
    We allow just digit, letters, hyphen, undrescore, period, colon for
    max lenght of 256.
    """
    pattern = "^[\.\w:-]{1,255}$"
    if search(pattern, name):
        return True
    else:
        #because the name of the method we want to return a bool value
        return False

def get_queue_name(topic, username):
    """
    Generates the queue name.
    """
    queue_name = username + '_'  + topic
    if is_valid_name(queue_name):
        return queue_name

def get_config_section(section, key):
    config = SafeConfigParser()
    config.read("apimes.conf")
    return config.get(section, key)

def get_driver():
    """
    Load the backend driver according to the value specified in the
    configuration file
    """
    driver_name = get_config_section('default', 'driver')
    mgr = driver.DriverManager(
                namespace='apimes.plugin',
                name=driver_name,
                invoke_on_load=True,
              )
    return mgr.driver

def server_error():
    return "Sorry the server can't perform your request", 500


