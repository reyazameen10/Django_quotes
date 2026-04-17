#mini_insta / serializer.py

from rest_framework import serializers
from .models import Post, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'display_name', 'profile_image_url', 'bio_text']


class PostSerializer(serializers.ModelSerializer):
    # read-only nested profile (for GET requests)
    image = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)
    profile_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

# Custom method to get the image URL
    def get_image(self, obj):
        request = self.context.get('request')

        if not obj.image:
            return None

        # If it's a real Django ImageField
        if hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)

        # If it's a URLField or a string URL
        return obj.image

    def create(self, validated_data):
        request = self.context.get('request')

        # automatically attach logged-in user's profile
        if request and hasattr(request, 'user'):
            try:
                validated_data['profile'] = request.user.profile
            except Profile.DoesNotExist:
                raise serializers.ValidationError(
                    "Profile does not exist for this user."
                )

        # create and return the post
        return Post.objects.create(**validated_data)