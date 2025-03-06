from setuptools import setup, find_packages

setup(
    name='explicit_util',
    version='0.1',
    packages=['explicit_util'],
    install_requires=[
        'tqdm',
        'namer',
    ],
    author='Alchemist-Aloha',
    description='A utility library for managing media files',
    url='https://github.com/Alchemist-Aloha/lust_util',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Windows',
    ],
)
