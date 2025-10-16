"""
Setup script for Pegasus Three OSINT Toolkit
"""

from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='pegasus-three',
    version='1.0.0',
    author='Pegasus Team',
    author_email='admin@pegasus-osint.local',
    description='A comprehensive OSINT framework for information gathering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sobri3195/pegasus-three',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pegasus=pegasus:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
