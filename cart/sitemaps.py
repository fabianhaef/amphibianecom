from django.contrib.sitemaps import Sitemap

from .models import Product


class ProductSitemap(Sitemap):
    change_frequency = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated
