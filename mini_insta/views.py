# mini_insta/views.py

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post
from .forms import CreatePostForm #import the form class for creating a new post
from django.urls import reverse

class ProfileListView(ListView):
    '''Define a view to show all the profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    '''Define a view to show one profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

# class CreatePostView(CreateView): 
class CreatePostView(CreateView):
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile  # attach profile to the post
        response = super().form_valid(form)

        # attach image if provided
        image_url = self.request.POST.get('image_url')
        if image_url:
            Post.objects.create(
                profile=self.object.profile,
                caption=self.object.caption,
                image_url=image_url
            )

        return response

    def get_success_url(self):
        return reverse('show_post', kwargs={'pk': self.object.pk})

class ShowPostView(DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'
    
    def get_success_url(self):

        return reverse('show_post', kwargs={'pk': self.object.pk})