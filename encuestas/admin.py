from django.shortcuts import render
from encuestas.models import Conjunto, Subject, Survey, SendedSurvey, Message, SendedMessage, ConjuntosToSend, \
    RequestDevice,FacebookToken, SurveyMonkey
from django.contrib import admin
from encuestas.views import subject_menu, survey_menu, message_record


def create_action_for_subject_message(message):
    def action(modeladmin, request, queryset):
     for obj in queryset:
        sended_message = SendedMessage(message=message,subject=obj)
        sended_message.save()

    name = "MENSAJE: Enviar " + message.title
    return (name, (action, name, name))


def create_action_for_subject_survey(survey):
    def action(modeladmin, request, queryset):
     for obj in queryset:
        sended_survey = SendedSurvey(survey=survey,subject=obj)
        sended_survey.save()
    name = "ENCUESTA: Enviar " + survey.title
    return (name, (action, name, name))

def create_action_for_sended_survey_message(message):
    def action(modeladmin, request, queryset):
     for obj in queryset:
        sended_message = SendedMessage(message=message,subject=obj.subject)
        sended_message.save()

    name = "MENSAJE: Enviar " + message.title
    return (name, (action, name, name))


def create_action_for_sended_survey_survey(survey):
    def action(modeladmin, request, queryset):
        for obj in queryset:
            sended_survey = SendedSurvey(survey=survey,subject=obj.subject)
            sended_survey.save()

    name = "ENCUESTA: Enviar " + survey.title
    return (name, (action, name, name))



class ConjuntoAdmin(admin.ModelAdmin):
    # list_display = ('name', 'description')
    # list_display_links = ('name',)

    search_fields = ['name', 'description']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'conjuntos', 'rut', 'phone', 'age']
    list_display_links = ['name', 'conjuntos', 'rut', 'phone', 'age']
    list_filter = ['conjunto', 'age']
    search_fields = ['name', 'conjunto__name']

    def conjuntos(self, obj):
        return ",".join([p.name for p in obj.conjunto.all()])

    def get_actions(self, request):
        x = dict(create_action_for_subject_message(q) for q in Message.objects.all())
        y = dict(create_action_for_subject_survey(x) for x in Survey.objects.all())
        return dict(x, **y)
        # messages = Message.admin.ModelAdmins.filter()[:3]
        # print("test")
        #
        # actions = [action_send_message(q) for q in Message.admin.ModelAdmins.all()]
        #
        # def save_model(self, request, obj, form, change):
        #     print("asdasd")
        #
        # for x in messages:
        #     actions.append(action_send_message(x))
        # surveys = Survey.admin.ModelAdmins.filter()[:3]
        # for x in surveys:
        #     actions.append(action_send_survey(x))


class SurveyAdmin(admin.ModelAdmin):
    ##list_display = ('title', 'description', 'url', 'date_creation')
    # list_display_links = ('titulo', 'description', 'url', 'fecha_creacion')
    list_filter = ['date_creation']
    search_fields = ['title']
    readonly_fields = ['last_connection']


class SendedSurveyAdmin(admin.ModelAdmin):
   pass


class MessageAdmin(admin.ModelAdmin):
    ##list_display = ('title', 'description')
    # list_display_links = ('title')
    search_fields = ['title']


class SendedMessageAdmin(admin.ModelAdmin):
    # list_display = ['message', 'subject', 'date_sended', 'read']
    # list_display_links = ['message', 'subject', 'date_sended', 'read']
    # list_filter = ['read']
    # search_fields = ['message__title']
    pass
class MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
class MySubjectAdmin(MyModelAdmin):
    readonly_fields= ('last_connection',)

class MySurveyAdmin(MyModelAdmin):
    readonly_fields= ('last_sended_date',)



# admin.site.register(Message, MyModelAdmin)
admin.site.register_view('personas' ,'Menu Personas', view=subject_menu,)
admin.site.register_view('encuestas','Menu Encuestas', view=survey_menu)
admin.site.register_view('mensajes','Historial de Mensajes', view=message_record)
# admin.site.register(Conjunto,ConjuntoAdmin)
# admin.site.register(Subject,SubjectAdmin)
# admin.site.register(Survey,SurveyAdmin)
# admin.site.register(SendedSurvey,SendedSurvey)
# admin.site.register(Message,MessageAdmin)
# admin.site.register(SendedMessage,SendedMessageAdmin)
admin.site.register(Conjunto,MyModelAdmin)
admin.site.register(SurveyMonkey,MyModelAdmin)
admin.site.register(Subject,MySubjectAdmin)
admin.site.register(Survey,MySurveyAdmin)
admin.site.register(SendedSurvey,MyModelAdmin)
admin.site.register(Message,MyModelAdmin)
admin.site.register(SendedMessage,MyModelAdmin)
admin.site.register(ConjuntosToSend,MyModelAdmin)
admin.site.register(FacebookToken,MyModelAdmin)
admin.site.register(RequestDevice)
