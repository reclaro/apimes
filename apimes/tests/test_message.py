from contextlib import nested

from flask.ext.testing import TestCase
from flask import Flask
import mock
import pytest

from apimes import utils
from apimes.resources.message import Message



class TestMessage(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_message_post_with_server_error(self):
         with nested(mock.patch('apimes.utils.get_config_section'),
                     mock.patch('apimes.tests.fake_driver.Fake_driver')) as \
                 (mock_driver, mock_fake_driver):
            mock_driver.return_value = 'fake'       
            _driver = mock_fake_driver.return_value 
            _driver.publish.return_value = 500 
            msg = Message()
            resp = msg.post('test')
            assert resp == utils.server_error()

