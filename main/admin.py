from django.contrib import admin
from .models import Post, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'publish', 'status') #only displays these fields in the lists of posts
	list_filter = ('status', 'created', 'publish', 'author')        #crates a filter sidebar using these options 
	search_fields = ('title', 'body')                               #creates a search bar
	prepopulated_fields = {'slug': ('title',)}                      #slug fields are auto-generated using the title when making a new post
	raw_id_fields = ('author',)                                     #use a dropdown menu to select the author
	date_hierarchy = 'publish'                                      #adds a bar to navigate through date ranges
	ordering = ['status', 'publish']                                #sets default ordering

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'email', 'body')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)