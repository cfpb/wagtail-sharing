from django.utils.module_loading import import_string


def get_router_cls():
    from django.conf import settings

    return getattr(
        settings,
        "WAGTAILSHARING_ROUTER",
        "wagtailsharing.routers.db.DatabaseHostRouter",
    )


def get_router():
    return import_string(get_router_cls())()
