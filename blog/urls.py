from django.urls import include, path
from rest_framework import routers
from blog import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/comments/', views.PostCommentsTree.as_view()),
    path('posts/<int:post_pk>/comments/<int:comment_pk>', views.CommentsTree.as_view()),
]
