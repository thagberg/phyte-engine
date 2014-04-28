import os
from distutils.core import setup

setup(
    name = "PhyteEngine",
    version = "0.2",
    author = "Tim Hagberg",
    author_email = "timothy.m.hagberg@gmail.com",
    description = ("A 2D fighting game engine built on Pygame"),
    license = "MIT",
    packages = ["engine", "tools"],
    install_requires = [
        "dill == 0.2b1"
    ]
)
