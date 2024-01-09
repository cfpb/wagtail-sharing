All notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.

## 2.12.1 2024-01-09

- Fix deprecation warning in Wagtail 5.2 (https://github.com/cfpb/wagtail-sharing/pull/73)

## 2.12 - 2023-12-19

- Add support for Wagtail 5.1 and 5.2 (https://github.com/cfpb/wagtail-sharing/pull/71)
- Drop support for Wagtail < 5.1 and dependence on wagtail.contrib.modeladmin

## 2.11 - 2023-11-29

- Add support for Wagtail 5.0 (https://github.com/cfpb/wagtail-sharing/pull/70)

## 2.10 - 2023-08-16

- Deprecate reliance on Wagtail's testapp (https://github.com/cfpb/wagtail-sharing/pull/68)
- Fix: get_sharing_url should use database slug (https://github.com/cfpb/wagtail-sharing/pull/67)

## 2.9 - 2023-05-12

- Added the "View sharing link" to page header links ([#63](https://github.com/cfpb/wagtail-sharing/pull/63))

## 2.8

- Fix flake8 configuration by @chosak in https://github.com/cfpb/wagtail-sharing/pull/58
- Remove definition of default_app_config by @chosak in https://github.com/cfpb/wagtail-sharing/pull/60
- Add support for Wagtail 4.2 by @willbarton, @chosak, and @nickmoreton in https://github.com/cfpb/wagtail-sharing/pull/62

## 2.7 - 2022-07-13

- Added support for Wagtail 3.0 (thanks [@nickmoreton](https://github.com/nickmoreton)!)

## 2.6 - 2022-03-10

- Update tests to Python 3.9
- Adds Django 4.0 support

## 2.5.1 - 2021-03-05

- Included a delete migration for `ShareableRoutablePage`, a model that does not exist but was accidentially included via migration in 2.5.0

## 2.5 - 2021-03-04

- Add `ShareableRoutablePageMixin` to enable sharing of draft default routes on routable pages
- Add a `before_route_page` hook
- Add `routed_by_wagtail_sharing` and `served_by_wagtail_sharing` attributes to requests

## 2.4 - 2021-01-29

- Add GITHUB_TOKEN to our action env
- Add DOTALL flag to sharing banner body-RE
- Handle hook signature change in Wagtail 2.10+

## 2.1 - 2020-04-07

- Improve error messages by refactoring ServeView

## 2.0 - 2020-03-31

- Adding Django 2.2 support, dropping Wagtail 1 support
- Introduces Black autoformatting.

## 1.0 - 2020-02-21

- Add support for Wagtail 2.8
- Remove testing for Python 2.7

## 0.8 - 2019-07-29

- Improve getting started documentation.
- Add support for RoutablePageMixin.

## 0.7 - 2018-05-11

- Simplified CHANGELOG format.
- Removed superfluous tests of `Page.get_admin_display_title`.
- Add additional tests for the `before_serve_shared_page` and `after_serve_shared_page` hooks.
- Added Django check and note in README to clarify dependency on `wagtail.contrib.modeladmin` app.
- Fixed MANIFEST.in to properly include only appropriate HTML templates.
- Added unit test against requests without `SERVER_PORT`.
- Added support for Django 2.0 and Wagtail 2.0.


## 0.6 - 2017-11-27

- Adds testing against Django 1.11 and Wagtail 1.13.
- Adds additional hooks to support custom serve logic.


## 0.5.1 - 2017-10-31

- Adds testing against Wagtail 1.10.
- setup.py now includes Trove classifiers for PyPI.


## 0.5 - 2017-04-04

- Explicitly only invoke sharing logic on HTTP GET requests.
- Better and simpler logic for preview banner insertion.


## 0.4 - 2017-03-27

- Improved README formatting for PyPI.


## 0.3 - 2017-03-01

- Improved sharing link text in Wagtail admin menu.


## 0.2 - 2017-02-22

- Moved sharing configuration to Django model.
- Update default banner text.
- Add sharing link to Wagtail admin page browser.


## 0.1 - 2017-02-21

- Initial release.
