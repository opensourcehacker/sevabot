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
    version = "1.0",
    description = "A Skype bot supporting integration with external services",
    long_description = README,
    author = "Mikko Ohtamaa",
    author_email = "mikko@opensourcehacker.com",
    url = "https://github.com/opensourcehacker/sevabot",
    install_requires = ["Flask", "Skype4Py", "plac"],
    packages = ['sevabot'],
    classifiers=[
        "Programming Language :: Python",
    ],
    license="BSD",
    include_package_data = True,
    entry_points="""
      [console_scripts]
      sevabot = sevabot.frontend.main:entry_point
      """,
)