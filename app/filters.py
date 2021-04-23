from django import forms

from app.models import Teacher, Subject
import django_filters


class NameFilter(django_filters.FilterSet):
    teacher_filter = django_filters.CharFilter(
        method="teacher_filter_method", label="teacher last name filter", max_length=1
    )
    subjects_taught = django_filters.ModelMultipleChoiceFilter(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Teacher
        fields = ["teacher_filter", "subjects_taught"]

    def teacher_filter_method(self, queryset, name, value):
        return queryset.filter(last_name__istartswith=value)
