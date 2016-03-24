from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from ..models import Post
from django.db.models import Count

@register.simple_tag  # Just process the data and return a string
def total_posts():
	return Post.published.count()

@register.inclusion_tag('main/post/latest_posts.html') #process data and return a template
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts': latest_posts}

@register.assignment_tag  # process data return a variable in the context
def get_most_commented_posts(count=5):
	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown') #have to register template filters like tags
def markdown_format(text):
	return mark_safe(markdown.markdown(text))