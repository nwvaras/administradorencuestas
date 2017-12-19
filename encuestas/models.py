# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from fcm.models import AbstractDevice
from encuestas.validators import verificar_rut
import pytz


class Conjunto(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        verbose_name = u"Conjunto"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def to_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'getStatus': True,
        }


class ConjuntosToSend(models.Model):
    conjunto = models.ForeignKey(to=Conjunto)
    type = models.IntegerField(default=1)

    def to_dict(self):
        return self.conjunto.to_dict()

    def __unicode__(self):
        return self.conjunto.name


class RequestDevice(models.Model):
    type = models.IntegerField()
    title = models.CharField(max_length=20)
    description = models.TextField()
    user = models.CharField(max_length=20)

    def to_dict(self):
        return self.title

    def __unicode__(self):
        return self.title


class SurveyMonkey(models.Model):
    script = models.CharField(max_length=20000)
    isAndroid = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def to_dict(self):
        return {'content': self.script}


class DeviceEncuesta(AbstractDevice):
    pass


class Subject(models.Model):
    name = models.CharField(max_length=32, default='John Doe')
    conjunto = models.ManyToManyField(to=Conjunto)
    rut = models.CharField(max_length=12, default='123456789-1', validators=[verificar_rut])
    phone = models.IntegerField(default=0)
    age = models.IntegerField(default=20)
    email = models.EmailField(blank=True, null=True)
    device = models.ForeignKey(to=DeviceEncuesta, blank=True, null=True, on_delete=models.SET_NULL)
    last_connection = models.DateTimeField(null=True)

    class Meta:
        verbose_name = u"Sujeto"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def conjuntos_dict(self):
        total = []
        for i in self.conjunto.all():
            total.append({"name": i.name})
        return total

    def getDateToIso(self, date):

        if date is not None:
            dt = date.replace(tzinfo=pytz.timezone("America/Santiago")).isoformat().split('T')
            dia = dt[0]
            hora = dt[1].split('.')[0]
            return dia + " " + hora
        else:
            return ""

    def to_dict(self):
        return {
            'pk': self.pk,
            'nombre': self.name,
            'rut': self.rut,
            'edad': self.age,
            'phone': self.phone,
            'email': self.email,
            'ultima_conexion': self.getDateToIso(self.last_connection),

            'conjuntos': self.conjuntos_dict()

        }

    def to_dict_with_survey(self, sendedsurveys):
        sendedsurvey = sendedsurveys.filter(subject_id=self.pk)
        status = False
        sended = ""
        responded = False
        tpk = -1
        if len(sendedsurvey) != 0:
            status = True
            tpk = sendedsurvey.first().pk
            sended = self.getDateToIso(sendedsurvey.first().date_creation)
            responded = sendedsurvey.first().respondida
        return {
            'pk': self.pk,
            'nombre': self.name,
            'rut': self.rut,
            'conjuntos': self.conjuntos_dict(),
            'enviada': status,
            'fecha_envio': sended,
            'responded': responded,
            'ultima_conexion': self.getDateToIso(self.last_connection),
            'survey_pk': tpk,

        }

    def to_dict_with_message(self, sendedmessages):
        sendedmessage = sendedmessages.filter(subject_id=self.pk)
        status = False
        sended = ""
        responded = False
        read = False
        if len(sendedmessage) != 0:
            status = True
            sended = self.getDateToIso(sendedmessage.first().date_sended)
            read = sendedmessage.first().read
        return {
            'pk': self.pk,
            'nombre': self.name,
            'conjuntos': self.conjuntos_dict(),
            'enviada': status,
            'leida': read,
            'fecha_envio': sended,

        }


class Message(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        verbose_name = u"Mensaje"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'pk': self.pk,
            'title': self.title,
            'description': self.description,
        }


class SendedMessage(models.Model):
    message = models.ForeignKey(to=Message)
    subject = models.ForeignKey(to=Subject)
    read = models.BooleanField(default=False)
    date_sended = models.DateTimeField(auto_now_add=True, blank=True)

    def to_dict(self):
        return {
            'pk': self.pk,
            'message': self.message.to_dict(),
            'usuario': self.subject.to_dict(),
        }

    def to_dict_to_user(self):
        return {
            'pk': self.pk,
            'message': self.message.to_dict(),
        }

    class Meta:
        verbose_name = u"Mensaje enviado"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.message.title


class Survey(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    url = models.URLField(default='www.google.cl')
    date_creation = models.DateTimeField(auto_now_add=True, blank=True)
    last_sended_date = models.DateTimeField(null=True)
    sended = models.BooleanField(default=False)
    end_survey_time = models.DateTimeField(null=True)

    class Meta:
        verbose_name = u"Encuesta"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

    def calculate_responses(self):
        sended = SendedSurvey.objects.filter(survey__pk=self.pk)
        yes_count = sended.filter(respondida=True).count()
        no_count = sended.filter(respondida=False).count()
        return (yes_count, no_count)

    def getDateToIso(self, date):
        if date is not None:
            dt = date.replace(tzinfo=pytz.timezone("America/Santiago")).isoformat().split('T')
            dia = dt[0]
            hora = dt[1].split('.')[0]
            hora = hora.split('-')[0]
            return dia + " " + hora
        else:
            return ""

    def to_dict(self):
        (yes, no) = self.calculate_responses()
        return {
            'pk': self.pk,
            'titulo': self.title,
            'description': self.description,
            'url': self.url,
            'date_creation': self.getDateToIso(self.date_creation),
            'date_end': self.getDateToIso(self.end_survey_time),
            'last_sended_date': self.getDateToIso(self.last_sended_date),
            'estado': [{
                'key': 'Si',
                'y': yes
            },
                {
                    'key': 'No',
                    'y': no
                }],

        }


class SendedSurvey(models.Model):
    survey = models.ForeignKey(to=Survey)
    subject = models.ForeignKey(to=Subject)
    respondida = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True, blank=True)
    date_responded = models.DateTimeField(null=True, blank=True)
    messages = models.ManyToManyField(to=SendedMessage)

    def getDateToIso(self, date):
        if date is not None:
            return date.replace(tzinfo=pytz.timezone("America/Santiago")).isoformat()
        else:
            return ""

    def messages_dict(self):
        total = []
        for i in self.messages.all():
            total.append({"message": i.message.to_dict(), "time": i.date_sended})
        return total

    class Meta:
        verbose_name = u"Encuesta enviada"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.survey.title

    def to_dict(self):
        return {
            'pk': self.pk,
            'respondida': self.respondida,
            'horaEnvio': self.date_creation,
            'survey': {
                'titulo': self.survey.title,
                'url': self.survey.url,
                'date_end': self.getDateToIso(self.survey.end_survey_time)
            },
            'messages': self.messages_dict()
        }


class FacebookToken(models.Model):
    user = models.ForeignKey(to=Subject)
    token = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def to_dict(self):
        return self.user.name

    def __unicode__(self):
        return self.user.name
