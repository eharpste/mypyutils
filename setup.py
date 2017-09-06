from setuptools import setup, find_packages
setup(
    name="mypyutils",
    version="0.1",
    packages=find_packages(),

    install_requires=['concept-formation>=0.3.2'],

    author='Erik Harpstead',
    author_email='eharpste@cs.cmu.edu',
    description='This is a collection of utilities scripts I have written for myself over the years',
    license='LICENSE.txt',
    url='https://github.com/eharpste/mypyutils'
)