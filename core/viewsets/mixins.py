from rest_framework.mixins import DestroyModelMixin


class ArchiveModelMixin(DestroyModelMixin):
    """
    Archives a record
    """

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
