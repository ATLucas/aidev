from setuptools import setup, find_packages

setup(
    name="newsletter_va",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "newsletter_va": ["*.yaml", ".txt"],
    },
    install_requires=[
        "openai",
        "packaging",
        "pyyaml",
        "setuptools",
    ],
)
