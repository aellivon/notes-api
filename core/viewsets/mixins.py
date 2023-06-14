from rest_framework import mixins, viewsets


class ArchiveModelMixin(mixins.DestroyModelMixin):
    """
    Archives a record
    """

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class AppModelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, mixins.UpdateModelMixin, ArchiveModelMixin):

    pass
