import setuptools
import os

setuptools.setup(
    name="Python2019_Project",
    version="0.0.1",
    author="Bikbulatov Timur and Shitik Artem",
    author_email="bikbulatovtimur96@yandex.ru",
    description="Python3 project for cmc msu course",
    long_description_content_type="text/markdown",
    url="https://github.com/artik008/Python2019_Project",
    packages=setuptools.find_packages() + ['Python2019_Project/images'],
    setup_require=["mo_installer"],
    locale_src='./Python2019_Project/locale',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'': '*'},
    include_package_data=True
)
