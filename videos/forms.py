from django import forms
from .models import VideoComment

class CommentForm(forms.ModelForm):
	class Meta:
		model = VideoComment
		fields = ['commentText']
		labels ={
			'commentText': ('Comment')
		}