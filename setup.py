from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

def get_version():
    with open('line.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

setup(
    name='line-counter',
    version=get_version(),
    description='A command line tool to analyze the amount of lines and files under current directory.',
    long_description=read_md('README.md'),
    url='https://github.com/MorganZhang100/line-counter',
    author='Morgan Zhang',
    author_email='MorganZhang100@gmail.com',
    license='MIT',
    py_modules=['line'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='file line code count',
    entry_points={
        'console_scripts': [
            'line=line:_main',
        ],
    },
)