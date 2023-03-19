from rest_framework import routers
from django.urls import include, path

from .api import UserViewSet, DivisionViewSet

urlpatterns = []

app_name = "users"

router = routers.SimpleRouter()

router.register(r"", UserViewSet, basename="user")
router.register(r"division", DivisionViewSet, basename="division")

auth_urls = [
    path('auth/', include('dj_rest_auth.urls'))
]

urlpatterns += auth_urls
urlpatterns += router.urls
