from setuptools import setup, find_packages

setup(
    name="coding_agents",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "coding_agents": ["*.yaml", ".json", ".txt"],
    },
    install_requires=[
        "openai",
        "packaging",
        "pyyaml",
        "setuptools",
    ],
)
