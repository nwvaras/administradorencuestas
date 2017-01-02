from django.conf.urls import url

from .views import get_survey, ready_survey, get_users_by_filter

urlpatterns = [
    url(r'^surveys/(?P<user>\w+)/$', get_survey, name='get_survey'),
    url(r'^supdate/(?P<string>\w+)/$',ready_survey, name='ready_survey'),
    url(r'^subjects/$',get_users_by_filter, name='get_users_by_filter')

]