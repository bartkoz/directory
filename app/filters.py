from app.models import Teacher, Subject
import django_filters


class NameFilter(django_filters.FilterSet):
    teacher_filter = django_filters.CharFilter(
        method="teacher_filter_method", label="teacher last name filter"
    )
    subject_filter = django_filters.ChoiceFilter(
        choices=[(x, x) for x in Subject.objects.values_list("name", flat=True)],
        method="subject_filter_method",
        label="subject filter",
    )

    class Meta:
        model = Teacher
        fields = ["teacher_filter", "subject_filter"]

    def teacher_filter_method(self, queryset, name, value):
        return queryset.filter(last_name__istartswith=value)

    def subject_filter_method(self, queryset, name, value):
        return queryset.filter(subjects_taught__name=value)
