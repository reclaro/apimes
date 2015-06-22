from setuptools import setup, find_packages

setup(
        name='roz-apimes',
        version='1.0',
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            'apimes.plugin': [
                'amqp = apimes.resources.kombu_driver:Kombu_driver',
                'fake = apimes.tests.fake_driver:Fake_driver',
                ],

            },
        )
