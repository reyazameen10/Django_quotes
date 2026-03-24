#mini_insta/forms.py
#define the forms that we use for create/ update/deete operaations 

from django import forms
from .models import Post
from .models import Profile

class CreatePostForm(forms.ModelForm):
    '''Define a form for creating a new post.'''

    class Meta:
        model = Post
        fields = ['image', 'caption']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']