from setuptools import setup, find_packages

import sdtg

setup(
    name='sdtg',
    version=sdtg.__version__,
    author='Vezono',
    author_email='gbball.baas@gmail.com',
    description='Second-dimensional Telegram Games library.',
    long_description='Second-dimensional Telegram Games library.',
    url='https://github.com/Vezono/sdtg-lib',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
