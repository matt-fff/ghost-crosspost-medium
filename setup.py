from os import path
import re
import io
from setuptools import setup

PACKAGE_NAME = "medium-crosspost"
PACKAGE_PATH = "medium_crosspost"
HERE = path.abspath(path.dirname(__file__))

with io.open(path.join(HERE, "README.md"), encoding="utf-8") as fp:
    README = fp.read()

with io.open(path.join(HERE, PACKAGE_PATH, "__init__.py"), encoding="utf-8") as fp:
    VERSION = re.search("__version__ = \"([^\"]+)\"", fp.read()).group(1)

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_PATH],
    version=VERSION,
    long_description=README,
    long_description_content_type="text/markdown",
    description="Easily crosspost articles to Medium",
    author="typenil",
    author_email="code@typenil.com",
    url="https://github.com/typenil/ghost-crosspost-medium",
    license="MIT License",
    install_requires=["requests"],
    keywords="medium ghost crosspost blog zapier",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
)
