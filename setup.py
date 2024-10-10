import os
import re
import setuptools

PKGNAME="pyvara"
MODULENAME="vara"
META_PATH = os.path.join(MODULENAME, "__init__.py")
META_FILE = open(META_PATH, "r").read()

def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=PKGNAME,
    version=find_meta("version"),
    license=find_meta("license"),
    author=find_meta("author"),
    author_email=find_meta("author_email"),
    description="Python library for VARA modem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/petrkr/"+PKGNAME,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.11'
)
