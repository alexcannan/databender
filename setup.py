from setuptools import find_packages, setup


setup(
    name="getbent",
    author="Alex Cannan",
    version="0.1.0",
    packages=find_packages("getbent"),
    install_requires=[
        "numpy",
    ],
)