from setuptools import setup, find_packages

import sdtg

setup(
    name='sdtg',
    version=sdtg.__version__,
    author='Vezono2',
    author_email='gbball.baas@yandex.ru',
    description='Second-dimensional Telegram Games library.',
    long_description='Second-dimensional Telegram Games library.',
    url='https://github.com/Vezono2/sdtg-lib',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
