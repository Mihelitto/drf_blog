from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all().order_by('-published_at')
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentsTree(APIView):
    def get(self, request, post_pk, comment_pk):
        try:
            current_comment = Comment.objects.get(pk=comment_pk, post_id=post_pk)
        except Comment.DoesNotExist:
            raise Http404
        current_depth = current_comment.depth
        if current_depth < 3:
            comments = Comment.objects.filter(
                post_id=post_pk,
                depth__range=(current_depth, current_depth+3)
            )
        else:
            comments = Comment.objects.filter(
                post_id=post_pk,
                depth__gt=current_depth
            )
        result_comments = {comment_pk: current_comment}
        for comment in comments:
            if comment.parent_id in result_comments.keys():
                result_comments[comment.id] = comment

        serializer = CommentSerializer(result_comments.values(), many=True)
        return Response({"comments": serializer.data})


class PostCommentsTree(APIView):
    def get(self, request, post_pk):
        comments = Comment.objects.filter(
                post_id=post_pk,
                depth__lte=3
        )

        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})
