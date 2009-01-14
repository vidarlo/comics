import datetime

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from comics.common.models import Strip
from comics.sets.models import Set

class SetFeed(Feed):
    feed_type = Atom1Feed
    item_author_name = settings.COMICS_SITE_TITLE
    title_template = 'feeds/strip_title.html'
    description_template = 'feeds/strip_description.html'

    def get_object(self, bits):
        if len(bits) != 1:
            raise Set.DoesNotExist
        return Set.objects.get(name=bits[0])

    def title(self, obj):
        return '%s: Set: %s' % (settings.COMICS_SITE_TITLE, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        from_date = datetime.date.today() \
            - datetime.timedelta(settings.COMICS_MAX_DAYS_IN_FEED)
        return Strip.objects.select_related().filter(comic__set=obj,
            pub_date__gte=from_date).order_by('-pub_date', '-fetched')

    def item_pubdate(self, item):
        return item.fetched

    def item_copyright(self, item):
        return item.comic.rights