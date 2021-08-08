from django.urls import include, path
from rest_framework import routers
from blog import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>', views.CommentsTree.as_view()),
]
