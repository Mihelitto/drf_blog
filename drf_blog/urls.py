from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]