class RouterBase:
    def route(self, request, path):
        raise NotImplementedError

    def get_sharing_url(self, page):
        raise NotImplementedError

    def _get_page_url_parts(self, page):
        # Retrieve the version of the page persisted to the database to
        # make sure we're using its routable path.
        if page.pk is not None:
            page = page.specific_class.objects.get(pk=page.pk)

        return page.get_url_parts()
