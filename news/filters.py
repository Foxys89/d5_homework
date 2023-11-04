from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter
from django.forms import DateInput
from .models import Post, Category


class PostFilter(FilterSet):
    post_time = DateFilter(
        field_name = 'post_time',
        label = 'Дата (позже)',
        lookup_expr = 'gt',
        widget = DateInput(
            attrs = {
                'type': 'date',
            }
        ),
    )

    category = ModelMultipleChoiceFilter(
    field_name = 'post_category',
    queryset = Category.objects.all(),
    label = 'Категория',
    conjoined = True
    )

    class Meta:
        model = Post
        fields = {
            'post_name' : ['icontains'],
        }