from django.conf.urls import url

from .views import get_survey, ready_survey, get_users_by_filter, get_surveys_by_filter, get_messages_by_filter, \
    send_surveys_from_cp, send_surveys_from_cp_to_survey_users

urlpatterns = [
    url(r'^supdate/(?P<string>\w+)/$',ready_survey, name='ready_survey'),
    url(r'^subjects/$',get_users_by_filter, name='get_users_by_filter'),
    url(r'^surveys/send/$',send_surveys_from_cp, name='send_surveys_from_cp'),
    url(r'^surveys/sendFromSurvey/$',send_surveys_from_cp_to_survey_users, name='send_surveys_from_cp_to_survey_users'),
    url(r'^surveys/$',get_surveys_by_filter, name='get_surveys_by_filter'),

    url(r'^mensajes/$',get_messages_by_filter, name='get_surveys_by_filter'),
    url(r'^surveys/(?P<user>\w+)/$', get_survey, name='get_survey'),

]