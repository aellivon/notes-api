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
            return queryset

        if status.lower() == "archived":
            status = False
        else:
            status = True

        return queryset.filter(is_active=status)
