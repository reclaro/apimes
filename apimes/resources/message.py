from flask import request
from flask_restful import Resource

from apimes.resources.kombu_driver import Kombu_driver

class Message(Resource):
    def __init__(self):
        self.driver = Kombu_driver()

    def post(self, topic):
        # this is quite general we expect the sender we put the data in the body
        # like binary data, if the data are passed with as form-data the message
        # will report details about the content-disposition
        #(TODO): insert validation for topic name just letter
        #TODO insert error handling, sugli specific su connection error e i possibile
        #errori sollevati dalla publish
        message = request.get_data()
        self.driver.publish(topic, message)
        return {'topic': topic, 'message': message}
