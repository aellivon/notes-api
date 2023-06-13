from rest_framework import routers
from django.urls import include, path

from .api import UserViewSet, GroupViewSet

urlpatterns = []

app_name = "users"

router = routers.SimpleRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"group", GroupViewSet, basename="group")

auth_urls = [
    path('auth/', include('dj_rest_auth.urls'))
]

urlpatterns += auth_urls
urlpatterns += router.urls
