from django.contrib import sitemaps
from django.contrib.sitemaps import Sitemap
from .models import Item, Category


class ItemSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Item.objects.all()

    def lastmod(self, obj):
        return obj.updated


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Category.objects.all()
