from setuptools import find_packages, setup


install_requires = [
    'Django>=1.11,<2.3',
    'wagtail>=1.6,<2.9',
]


testing_extras = [
    'coverage>=3.7.0',
    'flake8>=2.2.0',
    'mock>=1.0.0',
]


short_description = 'Easier sharing of Wagtail drafts'


setup(
    name='wagtail-sharing',
    url='https://github.com/cfpb/wagtail-sharing',
    author='CFPB',
    author_email='tech@cfpb.gov',
    license='CCO',
    version='1.0',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    },
    description=short_description,
    long_description=open('README.rst').read(),
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 1',
        'Framework :: Wagtail :: 2',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
