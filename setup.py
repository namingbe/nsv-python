from setuptools import setup, find_packages

setup(
    name="nsv",
    version="0.1.0",
    packages=find_packages(),
    description="Parser for Newline-Separated Values format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="naming",
    url="https://github.com/namingbe/nsv-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
