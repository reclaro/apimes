from urlparse import urljoin

import pytest
from requests import delete
from requests import get
from requests import post

from apimes import utils


class TestApimes(object):

    def get_endpoint(self):
        return utils.get_config_section('default', 'endpoint')

    def subscribe(self, topic, user):
        resource = '/'.join((topic, user))
        url = urljoin(self.get_endpoint(), resource)
        res = post(url)
        return res

    def unsubscribe(self, topic, user):
        resource = '/'.join((topic, user))
        url = urljoin(self.get_endpoint(), resource)
        res = delete(url)
        return res

    def send_message(self, topic, msg):
        url = urljoin(self.get_endpoint(), topic)
        res = post(url, data=msg)
        return res

    def get_message(self, topic, user):
        resource = '/'.join((topic, user))
        url = urljoin(self.get_endpoint(), resource)
        res = get(url)
        return res

    def test_post_and_get_message(self):
        topic = 'topic'
        user = 'user1'
        msg = "Hello world" # of course!
        res = self.subscribe(topic, user)
        assert res.status_code == 200

        res = self.send_message(topic, msg)
        assert res.status_code == 200

        res = self.get_message(topic, user)
        assert res.status_code == 200
        assert res.json() == msg

        # try to get a new message, but there are no messages left
        res = self.get_message(topic, user)
        assert res.status_code == 204

        #unsubscribe user
        res = self.unsubscribe(topic, user)
        assert res.status_code == 200

    def test_post_get_message_multiple_users(self):
        topic = 'topic'
        user = 'user1'
        user2 = 'user2'
        msg = "Hello world" # of course!

        #subscribe user1
        res = self.subscribe(topic, user)
        assert res.status_code == 200

        #subscribe user2
        res = self.subscribe(topic, user2)
        assert res.status_code == 200

        res = self.send_message(topic, msg)
        assert res.status_code == 200

        res = self.get_message(topic, user)
        assert res.status_code == 200
        assert res.json() == msg

        # try to get a new message, but there are no messages left
        res = self.get_message(topic, user2)
        assert res.status_code == 200
        assert res.json() == msg

        #unsubscribe user
        res = self.unsubscribe(topic, user)
        assert res.status_code == 200

        #unsubscribe user
        res = self.unsubscribe(topic, user2)
        assert res.status_code == 200

    def test_user_subscribe_late_no_message(self):
        topic = 'topic'
        user = 'user1'
        msg = "Hello world" # of course!
        res = self.subscribe(topic, user)
        assert res.status_code == 200

        res = self.send_message(topic, msg)
        assert res.status_code == 200

        res = self.get_message(topic, user)
        assert res.status_code == 200
        assert res.json() == msg

        #unsubscribe user2 to be sure that the queue is not there
        user2 = 'user2'
        self.unsubscribe(topic, user2)

        #subscribe user2
        res = self.subscribe(topic, user2)
        assert res.status_code == 200

        res = self.get_message(topic, user2)
        assert res.status_code == 204

        #unsubscribe user
        res = self.unsubscribe(topic, user)
        assert res.status_code == 200
        #unsubscribe user2
        res = self.unsubscribe(topic, user2)
        assert res.status_code == 200

    def test_subscription_does_not_exist(self):
        topic = 'topic'
        user = 'user1'
        res = self.get_message(topic, user)
        assert res.status_code == 404
