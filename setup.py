from setuptools import find_packages, setup


install_requires = [
    "wagtail>=2.3,<2.11",
]


testing_extras = [
    "coverage>=3.7.0",
    "flake8>=2.2.0",
    "mock>=1.0.0",
]


setup(
    name="wagtail-sharing",
    url="https://github.com/cfpb/wagtail-sharing",
    author="CFPB",
    author_email="tech@cfpb.gov",
    license="CCO",
    version="2.2.1",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
    description="Easier sharing of Wagtail drafts",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
