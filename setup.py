from setuptools import setup, find_packages

with open("requirements.txt", "r") as reqs:
    requirements = reqs.read()

setup(
    name="Anania",
    version="0.1",
    packages=find_packages(),
    description="Python client for interacting with Anania API.",
    author="Team Anania",
    author_email="hrant@anania.ai",
    url="https://github.com/Anania-AI/Anania-Python-Client.git",
    license="MIT",
    install_requires=[requirements]
)