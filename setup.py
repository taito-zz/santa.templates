from setuptools import find_packages
from setuptools import setup


setup(
    name='santa.templates',
    version='0.0',
    description="",
    long_description=open("README.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
    ],
    keywords='',
    author='ABITA',
    author_email='taito.horiuchi@abita.fi',
    url='',
    license='None-free',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['santa'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.PloneFormGen',
        'collective.contentleadimage',
        'five.grok',
        'hexagonit.testing',
        'plone.app.contentlisting',
        'plone.browserlayer',
        'santa.content',
        'setuptools',
        'zope.i18nmessageid',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
