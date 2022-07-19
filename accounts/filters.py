import django_filters
from django_filters import CharFilter




# class course_filter_form(django_filters.FilterSet):
#     course_name=CharFilter(field_name='course_name',lookup_expr='icontains',label="Search")
#     class Meta:
#           model=Courses
#           fields=(
#          'course_name',
#           )