from io import open
from setuptools import setup

version = '0.1.1'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='etudatasphere',
    version=version,

    author='sesh00',
    author_email='ernestrsage@gmail.com',

    description=(
        u'etudatasphere: Simplifying Cloud Administration. Access Yandex.Cloud services with ease, automating routine '
        u'tasks for resource management.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/sesh00/etudatasphere',
    download_url='https://github.com/sesh00/etudatasphere/archive/main.zip'.format(
        version
    ),

    license='MIT License, see LICENSE file',

    packages=['etudatasphere'],
    install_requires=['requests'],

    extras_require={
            'dev': [
                'pytest',
            ]
        },

    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
