from rest_framework import routers

from .api import KnowledgeBaseViewSet

urlpatterns = []

app_name = "knowledgebase"

router = routers.SimpleRouter()

router.register(r"knowledgebase", KnowledgeBaseViewSet, basename="knowledgebase")

urlpatterns += router.urls
