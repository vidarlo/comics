from django.conf.urls.defaults import include, patterns

from tastypie.api import Api

from comics.api.resources import ComicResource, ImageResource, ReleaseResource

v1_api = Api(api_name='v1')
v1_api.register(ComicResource())
v1_api.register(ImageResource())
v1_api.register(ReleaseResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)
