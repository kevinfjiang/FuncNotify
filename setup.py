import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="funcNotifys",
    version="1.0.0",
    description="Get Notified when your functions finish running",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kevinfjiang/FuncNotify",
    author="kevinfjiang",
    author_email="kevin.jiang016@gmail.com.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3s"
        "Programming Language :: Python :: 3.9",
    ],
    packages=["funcNotify"],
    include_package_data=True,
    install_requires=["twilio", "slackclient", "python-dotenv"],
    entry_points={ # What the fuck iss this
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)