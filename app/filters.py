from django.db.models import Q

from app.models import Teacher
import django_filters


class NameFilter(django_filters.FilterSet):
    teacher_filter = django_filters.CharFilter(method="q_teacher_filter", label="teacher/subject filter")

    class Meta:
        model = Teacher
        fields = ["teacher_filter"]

    def q_teacher_filter(self, queryset, name, value):
        return queryset.filter(
            Q(last_name__istartswith=value) | Q(subjects_taught__name__istartswith=value)
        ).distinct()
