from setuptools import setup

setup(
    name='ftservo_python_websockets',
    version='0.0.2',
    packages=['scservo_sdk'],
    description='Python SDK for FT Servo with WebSocket support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nicholas Stedman',
    author_email='nickstedman@gmail.com',
    url='https://github.com/nsted/FTServo_Python_Websockets',
    install_requires=['websockets>=9.0'],
    python_requires='>=3.7',
    license='Apache-2.0',
) 