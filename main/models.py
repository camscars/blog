from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class PublishedManager(models.Manager):
	def get_queryset(self):            #method that returns QuerySet to be executed
		return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	objects = models.Manager()  #default manager
	published = PublishedManager() #custom manager
	tags = TaggableManager()
	
	def get_absolute_url(self):
		return reverse('blog:post_detail',
						args=[self.publish.year,
							  self.publish.strftime('%m'),   #strftime function to build url using month and day
							  self.publish.strftime('%d'),
							  self.slug])
	class Meta:                       # Order posts in reverse order of publishing date
		ordering = ('-publish',)

	def __str__(self):               #Makes each post display the title in admin interface instead of post1,2,3 etc
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)    #Allows us to deactivate comments as admin

	class Meta:
		ordering = ('created',)     #order comments by date created

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)  #instead of showing up as comment 1,2,3 will display name and date

