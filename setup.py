from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sqlalchemy-dbtoolkit",
    version="0.1.5",
    description="A toolkit for building SQLAlchemy database engines and utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pymetheus",
    author_email="github.senate902@passfwd.com",
    url="https://github.com/Pymetheus/sqlalchemy-dbtoolkit",
    license="MIT",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        "sqlalchemy>=2.0",
        "mysql-connector-python>=9.3.0",
        "psycopg2>=2.9.10",
        "pandas>=2.2.0"
    ],
    python_requires=">=3.8"
)
