# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Conjunto(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        verbose_name = u"Conjunto"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=32, default='John Doe')
    conjunto = models.ManyToManyField(to=Conjunto)
    rut = models.CharField(max_length=12, default='123456789-1')
    phone = models.IntegerField(default=0)
    age = models.IntegerField(default=20)
    email = models.EmailField(blank=True, null=True)

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

    def to_dict(self):
        return {
            'pk': self.pk,
            'nombre': self.name,
            'rut': self.rut,
            'edad': self.age,
            'phone': self.phone,
            'email': self.email,

            'conjuntos': self.conjuntos_dict()

        }


class Survey(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    url = models.URLField(default='www.google.cl')
    date_creation = models.DateTimeField(auto_now_add=True, blank=True)

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

    def to_dict(self):
        (yes, no) = self.calculate_responses()
        return {
            'pk': self.pk,
            'titulo': self.title,
            'description': self.description,
            'url': self.url,
            'date_creation': self.date_creation,
            'si': yes,

            'no': no

        }


class SendedSurvey(models.Model):
    survey = models.ForeignKey(to=Survey)
    subject = models.ForeignKey(to=Subject)
    respondida = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True, blank=True)
    date_responded = models.DateTimeField(null=True, blank=True)

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
            }
        }


class Message(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        verbose_name = u"Mensaje"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class SendedMessage(models.Model):
    message = models.ForeignKey(to=Message)
    subject = models.ForeignKey(to=Subject)
    read = models.BooleanField(default=False)
    date_sended = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = u"Mensaje enviado"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.message.title
