from setuptools import find_packages, setup

install_requires = [
    "wagtail>=2.15,<4.0",
    "django>=3.0,<4.0",
]

testing_extras = ["coverage>=3.7.0", "mock>=3.0.0"]

setup(
    name="wagtail-sharing",
    url="https://github.com/cfpb/wagtail-sharing",
    author="CFPB",
    author_email="tech@cfpb.gov",
    license="CCO",
    version="2.6",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
    description="Easier sharing of Wagtail drafts",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2.15",
        "Framework :: Wagtail :: 2.16",
        "Framework :: Wagtail :: 3.0",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
