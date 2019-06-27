from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name='fact_minimal',
    version=VERSION,
    packages=find_packages('fact'),
    package_dir={
        'fact': 'src'
    },
    description='Finite State fork of minimized FACT_core repo',
    author='Finite State',
    author_email='',
    url='',
    license='')
