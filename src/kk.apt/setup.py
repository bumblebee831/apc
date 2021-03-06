from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='kk.apt',
      version=version,
      description="Androschin & Partner Transactions Services Diazo Plone Theme",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='kreativkombinat GbR',
      author_email='info@kreativkombinat.de',
      url='http://dist.kreativkombinat.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['kk'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.theming',
          'plone.app.themingplugins',
          'plone.app.toolbar',
          'plone.app.widgets',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
