from setuptools import setup, find_packages

long_description="""A simple tool that converts bmpfiles to GDS Layouts"""

setup(
    name='bmpToGDS',
    version='0.0.1',
    description=long_description, 

    # Main homepage
    url="https://github.com/trezitorul/bmpToGDS",
    
    # Extra info and author details
    author='Trezitorul',

    keywords=['bmp', 'GDS', 'GDSPY', 'layout'],

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: MIT Software License',
        ],

    # package
    packages = ['bmpToGDS'],
    zip_safe = False,
)