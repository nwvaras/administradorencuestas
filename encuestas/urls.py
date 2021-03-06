from django.conf.urls import url
from django.shortcuts import render
from requests import request

from .views import get_survey, ready_survey, get_users_by_filter, get_surveys_by_filter, get_messages, \
    send_surveys_from_cp, send_surveys_from_cp_to_survey_users, create_survey_from_cp, create_message_from_cp, \
    get_survey_details_html, get_conjuntos, get_sended_messages_by_filter, send_message, get_message_details_html, \
    create_message, user_get_data, user_register_data, user_register, upload_user_csv, user_register_device, \
    request_message, user_get_historial,ios_debug

urlpatterns = [

    url(r'^supdate/(?P<string>\w+)/$',ready_survey, name='ready_survey'),
    url(r'^subjects/$',get_users_by_filter, name='get_users_by_filter'),
    url(r'^subjects/fromcsv/$',upload_user_csv, name='upload_user_csv'),
    url(r'^surveys/send/$',send_surveys_from_cp, name='send_surveys_from_cp'),
    url(r'^surveys/create/$',create_survey_from_cp, name='create_survey_from_cp'),
    url(r'^surveys/sendFromSurvey/$',send_surveys_from_cp_to_survey_users, name='send_surveys_from_cp_to_survey_users'),
    url(r'^surveys/info/(?P<id>\d+)/$',get_survey_details_html, name='get_survey_details_html'),
    url(r'^messages/info/(?P<id>\d+)/$',get_message_details_html, name='get_message_details_html'),
    url(r'^surveys/$',get_surveys_by_filter, name='get_surveys_by_filter'),
    url(r'^conjuntos/$',get_conjuntos, name='get_conjuntos'),
    url(r'^sendedmensajes/$',get_sended_messages_by_filter, name='get_surveys_by_filter'),
    url(r'^mensajes/$',get_messages, name='get_messages'),
    url(r'^messages/create/$',create_message, name='create_message'),
    url(r'^message/send/$',send_message, name='send_message'),
    url(r'^surveys/(?P<user>\w+)/$', get_survey, name='get_survey'),
    url(r'^userGetData/$',user_get_data, name='user_get_data'),
    url(r'^userGetHistorial/$',user_get_historial, name='user_get_historial'),
    url(r'^userRegister/$',user_register, name='user_register'),
    url(r'^userRegisterData/$',user_register_data, name='user_register_data'),
    url(r'^userRegisterDevice/$',user_register_device, name='user_register_device'),
    url(r'^request/$',request_message, name='request_message'),
    url(r'^ios_debug/$',ios_debug, name='ios_debug'),

]