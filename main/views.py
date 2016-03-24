from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
								   PageNotAnInteger	
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet
# Create your views here.
#Function-based

def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 3) # 3 posts in each page
	page = request.GET.get('page')  #retrieve the corresponding page number
	tag= None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		#If page not integer deliver first page
		posts = paginator.page(1)
	except EmptyPage:
		# If page out of range deliver last page
		posts = paginator.page(paginator.num_pages)
	return render(request, 'main/post/list.html', {'page': page,'posts': posts,'tag': tag})



class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'main/post/list.html'


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, 
								   status='published',
								   publish__year=year,
								   publish__month=month,
								   publish__day=day)
	# Only list the active comments
	comments = post.comments.filter(active=True)

	if request.method == 'POST': 
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False) #doesnt save to database yet
			new_comment.post = post   #assigns current post to this comment
			new_comment.save()        #saves to database
	else:
		comment_form = CommentForm()
	# List similar posts
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)   #retrieve a list of posts that have the same tags excluding the current one
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]  #count the number of tags they have in common, order them by this and publish date
	return render(request, 'main/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts})  

def post_share(request, post_id):
	#Retrieve post by id
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False
	if request.method == 'POST':
		#Form was submitted, post is used when user provides input
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_url(post.get_absolute_url())
			subject = '{}  recommends reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
			# send the email
	else:                      #If request = GET then no information submitted, display empty form
		form = EmailPostForm()
	return render(request, 'main/post/share.html', {'post':post, 'form': form})

def post_search(request):
	form = SearchForm()
	cd = {}
	results = {}
	total_results = {}
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			cd = form.cleaned_data
			results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
			# count total results
			total_results = results.count()
	return render(request, 'main/post/search.html', {'form': form, 'cd': cd, 'results': results, 'total_results': total_results})



