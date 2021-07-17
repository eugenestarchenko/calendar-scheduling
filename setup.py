import io
from setuptools import setup, find_packages

VERSION = "0.0.1"

project_url = "https://github.com/eugenestarchenko/calendar-scheduling"

DEPENDENCIES = [
    "google-api-python-client==2.8.0",
    "google-auth-httplib2==0.1.0",
    "google-auth-oauthlib==0.4.4",
    "click==8.0.1",
]

with io.open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="gschedule",
    version=VERSION,
    url=project_url,
    author="Eugene Starchenko",
    author_email="eugene.starchenko@gmail.com",
    description="Set on-call events on a Google calendar",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={"console_scripts": ["oncaller = __main__:main"]},
    install_requires=DEPENDENCIES,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
)
