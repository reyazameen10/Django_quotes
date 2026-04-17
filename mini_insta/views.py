# mini_insta/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse

from .models import Profile, Post, Like, Follow
from .forms import CreatePostForm
from django.views.generic import View
from .models import Like
from django.shortcuts import redirect
from .models import Follow
from django.views.generic import TemplateView
from .forms import ProfileForm


from rest_framework import status


from .models import Profile
#API views
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
#Login API
from rest_framework.decorators import api_view, permission_classes, api_view
from rest_framework.response import Response


# API view for user login and token generation
@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    print(f"API Login attempt for username: {username}, success: {user is not None}")
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id
        }, status=status.HTTP_200_OK)

    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


#API view to create a post with authentication
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        caption = request.data.get('caption')
        image = request.FILES.get('image')

        post = Post.objects.create(
            caption=caption,
            image=image
        )

        return Response({'message': 'Post created'})
#REST API for serializer

from rest_framework import generics
from .serializers import PostSerializer, ProfileSerializer  # new import the serializer for the Profile model


#List API view for Profile
class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

#Detail API view for Profile

class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

#Post API views

class PostListAPIView(generics.ListCreateAPIView):
    '''
    An PAI view to return a listing of Posts and to create and Post.
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Override the perform_create method to associate the post with the authenticated user's profile

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)



#Detail class
class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


#for editing profile 
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'mini_insta/edit_profile.html', {'form': form})
# Feed API views
class ProfileFeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        return Post.objects.filter(profile=profile).order_by('-created_at')

# Mixin for login and profile
class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/'

    def get_login_url(self):
        return self.login_url

    def get_profile(self):
        return get_object_or_404(Profile, user=self.request.user)


# ---------------------------
# Profile Views
# ---------------------------
class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return Profile.objects.all().order_by('-id')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
    

class MyProfileView(MiniInstaLoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name', 'bio_text', 'profile_image_url']
    template_name = 'mini_insta/update_profile_form.html'
    success_url = '/mini_insta/profile/'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


# Profile Feed / Followers / Following

class ProfileFeedView(ListView):
    model = Post
    template_name = "mini_insta/profile_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        return Post.objects.filter(profile=profile).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context
    

class FollowersListView(DetailView):
    model = Profile
    template_name = "mini_insta/followers.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        context["followers"] = Follow.objects.filter(profile=profile)

        return context


class FollowingListView(DetailView):
    model = Profile
    template_name = "mini_insta/following.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        context["following"] = Follow.objects.filter(follower_profile=profile)

        return context


# ---------------------------
# Search
# ---------------------------
class SearchView(MiniInstaLoginRequiredMixin, ListView):
    model = Profile
    template_name = "mini_insta/search.html"
    context_object_name = "profiles"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Profile.objects.filter(display_name__icontains=query)
        return Profile.objects.all()


# ---------------------------
# Post Views
# ---------------------------
class CreatePostView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def form_valid(self, form):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})
    

class ShowPostView(MiniInstaLoginRequiredMixin, DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])
    
class LikePostView(MiniInstaLoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        post = get_object_or_404(Post, pk=kwargs['pk'])
        profile = self.get_profile()

        Like.objects.create(post=post, profile=profile)

        return redirect('show_post', pk=post.pk)
    

class FollowView(MiniInstaLoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        other_profile = get_object_or_404(Profile, pk=kwargs['pk'])
        my_profile, created = Profile.objects.get_or_create(user=request.user)

        if other_profile != my_profile:
            Follow.objects.get_or_create(
                profile=other_profile,
                follower_profile=my_profile
            )

        return redirect('show_profile', pk=other_profile.pk)

    def get(self, request, *args, **kwargs):
        return redirect('show_profile', pk=kwargs['pk'])
    
    
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_object()
        context['posts'] = Post.objects.filter(profile=profile).order_by('-created_at')

        return context
    
class DeleteFollowView(MiniInstaLoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        other_profile = get_object_or_404(Profile, pk=kwargs['pk'])
        my_profile = self.get_profile()

        Follow.objects.filter(
            profile=other_profile,
            follower_profile=my_profile
        ).delete()

        return redirect('show_profile', pk=other_profile.pk)


class LogoutConfirmationView(TemplateView):
    template_name = "mini_insta/logged_out.html"
    

class AddLikeView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        profile = Profile.objects.get(user=request.user)

        if post.profile != profile:
            Like.objects.get_or_create(profile=profile, post=post)

        return redirect(request.META.get('HTTP_REFERER'))
    
class DeleteLikeView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        profile = Profile.objects.get(user=request.user)

        Like.objects.filter(profile=profile, post=post).delete()

        return redirect(request.META.get('HTTP_REFERER'))
    
class AddFollowView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        other_profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        my_profile = Profile.objects.get(user=request.user)

        if other_profile != my_profile:
            Follow.objects.get_or_create(
                follower=my_profile,
                following=other_profile
            )

        return redirect('show_profile', pk=other_profile.pk)
    

