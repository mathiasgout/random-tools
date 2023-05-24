from setuptools import find_packages, setup


setup(
    name="random-tools",
    version="0.0.1",
    author="Mathias Gout",
    packages=find_packages(exclude=["tests"]),
    extras_require={"firebase": ["firebase-admin==6.1.0"]},
    python_requires="==3.9.*",
)
