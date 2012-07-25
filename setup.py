"""

    Declare a Python package sevabot

    See

    * http://wiki.python.org/moin/Distutils/Tutorial

    * http://packages.python.org/distribute/setuptools.html#developer-s-

    * http://plone.org/products/plone/roadmap/247

"""

from setuptools import setup

README = open("README.rst", "rt").read() + "\n" + open("CHANGES.rst", "rt").read()

setup(name = "sevabot",
    version = "0.1",
    description = "Generic purpose Skype bot",
    long_description = README,
    author = "Pete Sevander, Mikko Ohtamaa",
    author_email = "",
    url = "https://github.com/sevanteri/sevabot",
    install_requires = ["Flask"],
    packages = ['sevabot'],
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    license="GPL2",
    include_package_data = True,
    entry_points="""
      """,
)