from rest_framework import filters


class UserDivisionFilter(filters.BaseFilterBackend):
    """
    Filter that checks if it belongs to a specific division
    """

    def filter_queryset(self, request, queryset, view):

        division = request.query_params.get("division", "*")
        if division == "*":
            return queryset
        return queryset.filter(division_set__pk=division)
