from os import path

from setuptools import find_packages, setup

from wagtail_jotform import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

testing_extras = ["coverage>=7.0", "tox>=4.11.0"]
development_extras = ["black", "isort", "flake8", "pre-commit"]

setup(
    name="wagtail-jotform",
    version=__version__,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    description="Embed Jotform forms in wagtail.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/torchbox/wagtail-jotform",
    author="Kevin Howbrook",
    author_email="kevin.howbrook@torchbox.com",
    license="BSD",
    python_requires=">=3.10",
    install_requires=["wagtail>=7.0", "requests"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 7",
    ],
    extras_require={"testing": testing_extras, "development": development_extras},
)
