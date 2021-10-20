import pathlib
import requests
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "READMEPYPI.md").read_text() # GitHUB markdown is different

# This call to setup() does all the work

with open("requirements.txt") as file: # Pulls from requirements.txt
    req = [line.rstrip() for line in file]

setup(
    name="FuncNotify",
    version=requests.get("https://api.github.com/repos/kevinfjiang/FuncNotify/releases/latest").json()['name'].split("v")[1],
    description="Get notified when your functions finish running",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kevinfjiang/FuncNotify",
    author="kevinfjiang",
    author_email="kevin.jiang016@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["FuncNotify"],
    include_package_data=True,
    install_requires=req,
    entry_points={ 
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)