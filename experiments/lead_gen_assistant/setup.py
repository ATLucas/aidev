from setuptools import setup, find_packages

setup(
    name="lead_gen_assistant",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "lead_gen_assistant": ["*.yaml", ".txt"],
    },
    install_requires=[
        "openai",
        "packaging",
        "pyyaml",
        "setuptools",
    ],
)
