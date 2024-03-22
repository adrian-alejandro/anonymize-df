import pathlib
from setuptools import setup

import versioneer

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="anonymize-df",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Fork of anonymizedf, a convenient way to anonymize your data for analytics.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/adrian-alejandro/anonymize-df",
    author="Adrián Zelaya, Alexander Fridriksson",
    author_email="zelaya.adrian@gmail.com, post@alexanderfridriksson.com",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
    ],
    keywords='faker pandas anonymize fake mock data',
    packages=["anonymize-df"],
    include_package_data=True,
    install_requires=["pandas", "faker"]
)
