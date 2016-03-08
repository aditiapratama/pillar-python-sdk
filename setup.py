# -*- coding: utf-8 -*-
from setuptools import setup

long_description = """
The Pillar REST SDK provides Python APIs to communicate to the Pillar webservices.
"""

setup(
    name='pillar-sdk',
    version='0.0.1',
    author='Francesco Siddi, PayPal',
    author_email='francesco@blender.org',
    packages=['pillarsdk'],
    scripts=[],
    url='https://github.com/armadillica/Pillar-Python-SDK',
    license='BSD License',
    description='The Pillar REST SDK provides Python APIs to communicate to the Pillar webservices.',
    long_description=long_description,
    install_requires=['requests>=1.0.0', 'six>=1.0.0', 'pyopenssl>=0.14'],
    test_requires=['tox', 'coverage', 'pytest', 'pytest-xdist', 'pytest-cov'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=['pillar', 'rest', 'sdk', 'tracking', 'film', 'production']
)
