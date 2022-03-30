from setuptools import setup, find_packages

setup(
    name='Quirks',
    # version='0.1.0',
    description='Setting up Package for Which Looks for Quirky Data and transform it accordingly.',
    author='Suprabhat Sinha',
    author_email='superbhat.sinha@gmail.com',
    # url='', provide git hub url..
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'pandas',
        'fastparquet'
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['transform=src.main:main']
    }
)