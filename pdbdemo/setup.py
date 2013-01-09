from setuptools import setup, find_packages
import sys, os

install_requires = [
    "Django",
]


setup(name='pdbdemo',
      description="",
      keywords='',
      author='Nathan Yergler',
      author_email='nathan@yergler.net',
      packages=find_packages('.'),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
)
