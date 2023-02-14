from django.urls import include, path

urlpatterns = []

auth_urls = [
    path('auth/', include('dj_rest_auth.urls'))
]

urlpatterns += auth_urls
