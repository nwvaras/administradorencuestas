# -*- coding: utf-8 -*-
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

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

from encuestas.models import Survey, SendedSurvey


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
def subir(request):
    return render(request, 'subir.html')