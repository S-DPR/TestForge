from setuptools import setup, find_packages

setup(
    name="kafka_common",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "confluent-kafka>=2.3.0",
        "pydantic>=2.0",
        "loguru>=0.7.0",
        "jsonschema>=4.0.0"
    ]
)
