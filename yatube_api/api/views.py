from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'group')
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if (
            "limit" not in request.query_params
            and "offset" not in request.query_params
        ):
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    lookup_url_kwarg = 'comment_id'

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.select_related('author', 'post')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user).select_related(
            'user', 'following'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
