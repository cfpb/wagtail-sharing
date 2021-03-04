All notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.

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
