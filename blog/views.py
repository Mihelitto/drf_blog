from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all().order_by('-published_at')
    serializer_class = PostSerializer


class CommentsTree(APIView):
    def get(self, request, pk):
        current_comment = Comment.objects.get(pk=pk)
        current_depth = current_comment.depth
        current_post = current_comment.post
        if current_depth < 3:
            comments = Comment.objects.filter(
                post=current_post,
                depth__range=(current_depth, current_depth+3)
            )
        else:
            comments = Comment.objects.filter(
                post=current_post,
                depth__gt=current_depth
            )
        result_comments = {pk: current_comment}
        for comment in comments:
            if comment.parent_id in result_comments.keys():
                result_comments[comment.id] = comment

        serializer = CommentSerializer(result_comments.values(), many=True)
        return Response({"comment": serializer.data})


class CommentList(APIView):
    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response({"comment": serializer.data})

    def post(self, request):
        comment = request.data.get('comment')
        serializer = CommentSerializer(data=comment)
        if serializer.is_valid(raise_exception=True):
            comment_saved = serializer.save()
        return Response({
            "success":
                f"Comment from '{comment_saved.author}' created successfully"
        })

