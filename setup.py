"""Python setup.py for radex package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("radex", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="radex",
    version=read("radex", "VERSION"),
    description="Awesome radex created by ljhowell",
    url="https://github.com/ljhowell/radex/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="ljhowell",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=[
        *read_requirements("requirements.txt"),
        "negex @ git+https://github.com/ljhowell/negex.git@master#egg=negex"
    ],
    extras_require={"test": read_requirements("requirements-test.txt")},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="BSD 3-Clause License",
    python_requires='>=3.7',
)
