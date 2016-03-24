from django import forms
from .models import Comment

class EmailPostForm(forms.Form):  #Standard form, only use ModelForm when creating or updating a model instance
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField
	comments = forms.CharField(required=False,
							   widget=forms.Textarea)  #override the default small charfield with a textfield

class CommentForm(forms.ModelForm):  #ModelForm, as we are using this class to update or create a model
	class Meta:
		model = Comment              # indicate which model to use
		fields = ('name', 'email', 'body')  # builds a form with all fields by default, can use this to make it only use ones you want.

class SearchForm(forms.Form):
	query = forms.CharField()
	