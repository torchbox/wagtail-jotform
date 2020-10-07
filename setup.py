from os import path

from setuptools import find_packages, setup

from wagtail_jotform import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="wagtail-jotform",
    version=__version__,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    description="Embed Jotform forms in wagtail.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevinhowbrook/wagtail-jotform",
    author="Kevin Howbrook",
    author_email="kevin.howbrook@torchbox.com",
    license="BSD",
    install_requires=["wagtail>=2.0"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
    ],
)
