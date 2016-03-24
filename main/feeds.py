from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
	title = 'My Blog'
	link = '/blog'
	description = 'New Posts of my blog'

	def items(self):   #retrieves the objects for the feed (last 5)
		return Post.published.all()[:5]

	def item_title(self, item):  #get the objects title
		return item.title

	def item_description(self, item): #get the objects description
		return truncatewords(item.body, 30)