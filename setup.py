from os import path, environ
import re
import io
from setuptools import setup

PACKAGE_NAME = "medium-crosspost"
PACKAGE_PATH = "medium_crosspost"
HERE = path.abspath(path.dirname(__file__))

with io.open(path.join(HERE, "README.md"), encoding="utf-8") as fp:
    README = fp.read()

# Retrieves the last version from the environment
LAST_PYPI_VERSION = environ["LAST_PYPI_VERSION"]

# Strips out the final number into it's own variable
PATCH_NUM = re.search('[0-9]+$', LAST_PYPI_VERSION).group(0)

# Increases the patch number and creates the updated version.
VERSION = f"{LAST_PYPI_VERSION[:-len(PATCH_NUM)]}{int(PATCH_NUM) + 1}"

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_PATH],
    version=VERSION,
    long_description=README,
    long_description_content_type="text/markdown",
    description="Easily crosspost articles to Medium",
    author="Matt White",
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
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
)
