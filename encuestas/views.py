# -*- coding: utf-8 -*-
import json
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

from encuestas.models import Survey, SendedSurvey, Subject


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
    if request.method != 'POST':
        return (None, 'Request inválido.',)
    print("holi")
    body = request.body.decode('utf-8')
    print(body)
    try:
        body = json.loads(body)
        print("holi")
    except ValueError:
        print("holo")
        return JsonResponse({},safe=False)
    print("holi")
    filters = body.get('filters',{})
    age_min = filters.get('age_min',0)
    age_max = filters.get('age_max',99)
    conjuntos = filters.get('conjuntos',{})
    users = Subject.objects
    for c in conjuntos:
        print("conjuntos" + str(conjuntos))
        print c
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