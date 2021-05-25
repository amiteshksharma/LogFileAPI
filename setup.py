# setup.py
from setuptools import setup, find_packages

requires = [
    'tornado',
    'requests',
]

setup(
    name='tornado_todo',
    version='0.0',
    description='Log File loader',
    author='Amitesh Sharma',
    author_email='amsharma@scripps.edu',
    keywords='web tornado',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'serve_app = server:main',
        ],
    },
)