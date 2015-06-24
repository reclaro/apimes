from flask.ext.testing import TestCase
from flask import Flask
import mock
import pytest

from apimes import exceptions
from apimes import utils
from apimes.resources.subscription import Subscription


class TestSubscription(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def set_server_error(self, mock_fake):
        _driver = mock_fake.return_value
        _driver.subscribe.return_value = 500
        _driver.unsubscribe.return_value = 500
        _driver.get_message.return_value = 500

    def set_invalid_subscritpion(self, mock_fake):
        _driver = mock_fake.return_value
        _driver.unsubscribe.return_value = exceptions.InvalidSubscription()
        _driver.get_message.return_value = exceptions.InvalidSubscription()

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_post_no_error(self, mock_driver):
        subs = Subscription()
        expected = "Subscription succeeded"
        resp = subs.post('topic', 'user')
        assert resp == expected

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_post_server_error(self, mock_driver):
        with mock.patch('apimes.tests.fake_driver.Fake_driver') as mock_fake:
            self.set_server_error(mock_fake)
            subs = Subscription()
            expected = utils.server_error()
            resp = subs.post('topic', 'user')
            assert resp == expected

    def test_post_invalid_q_name(self):
        topic = 'a' * 256
        subs = Subscription()
        resp = subs.post(topic, 'user')
        assert isinstance(resp, tuple)
        assert resp[1] == 400

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_delete(self, mock_driver):
        subs = Subscription()
        expected = None
        resp = subs.delete('topic', 'name')
        assert resp == expected

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_delete_unknow_subscription(self, mock_driver):
        with mock.patch('apimes.tests.fake_driver.Fake_driver') as mock_fake:
            self.set_invalid_subscritpion(mock_fake)
            subs = Subscription()
            resp = subs.delete('topic', 'name')
            assert isinstance(resp, tuple)
            assert resp[1] == 404

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_delete_server_error(self, mock_driver):
        with mock.patch('apimes.tests.fake_driver.Fake_driver') as mock_fake:
            self.set_server_error(mock_fake)
            subs = Subscription()
            expected = utils.server_error()
            resp = subs.delete('topic', 'name')
            assert resp == expected

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_get_message(self, mock_driver):
        expected = 'This is a message'
        with mock.patch('apimes.tests.fake_driver.Fake_driver') as mock_fake:
            _driver = mock_fake.return_value
            _driver.get_message.return_value = expected
            subs = Subscription()
            resp = subs.get('topic', 'user')
            assert resp == expected

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_no_message(self, mock_driver):
        subs = Subscription()
        resp = subs.get('topic', 'user')
        assert isinstance(resp, tuple)
        assert resp[1] == 204

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_get_message_server_error(self, mock_driver):
        with mock.patch('apimes.tests.fake_driver.Fake_driver') as mock_fake:
            self.set_server_error(mock_fake)
            subs = Subscription()
            expected = utils.server_error()
            resp = subs.get('topic', 'user')
            assert resp == expected

    @mock.patch('apimes.utils.get_config_section', return_value='fake')
    def test_get_message_unknow_subscription(self, mock_driver):
        with mock.patch('apimes.tests.fake_driver.Fake_driver') as mock_fake:
            self.set_invalid_subscritpion(mock_fake)
            subs = Subscription()
            resp = subs.get('topic', 'name')
            assert isinstance(resp, tuple)
            assert resp[1] == 404
