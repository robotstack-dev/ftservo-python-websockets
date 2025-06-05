from setuptools import setup

setup(
    name='ftservo-python-websockets',
    version='0.0.3',
    packages=['scservo_sdk'],
    description='Python SDK for FT Servo with WebSocket support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Robotstack',
    author_email='nick@robotstack.com',
    url='https://github.com/robotstack-dev/ftservo-python-websockets',
    install_requires=['websockets>=9.0'],
    python_requires='>=3.7',
    license='Apache-2.0',
) 