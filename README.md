# Apimes

This is a simple RestAPI application used to create a Sub/Pub system.
Users can register to a topic and they receive all the messages sent to that
topic.

# Requirements
This version of the code is based on RabbitMQ server as backend.<br />
The code has been tested with [RabbitMQ 3.4.3](https://www.rabbitmq.com).
To install rabbitmq on a Debiain/Ubuntu box run:<br />
`sudo apt-get install rabbitmq-server`

# Installation and tests
We recommend to use virtualenv to install and test apimes.<br />
Below we report a step by step installation process, please note we consider
that the rabbitmq server is already installed on the machine.
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
