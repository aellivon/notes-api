from rest_framework import filters


class UserGroupFilter(filters.BaseFilterBackend):
    """
    Filter that checks if it belongs to a specific division
    """

    def filter_queryset(self, request, queryset, view):

        group = request.query_params.get("group", "*")
        if group == "*" or not group:
            return queryset

        try:
            group = int(group)
        except ValueError as e:
            print(e)
            return queryset

        return queryset.filter(groups__pk=group)


class StringUserStatusFilter(filters.BaseFilterBackend):
    """
    Filter that checks user status
    """

    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get("status", "all")

        if status.lower() == "all" or status == "*":
            return queryset

        if status.lower() == "archived":
            status = False
        else:
            status = True

        return queryset.filter(is_active=status)


class AdminStatusFilter(filters.BaseFilterBackend):
    """
    Filter that checks for superuser or not
    """

    def filter_queryset(self, request, queryset, view):

        user_type = request.query_params.get("type", "all")

        if user_type.lower() == "all" or user_type == "*":
            return queryset

        superuser = False

        if user_type.lower() == "admin":
            superuser = True

        return queryset.filter(is_superuser=superuser)
