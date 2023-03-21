from setuptools import setup, find_packages

setup(
    name='Chatbot',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run = index:run_app',
            'test = index:test_app',
        ]
    }
)