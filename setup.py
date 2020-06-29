from setuptools import setup, find_packages
from os.path import join, dirname
import sdtg

setup(
    name='sdtg-lib',
    version=sdtg.__version__,
    author='Vezono2',
    author_email='gbball.baas@yandex.ru',
    description='Second-dimensional Telegram Games library.',
    long_description=open(join(dirname(__file__), 'README.md'), encoding='utf-8').read(),
    url='https://github.com/Vezono2/sdtg-lib',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
