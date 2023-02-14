from django.urls import include, path

urlpatterns = []

app_name = "users"

auth_urls = [
    path('auth/', include('dj_rest_auth.urls'))
]

urlpatterns += auth_urls
