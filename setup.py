from setuptools import find_packages, setup


install_requires = [
    "wagtail>=2.15",
    "django>=3.2,<5.0",
    "pyjwt>1.7,<2.5",
]

testing_extras = ["coverage>=3.7.0"]

setup(
    name="wagtail-sharing",
    url="https://github.com/cfpb/wagtail-sharing",
    author="CFPB",
    author_email="tech@cfpb.gov",
    license="CCO",
    version="2.7",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
    description="Easier sharing of Wagtail drafts",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Framework :: Wagtail :: 3",
        "Framework :: Wagtail :: 4",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
