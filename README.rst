.. image:: https://github.com/cfpb/wagtail-sharing/workflows/test/badge.svg?branch=main
  :alt: Build Status
  :target: https://github.com/cfpb/wagtail-sharing/actions?query=branch%3Amain+workflow%3Atest+

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

``wagtail.snippets`` is also required and must be included in your list of installed apps.

The code examples below assume that you are using a recent Wagtail version (3.0+).

Run migrations to create required database tables:

.. code-block:: bash

  $ python manage.py migrate wagtailsharing

Replace use of Wagtail's catch-all URL pattern:

.. code-block:: diff

  # in urls.py
  -from wagtail import urls as wagtail_urls
  +from wagtailsharing import urls as wagtailsharing_urls

  ...

  -urlpatterns.append(url(r'', include(wagtail_urls)))
  +urlpatterns.append(url(r'', include(wagtailsharing_urls)))

Sharing sites
-------------

The Wagtail admin now contains a new section under Settings called Sharing Sites that allows users to define how they would like to expose latest page revisions.

.. image:: ./docs/images/sharing-sites.png
    :width: 640px
    :alt: Sharing sites

No sharing sites exist by default. A sharing site must be manually created for each Wagtail Site to make its latest revisions shareable. Each sharing site is defined by a unique hostname and port number. **Important: configuring your sharing sites improperly could expose draft/private content publicly. Be careful when setting them up!**

Creating a new sharing site
---------------------------

After following the setup steps above, you should be able to create a new sharing site to use this functionality in a local Django development server. Let's assume that you are running your local development server on the default port 8000, and that pages there are being served at http://localhost:8000. We want to create a new sharing site at http://sharing.localhost:8000 at which latest page revisions will be exposed.

To simulate accessing your site on a different hostname, you'll need to loosen `Django's default security settings <https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts>`_ that only allow access on `localhost`. Edit your settings file (e.g. ``myproject/settings/local.py``) to add the following:

.. code-block:: python

  ALLOWED_HOSTS = ['*']

Verify that you can access your local server at http://sharing.localhost:8000. You should see the same content there as on http://localhost:8000, as you haven't enabled wagtail-sharing for the default site yet.

To do so, in the Wagtail admin, under Settings, Sharing Sites, create a new sharing site for the default site, with hostname ``sharing.localhost`` and port ``8000``.

.. image:: ./docs/images/new-sharing-site.png
    :width: 640px
    :alt: New sharing site with site: "localhost [default]", hostname: "sharing.localhost", port: "8000"

Your latest page revisions (including drafts) should now be available at http://sharing.localhost:8000.

Banners
-------

Pages viewed on a wagtail-sharing shared site have a simple banner added to them to remind reviewers that the current published content may differ from the content they are viewing.

.. image:: ./docs/images/banner.png
    :alt: Banner

This behavior can be disabled by setting ``settings.WAGTAILSHARING_BANNER = False``.  The banner template can be overridden by providing an alternate template file at ``wagtailsharing/banner.html`` similar to how `wagtailadmin template overrides <http://docs.wagtail.io/en/latest/advanced_topics/customisation/admin_templates.html#customising-admin-templates>`_ are supported.

Sharing links
-------------

A page's sharing URL can be retrieved by passing its ``Page`` instance to ``wagtailsharing.helpers.get_sharing_url``. This method returns ``None`` if no shared sites are configured or if the specified page is not routable to a shared site.
A page's sharing URL is based on the slug of its most recently published revision
or, if the page has never been published, its initial revision.

Shared pages will also have a new dropdown menu option that links to this sharing URL from the Wagtail page explorer.

.. image:: ./docs/images/dropdown.png
    :alt: Dropdown with sharing link
    :width: 640px

Hooks
-----

 .. |before_serve_page| replace:: ``before_serve_page``
 .. _before_serve_page: http://docs.wagtail.io/en/latest/reference/hooks.html#before-serve-page

As with normal page serving, the serving of shared pages continues to respect Wagtail's built-in |before_serve_page|_ hook.

This project adds these additional hooks:

``before_route_page``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Called when routing, before a page's ``route()`` method is called. This hook is passed the ``request`` and the ``page`` that will have ``route()`` called on it. If the callable returns an ``HttpResponse``, that response will be returned immediately to the user.

This hook allows for any necessary customization of Wagtail's built-in routing behavior, for example to support `ShareableRoutablePageMixin`_.

``before_serve_shared_page``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Called before the latest revision of the page is about to be served, just before its ``serve()`` method is called. Like ``before_serve_page`` this hook is passed the page object, the request object, and the ``args`` and ``kwargs`` that will be passed to the page's ``serve()`` method. If the callable returns an ``HttpResponse``, that response will be returned immediately to the user.

This hook could be useful for limiting sharing to only certain page types or for modifying a page's contents when it is shared.

.. code-block:: python

  from wagtail import hooks

  @hooks.register('before_serve_shared_page')
  def modify_shared_title(page, request, args, kwargs):
      page.title += ' (Shared)'

``after_serve_shared_page``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Called after the page's ``serve()`` method is called but before the response is returned to the user. This hook is passed the page object and the response object returned by ``serve()``. If the callable returns an ``HttpResponse``, that response will be returned immediately to the user.

This hook could be useful for directly modifying the response content, for example by adding custom headers or altering the generated HTML. This hook is used to implement the notification banner described above.

.. code-block:: python

  from wagtail import hooks

  @hooks.register('after_serve_shared_page')
  def add_custom_header(page, response):
      response['Wagtail-Is-Shared'] = '1'

Mixins
------

``ShareableRoutablePageMixin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 .. |RoutablePageMixin| replace:: ``RoutablePageMixin``
 .. _RoutablePageMixin: https://docs.wagtail.io/en/stable/reference/contrib/routablepage.html

By default, Wagtail's |RoutablePageMixin|_ is not compatible with Wagtail-Sharing, instead you need to use ``ShareableRoutablePageMixin`` in order to view share draft content fields on routable pages.

``ShareableRoutablePageMixin`` is used exactly the same way as |RoutablePageMixin|_:

.. code-block:: python

  from wagtail.fields import RichTextField
  from wagtail.models import Page
  from wagtail.contrib.routable_page.models import route
  from wagtailsharing.models import ShareableRoutablePageMixin


  class EventIndexPage(ShareableRoutablePageMixin, Page):
      intro = RichTextField()

      @route(r'^$')
      def current_events(self, request):
          # …

      @route(r'^past/$')
      def past_events(self, request):
          # …

Compatibility
-------------

This project has been tested for compatibility with:

* Python 3.9+
* Django 3.2+
* Wagtail 5.1+ (see past releases for older Wagtail support)

It should be compatible with all intermediate versions, as well.
If you find that it is not, please `file an issue <https://github.com/cfpb/wagtail-sharing/issues/new>`_.

Testing
-------

Running project unit tests requires `tox <https://tox.wiki/en/latest/>`_:

.. code-block:: bash

  $ tox

To run the test app interactively, run:

.. code-block:: bash

  $ tox -e interactive

Now you can visit http://localhost:8000/admin/ in a browser and log in with ``admin`` / ``changeme``.

Open source licensing info
--------------------------

#. `TERMS <https://github.com/cfpb/cfgov-refresh/blob/main/TERMS.md>`_
#. `LICENSE <https://github.com/cfpb/cfgov-refresh/blob/main/LICENSE>`_
#. `CFPB Source Code Policy <https://github.com/cfpb/source-code-policy>`_
