.. image:: https://travis-ci.org/cfpb/wagtail-sharing.svg?branch=master
  :alt: Build Status
  :target: https://travis-ci.org/cfpb/wagtail-sharing
.. image:: https://coveralls.io/repos/github/cfpb/wagtail-sharing/badge.svg?branch=master
  :alt: Coverage Status
  :target: https://coveralls.io/github/cfpb/wagtail-sharing?branch=master

wagtail-sharing
===============

Easier sharing of `Wagtail <https://wagtail.io>`_ drafts.

Wagtail Sharing makes it easier to share Wagtail draft content for review by users who don't have access to the Wagtail admin site. It allows you to define an alternate hostname and/or port on which to expose the latest revision of all of your Wagtail pages.

For example, let's say your Wagtail site is running on http://mysite.com. You've created a draft page at slug ``/path/to/draft``, but haven't yet published it. Wagtail Sharing lets you expose that draft page at some other domain, for example http://sharing.mysite.com/path/to/draft.

In another use case, you might have a published page at http://mysite.com/already/published/page, and you've made some draft changes. Wagtail Sharing lets you expose those draft changes at http://sharing.mysite.com/already/published/page while still keeping the same published content at your regular domain.

These examples obviously work best when you have some method of restricting access to http://sharing.mysite.com, for example by only exposing that subdomain on a private network.

Wagtail Sharing lets you create separate sharing sites for each Wagtail Site you have defined. It also supports a configurable visual banner on shared pages to remind reviewers that content may differ from your published site.

This new logic only applies to ``GET`` requests. Other HTTP methods like ``POST`` defer to standard Wagtail handling.

Setup
-----

Install the package using pip:

.. code-block:: bash

  $ pip install wagtail-sharing
 
Add ``wagtailsharing`` as an installed app in your Django settings:

.. code-block:: python

  # in settings.py
  INSTALLED_APPS = (
      ...
      'wagtailsharing',
      ...
  )

Run migrations to create required database tables:

.. code-block:: bash

  $ manage.py migrate wagtailsharing
 
Replace use of Wagtail's catch-all URL pattern:

.. code-block:: diff

  # in urls.py
  -from wagtail.wagtailcore import urls as wagtail_urls
  +from wagtailsharing import urls as wagtailsharing_urls

  ...

  -urlpatterns.append(url(r'', include(wagtail_urls)))
  +urlpatterns.append(url(r'', include(wagtailsharing_urls)))

Sharing sites
-------------

The Wagtail admin now contains a new section under Settings called Sharing Sites that allows users to define how they would like to expose latest page revisions. 

.. image:: https://raw.githubusercontent.com/cfpb/wagtail-sharing/master/docs/images/sharing-sites.png
    :width: 200px
    :height: 100px
    :alt: Sharing sites

No sharing sites exist by default. A sharing site must be manually created for each Wagtail Site to make its latest revisions shareable. Each sharing site is defined by a unique hostname and port number. **Important: configuring your sharing sites improperly could expose draft/private content publicly. Be careful when setting them up!**

Banners
-------

Pages viewed on a wagtail-sharing shared site have a simple banner added to them to remind reviewers that the current published content may differ from the content they are viewing.

.. image:: https://raw.githubusercontent.com/cfpb/wagtail-sharing/master/docs/images/banner.png
    :alt: Banner

This behavior can be disabled by setting ``settings.WAGTAILSHARING_BANNER = False``.  The banner template can be overridden by providing an alternate template file at ``wagtailsharing/banner.html`` similar to how `wagtailadmin template overrides <http://docs.wagtail.io/en/latest/advanced_topics/customisation/admin_templates.html#customising-admin-templates>`_ are supported.

Sharing links
-------------

A page's sharing URL can be retrieved by passing its ``Page`` instance to ``wagtailsharing.helpers.get_sharing_url``. This method returns ``None`` if no shared sites are configured or if the specified page is not routable to a shared site.

Shared pages will also have a new dropdown menu option that links to this sharing URL from the Wagtail page explorer.

.. image:: https://raw.githubusercontent.com/cfpb/wagtail-sharing/master/docs/images/dropdown.png
    :alt: Dropdown with sharing link

Hooks
-----

 .. |before_serve_page| replace:: ``before_serve_page``
 .. _before_serve_page: http://docs.wagtail.io/en/latest/reference/hooks.html#before-serve-page

As with normal page serving, the serving of shared pages continues to respect Wagtail's built-in |before_serve_page|_ hook.

This project adds these additional hooks:

``before_serve_shared_page``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Called before the latest revision of the page is about to be served, just before its ``serve()`` method is called. Like ``before_serve_page`` this hook is passed the page object, the request object, and the ``args`` and ``kwargs`` that will be passed to the page's ``serve()`` method. If the callable returns an ``HttpResponse``, that response will be returned immediately to the user.

This hook could be useful for limiting sharing to only certain page types or for modifying a page's contents when it is shared.

.. code-block:: python

  from wagtail.wagtailcore import hooks

  @hooks.register('before_serve_shared_page')
  def modify_shared_title(page, request, args, kwargs):
      page.title += ' (Shared)'

``after_serve_shared_page``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Called after the page's ``serve()`` method is called but before the response is returned to the user. This hook is passed the page object and the response object returned by ``serve()``. If the callable returns an ``HttpResponse``, that response will be returned immediately to the user.

This hook could be useful for directly modifying the response content, for example by adding custom headers or altering the generated HTML. This hook is used to implement the notification banner described above.

.. code-block:: python

  from wagtail.wagtailcore import hooks

  @hooks.register('after_serve_shared_page')
  def add_custom_header(page, response):
      response['Wagtail-Is-Shared'] = '1'

Compatibility
-------------

This project has been tested for compatibility with:

* Python 2.7, 3.5, 3.6
* Django 1.8-1.11
* Wagtail 1.6-1.13

Open source licensing info
--------------------------

#. `TERMS <https://github.com/cfpb/cfgov-refresh/blob/master/TERMS.md>`_
#. `LICENSE <https://github.com/cfpb/cfgov-refresh/blob/master/LICENSE>`_
#. `CFPB Source Code Policy <https://github.com/cfpb/source-code-policy>`_
