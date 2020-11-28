#!/usr/bin/env python
# Source: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-setup-script
# Via: https://www.samueldowling.com/2020/06/08/how-to-set-up-a-python-project-and-development-environment/  # noqa
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='Egg_Bot_Preocts',
    version='0.0.3',
    license='GNU General Public License',
    description='A module based Discord bot written in Python',
    author='Preocts',
    author_email='preocts@preocts.com',
    url='https://github.com/Preocts/Egg_Bot',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'discord.py>=1.5.1',
        'python-dotenv>=0.15.0'
    ],
    entry_points={
        'console_scripts': [
            'start-eggbot = eggbot.eggbot_core:main',
        ]
    },
    include_package_data=True
)
