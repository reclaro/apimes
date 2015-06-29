# Apimes

This is a simple RestAPI application used to create a Sub/Pub system.
Users can register to topics and they receive all the messages sent to them.
<br />
A message get delivered to a client when the client explicitly checks for new messages.
Every time a client checks for a new message just a new message is delivered, if
there are N message in order to get all the messages the user needs
to check N times for consuming all the messages.<br />
If a message is sent to a topic but there are no subscribers the message get
lost.<br />
A client gets the messages which are published after his registration.<br />
Messages survive to a server restart and they get deleted once all the
subscribers have consumed them.<br />
A topic is created in two ways:

1. A user subscribe to the topic, if the topic doesn't exist it will be created.
2. A message is sent to a topic, please note that in this case if the topic
   doesn't exist it will be created but the message will get lost as there won't
   be any subscribers

If a user tries to get messages from a topic when he has not a valid
subscription the application will return an error code.
# Requirements
This version of the code is based on RabbitMQ server as backend.<br />
The code has been tested with [RabbitMQ 3.4.3](https://www.rabbitmq.com).
To install rabbitmq on a Debiain/Ubuntu box run:<br />
`sudo apt-get install rabbitmq-server`

# Installation and tests
We recommend to use virtualenv to install and test apimes.<br />
Below we report a step by step installation process, please note we consider
that the **rabbitmq server is already installed on the machine.**


1. Creation of a virtual env using [virtualevwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):<br />
`mkvirtualenv apimes`
2. Clone the repository:<br />
`git clone https://github.com/reclaro/apimes.git`
3. Installation of the python code:<br />
`cd apimes`<br />
`python setup.py install`
4. Run the API:
`python apimes/api.py`<br />
**NOTE the application will run on a webserver which is not suitable for a
production environment, it is good for testing the code.**
5. Run the tests:
The tests include unit and functional tests, to get the functional tests working
rabbitmq server must run, please start it with <br /> `sudo service rabbtimq-server
start`<br />
`py.test apimes/`
