from setuptools import setup, find_packages

setup(
    name = "TWiki_To_Moin",
    version = "0.1",
    packages = find_packages(),
    scripts = ['bin/twiki_to_moin'],
    test_suite = "twiki_to_moin.tests.test_conversion.suite",

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # TODO(mikeyp) review dependeicies 
    # install_requires = ['docutils>=0.3'],

    # TODO(mikeyp) update to include test data, docs, etc   
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Mike Pittaro",
    author_email = "mikeyp@lhrc.com",
    description = "twiki to moin conversion utility",
    license = "GNU General Public License v3 or later (GPLv3+)",
    keywords = "moin moinmoin twiki conversion",
    # TODO(mikeyp) update URL for github 
    url = "http://example.com/HelloWorld/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)

