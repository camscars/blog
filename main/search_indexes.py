from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)  #primary search field
	publish = indexes.DateTimeField(model_attr='publish') #additional filter

	def get_model(self):  #returns the model that will be stored
		return Post

	def index_queryset(self, using=None): #returns QuerySet for objects to be indexed
		return self.get_model().published.all()

		