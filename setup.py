# setup.py for the are-u-query-ous project

from setuptools import setup, find_packages

setup(
    name="areuqueryous",
    version="0.1.0",
    author="Nico D'Alessandro",  # Optional but recommended
    description="ETL tools and geospatial data loaders for the Are U Query-ous project",
    packages=find_packages(
        include=["shared", "shared.*"]
    ),
    include_package_data=True,
    install_requires=[
        "requests",
        "shapely",
    ],
    python_requires=">=3.8",
)
