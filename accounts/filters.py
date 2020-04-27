import django_filters
from accounts.models import *

# not worked on this for some difficulties
# because it seems to me kinda useless and problem faced due to write all the queries in a different py file

class orderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
