import os
from setuptools import setup

setup(
    name = "print_app",
    version = "1.6.0",
    author = "Pa Lia",
    author_email = "pliam1105@gmail.com",
    description = "An app that prints everything you want in the terminal",
    license = "BSD",
    url = "https://launchpad.net/",
    packages=['print_app'],
    entry_points = {
        'gui_scripts' : ['print_app = print_app.print_app:main']
    },
    data_files = [
        ('share/applications/', ['print_app.desktop']),
	('/usr/lib/python3/dist-packages/print_app/',['print_app/terminal.png']),
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
