import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "TWiki_To_Moin",
    version = "1.0",
    packages = find_packages(),
    scripts = ['bin/twiki_to_moin'],
    test_suite = "twiki_to_moin.tests.test_conversion.suite",

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = "Mike Pittaro",
    author_email = "mikeyp@lhrc.com",
    description = "TWiki to Moin Moin conversion utility",
    license = "GNU General Public License v3 or later (GPLv3+)",
    keywords = "moin moinmoin wiki twiki converter",
    # TODO(mikeyp) update URL for github 
    url = "http://example.com/HelloWorld/",   # project home page, if any
)
