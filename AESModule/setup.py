from setuptools import setup, find_packages

setup(
    name='AESUtils',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'cryptography>=3.4.0',
        'pyspark>=3.0.0'
    ],
    description='A utility package for AES encryption and decryption in PySpark',
    author='Rajesh Kumar',
    python_requires='>=3.8'
)