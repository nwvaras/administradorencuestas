# -*- coding: utf-8 -*-
import codecs
import csv
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
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
from fcm.utils import get_device_model

from encuestas.models import Survey, SendedSurvey, Subject, Message, SendedMessage, Conjunto, ConjuntosToSend, \
    DeviceEncuesta
from encuestas.validators import verificar_rut


@csrf_exempt
def get_survey(request, user):
    surveyRespList = SendedSurvey.objects.filter(respondida=False, subject__rut=user).all()
    print surveyRespList
    results = [ob.to_dict() for ob in surveyRespList]
    return JsonResponse(results, safe=False)


@csrf_exempt
def user_register(request):
    print "first"
    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    print "firstf"
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)
    print "second"
    if 'rut' in body and 'conjunto' in body and 'email' in body and 'telefono' in body and 'sexo' in body and 'nombre' in body and 'apellido' in body and 'edad' in body:

        name = body['nombre'] + " " + body['apellido']
        email = body['email']
        phone = body['telefono']
        sexo = body['sexo']
        rut = body['rut']
        verificar_rut(rut)
        conjunto = body['conjunto']
        age = body['edad']
        userExist = Subject.objects.filter(rut=rut)
        if len(userExist) > 0:
            return JsonResponse({}, status=404)
        new_user = Subject(name=name, age=age, phone=phone, email=email, rut=rut)
        new_user.save()
        new_user.conjunto.add(Conjunto.objects.get(id=conjunto['pk']))
        new_user.conjunto.add(Conjunto.objects.get(id=sexo['pk']))
        new_user.last_connection = datetime.now()
        new_user.save()
        return JsonResponse({'status': 'Ok'})
    else:
        return JsonResponse({}, status=404)


@csrf_exempt
def user_register_device(request):
    print "first"
    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    print "firstf"
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)
    print "second"
    if 'rut' in body and 'device':
        # Checkear si usuarios existe:
        rut = body.get('rut')
        device_json = body.get('device')
        user = Subject.objects.filter(rut=rut)
        if (len(user) > 0):
            # Si existe, crear un device y agregarselo al usuario
            if 'reg_id' in device_json:
                reg_id = device_json.get('reg_id')
                device = DeviceEncuesta(reg_id=reg_id, dev_id=rut, name=rut)
                user = user.first()
                device.save()
                user.device= device
                user.save()
                return JsonResponse({'status': 'Ok'})
            else:
                 return JsonResponse({}, status=404)
        else:
             return JsonResponse({}, status=404)


    else:
        return JsonResponse({}, status=404)


@csrf_exempt
def user_register_data(request):
    print "first"
    if request.method != 'GET':
        return JsonResponse({}, status=404)

    conjuntos = ConjuntosToSend.objects.exclude(conjunto__name="Mujer").exclude(conjunto__name="Hombre").all()
    dict_base = dict()
    base = []
    for i in xrange(0, len(conjuntos)):
        conjunto = conjuntos[i].conjunto
        base.append(conjunto.to_dict())
    dict_base['conjuntos'] = base
    base2 = []
    conjuntos = ConjuntosToSend.objects.filter(Q(conjunto__name='Mujer') | Q(conjunto__name='Hombre'))
    for i in xrange(0, len(conjuntos)):
        conjunto = conjuntos[i].conjunto
        base2.append(conjunto.to_dict())
    dict_base['sexo'] = base2
    return JsonResponse(dict_base)


@csrf_exempt
def user_get_data(request):
    print "first"
    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    print "firstf"
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)
    print "second"
    rut = body.get('rut', "12121")
    userExist = Subject.objects.filter(rut=rut)
    if len(userExist) == 0:
        return JsonResponse({}, status=404)
    print body
    user = userExist.first()
    user.last_connection = datetime.now()
    user.save()
    surveyRespList = SendedSurvey.objects.filter(respondida=False, subject__rut=rut).all()
    last_message = SendedMessage.objects.filter(subject__rut=rut).order_by('-date_sended')
    print surveyRespList
    results = dict()
    results['result'] = [ob.to_dict() for ob in surveyRespList]
    if len(last_message) > 0:
        results['last_message'] = last_message.first().to_dict_to_user()
    else:
        results['last_message'] = ""
    results["count"] = len(results['result'])
    return JsonResponse(results, safe=False)


def ready_survey(request, string):
    surveyResp = SendedSurvey.objects.get(pk=string)

    surveyResp.respondida = True
    surveyResp.save()

    return JsonResponse({}, safe=False)


@transaction.atomic
def upload_user_csv(request):
    print request.FILES
    if request.method == 'POST' and request.FILES:
        csvfile = request.FILES['csv']
        dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "Latin-1").read(1024))
        csvfile.open()
        reader = csv.reader(codecs.EncodedFile(csvfile, "Latin-1"), delimiter=';', dialect=dialect)
        header = next(reader, None)
        print header
        conjunto = Conjunto(name=header[1], description=header[2])
        conjunto.save()
        for row in reader:
            try:
                subject = Subject.objects.get(rut=row[0])
            except ObjectDoesNotExist:
                continue
            if row[1] == 1:
                subject.conjuntos.add(conjunto)

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
    filters = body.get('filters', {})
    age_min = filters.get('age_min', 0)
    age_max = filters.get('age_max', 99)
    conjuntos = filters.get('conjuntos', [])
    users = Subject.objects
    for c in conjuntos:
        users = users.filter(conjunto__name=c['name'])
    users = users.filter(age__range=[age_min, age_max])
    base = []
    if len(users) == 0:
        return JsonResponse({}, status=404)
    else:
        for i in xrange(0, len(users)):
            user = users[i]
            base.append(user.to_dict())
    return JsonResponse({'usuarios': base})


@csrf_exempt
def get_surveys_by_filter(request):
    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)
    filters = body.get('filters', {})
    date_creation_min = filters.get('date_creation_min', datetime(2005, 1, 30))
    date_creation_max = filters.get('date_creation_max', datetime(2025, 1, 30))
    surveys = Survey.objects
    surveys = surveys.filter(date_creation__range=[date_creation_min, date_creation_max])
    base = []
    if len(surveys) == 0:
        return JsonResponse({}, status=404)
    else:
        for i in xrange(0, len(surveys)):
            survey = surveys[i]
            base.append(survey.to_dict())
    return JsonResponse({'encuestas': base})


@csrf_exempt
def get_sended_messages_by_filter(request):
    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)
    filters = body.get('filters', {})
    date_sended_min = filters.get('date_sended_min', datetime(2005, 1, 30))
    date_sended_max = filters.get('date_sended_max', datetime(2025, 1, 30))
    messages = SendedMessage.objects
    messages = messages.filter(date_sended__range=[date_sended_min, date_sended_max])
    base = []
    if len(messages) == 0:
        return JsonResponse({}, status=404)
    else:
        for i in xrange(0, len(messages)):
            message = messages[i]
            base.append(message.to_dict())
    return JsonResponse({'mensajes': base})


@csrf_exempt
def get_messages(request):
    if request.method != 'POST':
        return JsonResponse({}, status=404)
    messages = Message.objects.all()
    base = []

    if len(messages) == 0:
        return JsonResponse({}, status=404)
    else:
        for i in xrange(0, len(messages)):
            message = messages[i]
            base.append(message.to_dict())
    return JsonResponse({'mensajes': base})


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
        usuarios = body.get('usuarios', {})
        encuesta = body.get('encuesta', {})
        for user in usuarios:
            survey = Survey.objects.get(id=encuesta['pk'])
            survey.last_sended_date = datetime.now()
            survey.save()
            sended_survey = SendedSurvey(survey_id=encuesta['pk'], subject_id=user['pk'])
            sended_survey.save()
            db_user = Subject.objects.get(id=user['pk'])
            device = db_user.device
            device.send_message({'message':'my test message'}, collapse_key='something')
    else:
        return JsonResponse({}, status=404)
    base = []
    if len(usuarios) == 0:
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({'status': 'OK'})


@csrf_exempt
@transaction.atomic
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

        encuesta = body.get('encuesta', {})
        selectedSurveys = body.get('selected', {})
        if len(selectedSurveys) == 0:
            return JsonResponse({}, status=404)
        for selectedSurvey in selectedSurveys:
            sended_surveys = SendedSurvey.objects.filter(survey_id=selectedSurvey['pk'])
            for sended in sended_surveys:
                to_send = SendedSurvey(survey_id=encuesta['pk'], subject=sended.subject)
                to_send.save()
    else:
        return JsonResponse({}, status=404)
    return JsonResponse({'status': 'OK'})


@csrf_exempt
@transaction.atomic
def create_survey_from_cp(request):
    print(request.body)
    print "je2"

    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)

    if 'encuesta' in body:

        encuesta = body.get('encuesta', {})
        date = datetime.strptime(encuesta['date'], "%a, %d %b %Y %H:%M:%S %Z")
        survey = Survey(title=encuesta['titulo'], description=encuesta['description'], url=encuesta['url'],
                        end_survey_time=date)
        survey.save()

    else:
        return JsonResponse({}, status=404)
    return JsonResponse({'status': 'OK'})


@csrf_exempt
@transaction.atomic
def create_message_from_cp(request):
    print(request.body)
    print "je2"

    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)

    if 'message' in body:
        message = body.get('message', {})
        db_message = Message(title=message['title'], description=message['description'])
        db_message.save()
        if 'users' in body:
            users = body.get('users', {})
            for user in users:
                sended_message = SendedMessage(message=db_message, subject_id=user['pk'])
                sended_message.save()
        else:
            if 'surveys' in body:
                selectedSurveys = body.get('surveys', {})
                for selectedSurvey in selectedSurveys:
                    sended_surveys = SendedSurvey.objects.filter(survey_id=selectedSurvey['pk'])
                    for sended in sended_surveys:
                        to_send = SendedMessage(message=db_message, subject=sended.subject)
                        to_send.save()
            else:
                return JsonResponse({}, status=404)



    else:
        return JsonResponse({}, status=404)
    return JsonResponse({'status': 'OK'})


def create_message(request):
    print(request.body)
    print "je2"

    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)

    if 'message' in body:
        message = body.get('message', {})
        db_message = Message(title=message['title'], description=message['description'])
        db_message.save()
    else:
        return JsonResponse({}, status=404)
    return JsonResponse({'status': 'OK'})


@transaction.atomic
def send_message(request):
    print(request.body)
    print "je2"

    if request.method != 'POST':
        return JsonResponse({}, status=404)
    body = request.body.decode('utf-8')
    try:
        body = json.loads(body)
    except ValueError:
        return JsonResponse({}, status=404)

    if 'message' in body:

        message = body.get('message')
        id = message['pk']
        if 'users' in body:
            users = body.get('users', {})

            for user in users:
                sended = user.get('survey_pk')
                if sended == -1:
                    continue
                sended_message = SendedMessage(message_id=id, subject_id=user['pk'])
                sended_message.save()
                sended_survey = SendedSurvey.objects.get(id=sended)
                sended_survey.messages.add(sended_message)
                sended_survey.save()

        else:
            return JsonResponse({}, status=404)

    else:
        return JsonResponse({}, status=404)
    return JsonResponse({'status': 'OK'})


@csrf_exempt
def get_survey_details_html(request, id):
    print "hello"
    if request.method != 'GET':
        return JsonResponse({}, status=404)
    sended_surveys = SendedSurvey.objects.filter(survey_id=id)
    survey = Survey.objects.get(id=id)
    users = Subject.objects.all()
    responded = 0
    total = 0
    base = []
    if sended_surveys.exists():
        total = sended_surveys.count()
        responded = sended_surveys.filter(respondida=True).count()

    for i in xrange(0, len(users)):
        user = users[i]
        base.append(user.to_dict_with_survey(sended_surveys))
    surveyDetails = json.dumps(
        {'surveyDetails': {'usuarios': base, 'encuesta': survey.to_dict(), 'total': total, 'responded': responded}})
    return render_to_response('survey_details.html', {'surveyDetails': surveyDetails})


@csrf_exempt
def get_message_details_html(request, id):
    print "hello"
    if request.method != 'GET':
        return JsonResponse({}, status=404)
    sended_surveys = SendedMessage.objects.filter(message_id=id)
    message = Message.objects.get(id=id)
    users = Subject.objects.all()
    responded = 0
    total = 0
    base = []
    for i in xrange(0, len(users)):
        user = users[i]
        base.append(user.to_dict_with_message(sended_surveys))
    surveyDetails = json.dumps(
        {'messageDetails': {'usuarios': base, 'message': message.to_dict(), 'total': total, 'responded': responded}})
    return render_to_response('message_details.html', {'messageDetails': surveyDetails})


@csrf_exempt
def get_conjuntos(request):
    if request.method != 'GET':
        return JsonResponse({}, status=404)

    conjuntos = Conjunto.objects.all()

    base = []
    for i in xrange(0, len(conjuntos)):
        conjunto = conjuntos[i]
        base.append(conjunto.to_dict())
    return JsonResponse({'conjuntos': base})


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
