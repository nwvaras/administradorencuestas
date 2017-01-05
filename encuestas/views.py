# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

#
#
# def index(request):
#     return render(request, 'index.html')
#
#
# def lista(request):
#     return render(request, 'lista.html')
#
#
# @ensure_csrf_cookie
# def subir(request):
#     return render(request, 'subir.html')
#
#
# def acta_base(request):
#
#     config = obtener_config()
#
#     acta = {
#         'min_participantes': config['participantes_min'],
#         'max_participantes': config['participantes_max'],
#         'geo': {},
#         'participantes': [{} for _ in range(config['participantes_min'])]
#     }
#
#     acta['itemsGroups'] = [g.to_dict() for g in GrupoItems.objects.all().order_by('orden')]
#
#     return JsonResponse(acta)
#
#
# @transaction.atomic
# def subir_validar(request):
#     acta, errores = validar_acta_json(request)
#
#     if len(errores) > 0:
#         return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)
#
#     return JsonResponse({'status': 'success', 'mensajes': ['El acta ha sido validada exitosamente.']})
#
#
# @transaction.atomic
# def subir_confirmar(request):
#     acta, errores = validar_acta_json(request)
#
#     if len(errores) > 0:
#         return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)
#
#     errores = validar_cedulas_participantes(acta)
#
#     if len(errores) == 0:
#         guardar_acta(acta)
#         return JsonResponse({'status': 'success', 'mensajes': ['El acta ha sido ingresada exitosamente.']})
#
#     return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)

from encuestas.models import Survey, SendedSurvey, Subject, Message, SendedMessage


def get_survey(request, user):
    surveyRespList = SendedSurvey.objects.filter(respondida=False,subject__rut=user).all()
    print surveyRespList
    results = [ob.to_dict() for ob in surveyRespList]
    return JsonResponse(results, safe=False)

def ready_survey(request, string):
    surveyResp = SendedSurvey.objects.get(pk=string)

    surveyResp.respondida = True
    surveyResp.save()

    return JsonResponse({}, safe=False)

@csrf_exempt
def get_users_by_filter(request):
    print("asd2")
    print request.body
    if request.method != 'POST':
         return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
         return JsonResponse({}, status=404)
    filters = body.get('filters',{})
    age_min = filters.get('age_min',0)
    age_max = filters.get('age_max',99)
    conjuntos = filters.get('conjuntos',[])
    users = Subject.objects
    for c in conjuntos:
        users= users.filter(conjunto__name=c['name'])
    users=users.filter(age__range=[age_min,age_max])
    base =[]
    if len(users) == 0:
        return JsonResponse({}, status=404)
    else:
        for i in xrange(0,len(users)):
            user = users[i]
            base.append(user.to_dict())
    return JsonResponse({'usuarios' : base})

@csrf_exempt
def get_surveys_by_filter(request):

    if request.method != 'POST':
         return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
         return JsonResponse({}, status=404)
    filters = body.get('filters',{})
    date_creation_min = filters.get('date_creation_min',datetime(2005, 1, 30))
    date_creation_max = filters.get('date_creation_max',datetime(2025, 1, 30))
    surveys = Survey.objects
    surveys=surveys.filter(date_creation__range=[date_creation_min,date_creation_max])
    base =[]
    if len(surveys) == 0:
        return JsonResponse({}, status=404)
    else:
        for i in xrange(0,len(surveys)):
            survey = surveys[i]
            base.append(survey.to_dict())
    return JsonResponse({'encuestas' : base})
@csrf_exempt
def get_messages_by_filter(request):
    if request.method != 'POST':
         return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
         return JsonResponse({}, status=404)
    filters = body.get('filters',{})
    date_sended_min = filters.get('date_sended_min',datetime(2005, 1, 30))
    date_sended_max = filters.get('date_sended_max',datetime(2025, 1, 30))
    messages = SendedMessage.objects
    messages=messages.filter(date_sended__range=[date_sended_min,date_sended_max])
    base =[]
    if len(messages) == 0:
        return JsonResponse({}, status=404)
    else:
        for i in xrange(0,len(messages)):
            message = messages[i]
            base.append(message.to_dict())
    return JsonResponse({'mensajes' : base})

@csrf_exempt
def send_surveys_from_cp(request):
    print("asd")
    print(request.body)
    print("asd")
    if request.method != 'POST':
         return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
         return JsonResponse({}, status=404)

    if 'encuesta' in body and 'usuarios' in body:
        usuarios= body.get('usuarios',{})
        encuesta = body.get('encuesta',{})
        for user in usuarios:
            sended_survey = SendedSurvey(survey_id=encuesta['pk'],subject_id=user['pk'])
            sended_survey.save()
    else:
        return JsonResponse({}, status=404)
    base =[]
    if len(usuarios) == 0:
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({'status' : 'OK'})
@csrf_exempt
def send_surveys_from_cp_to_survey_users(request):

    print(request.body)
    print "je"

    if request.method != 'POST':
         return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
         return JsonResponse({}, status=404)

    if 'encuesta' in body and 'selected' in body:

        encuesta = body.get('encuesta',{})
        selectedSurveys = body.get('selected',{})
        for selectedSurvey in selectedSurveys:
            sended_surveys = SendedSurvey.objects.filter(survey_id=selectedSurvey['pk'])
            for sended in sended_surveys:
                to_send = SendedSurvey(survey_id=encuesta['pk'],subject=sended.subject)
                to_send.save()
    else:
        return JsonResponse({}, status=404)
    return JsonResponse({'status' : 'OK'})



@login_required
def survey_menu(request):
    return render(request, 'survey_table.html')
@login_required
def graph_viewer(request):
    return render(request, 'graph_viewer.html')
@login_required
def subject_menu(request):
    return render(request, 'subject_table.html')
@login_required
def message_record(request):
    return render(request, 'message_table.html')