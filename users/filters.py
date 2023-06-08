from rest_framework import filters


class UserDivisionFilter(filters.BaseFilterBackend):
    """
    Filter that checks if it belongs to a specific division
    """

    def filter_queryset(self, request, queryset, view):

        division = request.query_params.get("division", "*")
        if division == "*" or not division:
            return queryset
        return queryset.filter(division_set__pk=division)


class StringUserStatusFilter(filters.BaseFilterBackend):
    """
    Filter that checks if it belongs to a specific division
    """

    def filter_queryset(self, request, queryset, view):

        status = request.query_params.get("status", True)

        if status.lower() == "all" or status == "*":
            print("aall")
            return queryset

        if status.lower() == "archived":
            status = False
        else:
            print("Truee")
            status = True

        return queryset.filter(is_active=status)


class AdminStatusFilter(filters.BaseFilterBackend):
    """
    Filter that checks if it belongs to a specific division
    """

    def filter_queryset(self, request, queryset, view):

        user_type = request.query_params.get("type", True)

        if user_type.lower() == "all" or user_type == "*":
            return queryset

        superuser = False

        if user_type.lower() == "admin":
            superuser = True

        return queryset.filter(is_superuser=superuser)
