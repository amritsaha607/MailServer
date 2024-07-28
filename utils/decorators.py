from django.urls import path

from MailServer.urls import urlpatterns


def add_to_urlpatterns(endpoint):
    urlpatterns += [
        path(endpoint, )
    ]


def url_mapper(endpoint):

    def wrapper(function):

        return function()

    return wrapper
