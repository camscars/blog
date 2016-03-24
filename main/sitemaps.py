from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):    #which Queryset of items to use
		return Post.published.all()

	def lastmod(self, obj):  #tells the last time each item was modified
		return obj.publish
