from django.utils.text import slugify

from wagtail import VERSION as WAGTAIL_VERSION


if WAGTAIL_VERSION >= (3, 0):    
    from wagtail.test.routablepage.models import RoutablePageTest
    from wagtail.test.testapp.models import SimplePage
else:
    from wagtail.tests.routablepage.models import RoutablePageTest
    from wagtail.tests.testapp.models import SimplePage


def create_draft_page(site, title):
    page = SimplePage(
        title=title, slug=slugify(title), content="content", live=False
    )

    site.root_page.add_child(instance=page)
    return page


def create_draft_routable_page(site, title):
    page = RoutablePageTest(title=title, live=False)
    site.root_page.add_child(instance=page)
    return page
