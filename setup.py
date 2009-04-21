from setuptools import setup, find_packages
import os

version = '1.0'

tests_require = ['collective.testcaselayer']

setup(name='collective.formcriteria',
      version=version,
      description=
      "Add forms for user enterable search criteria to collections.",
      long_description='\n'.join(
          open(os.path.join(*path)).read() for path in [
              ("src", "collective", "formcriteria", "README.txt"),
              ("src", "collective", "formcriteria", "criteria", "sort.txt"),
              ("docs", "HISTORY.txt"),
              ("docs", "TODO.txt")]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='http://pypi.python.org/pypi/collective.formcriteria',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'':'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.browserlayer',
      ],
      tests_require=tests_require,
      extras_require={'tests': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
