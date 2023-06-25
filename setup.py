from setuptools import find_packages, setup


setup(
    name="random-tools",
    version="0.0.4",
    author="Mathias Gout",
    packages=find_packages(exclude=["tests"]),
    python_requires="==3.9.*",
)
