import os
from setuptools import setup, find_packages

version = '0.0.3'


def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-zap',
    version=version,
    description='Automate the destruction and re-creation of django databases',
    long_description=fread('README.rst') + '\n\n' + fread('CHANGES.rst'),
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
    packages=find_packages(),
    keywords='django isotoma zap',
    author='Alex Holmes',
    author_email='alex.holmes@isotoma.com',
    license='Apache Software License',
    url='https://www.isotoma.com/open-source/',
    install_requires=[
        'setuptools',
        'Django',
    ],
    zip_safe=False,
    include_package_data=True,
)
