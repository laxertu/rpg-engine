import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpg-engine",
    version="0.0.1",
    author="Luca Stretti",
    author_email="laxertu@gmail.com",
    url="https://github.com/laxertu/rpg-engine",
    packages=setuptools.find_packages(),
)