from setuptools import find_packages, setup


setup(
    name="random-tools",
    author="Mathias Gout",
    packages=find_packages(),
    extras_require={
        "firebase": [
            "firebase-admin==6.1.0"
        ]
    },
    python_requires="==3.9.*"
)