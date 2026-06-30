from setuptools import setup, find_packages

version = '1.1.0'

setup(
    name='ckanext-ldm_schema',
    version=version,
    description="LDM Schema",
    long_description="""
    Schema for the Leibniz Data Manager (LDM) based on ckanext-scheming.

    Leibniz Data Manager: https://github.com/SDM-TIB/LDM_Docker
    """,
    classifiers=[
        "Development Status :: 5 - Production/Stable"
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Programming Language :: Python :: 3 :: Only"
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='ckan',
    author='Mauricio Brunet, Philipp D. Rohde',
    author_email='Mauricio.Brunet@tib.eu',
    url='https://github.com/TIB-SDM/ckanext-ldm_schema',
    license='GNU/GPLv3',
    packages=find_packages(),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ckanext-scheming>=3.0.0',
    ],
    entry_points="""
    [ckan.plugins]
    ldm_schema=ckanext.ldm_schema.plugins:LDMSchemaPlugin
    scheming_tibupdateresources=ckanext.ldm_schema.plugins:TIBupdateResourcesPlugin
    """,
)
