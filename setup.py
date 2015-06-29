from setuptools import setup, find_packages

setup(
        name='roz-apimes',
        version='1.0',
        description='Simple API messaging system',
        author='Andrea Rosa',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'Flask-RESTful',
            'Flask-Testing',
            'flask',
            'kombu',
            'requests',
            'stevedore',
            'pytest',
            'mock'
            ],
        entry_points={
            'apimes.plugin': [
                'amqp = apimes.resources.kombu_driver:Kombu_driver',
                'fake = apimes.tests.fake_driver:Fake_driver',
                ],

            },
        )
