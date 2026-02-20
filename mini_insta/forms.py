#mini_insta/forms.py
#define the forms that we use for create/ update/deete operaations 

from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    '''Define a form for creating a new post.'''
    image_url = forms.URLField(required=False)

    class Meta:
        model = Post
        fields = ['caption']   
