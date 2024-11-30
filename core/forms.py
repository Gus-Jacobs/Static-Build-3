from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
 content = forms.CharField(widget=forms.Textarea(attrs={'class': 'md-textarea form-control', 
    'placeholder': 'Place comment...',
    'rows': '4'}))
 class Meta:
  model = Comment
  fields = ('content', )
