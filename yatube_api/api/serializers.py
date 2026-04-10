from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.contrib.auth import get_user_model

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate_following(self, value):
        request = self.context['request']
        if request.user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value

    def validate(self, attrs):
        request = self.context['request']
        following = attrs['following']
        if Follow.objects.filter(
            user=request.user, following=following
        ).exists():
            raise serializers.ValidationError(
                {'following': 'Вы уже подписаны на этого пользователя.'}
            )
        return attrs
