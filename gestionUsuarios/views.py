from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, request
from datetime import date

from datetime import datetime

from dateutil.parser import parse as date_parse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages
from django.views import generic
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import get_template, render_to_string
from django.db.models.query_utils import Q
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.core.paginator import Paginator
from termcolor import colored
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

import base64
import os
import time
import traceback
from io import BytesIO
import imageio
import matplotlib.pyplot as plt
import calendar
import requests
from .models import *
from .utils import Calendar
from .forms import *

# @permission_required('gestionPacientes.es_paciente')
"""
    CRUD:

    1.- Dispatch valida la peticion y elige un metodo HTTP
    2.- HTTP_method_not_allowed(): Retorna error si no soprta o define
    3.- options()

"""
"""
class Index(TemplateView):
    def get(self,request,*args,**kwargs):
        return render(request, 'paginas/index.html')
"""
GLOBAL_Entry = ''
fecha = datetime.date.today()
variable = 0
variable_fecha = 0
memberDC = ''
member = ''
evento_principal = ''


class Inicio(TemplateView):
    template_name = 'principal/home.html'


class Index(TemplateView):
    template_name = 'principal/index.html'


def medico_inf(request):
    model = instructor_datos.objects.all()
    paginator = Paginator(model, 10)
    pagina = request.GET.get('page') or 1
    posts = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, posts.paginator.num_pages+1)
    return render(request, 'historia/consulta/consulta_medico.html', {'base': model, 'page': posts, 'paginas': paginas, 'pagina_actual': pagina_actual})


def seleccion_paciente(request):
    global GLOBAL_Entry
    if request.method == "POST":
        GLOBAL_Entry = request.POST['Input']
        print(GLOBAL_Entry)
        return redirect('interrogatorio')
    return render(request, "historia/paciente/seleccion.html", {'global': GLOBAL_Entry})


# ----------------------------------------------------------------
# CREAR INFORMACION instructor
@login_required
class FormMedico(request.HttpRequest):
    def formulario_instructor(request):
        if request.method == 'POST':
            form = instructor_principal(request.POST)
            if form.is_valid():
                form.save()
                return redirect('instructor_datos')
        else:
            form = instructor_principal()
        return render(request, 'historia/personal/medico.html', {'form': form, "mensaje": 'OK'})


@login_required
class FormMedico_datos(request.HttpRequest):
    def formulario_instructor_datos(request):
        if request.method == 'POST':
            form = instructor_informacion(request.POST)
            if form.is_valid():
                form.save()
                return redirect('instructor_info')
        else:
            form = instructor_informacion()
        return render(request, 'historia/personal/medico_datos.html', {'form': form, "mensaje": 'OK'})


@login_required
class Create_inf_medico(request.HttpRequest):
    def crear_medico(request):
        if request.method == 'POST':
            form = instructor_principal(request.POST)
            if form.is_valid():
                form.save()
            return redirect('instructor_info')
        else:
            form = instructor_principal()
        return render(request, 'historia/crear/crear_consulta_medico.html', {'form': form})
# EDITAR INFORMACION

def editar_inf_medico(request, id):
    form = None
    error = None
    try:
        ant = instructor.objects.get(id=id)
        if request.method == 'GET':
            form = instructor_principal(instance=ant)
        else:
            form = instructor_principal(request.POST, instance=ant)
            if form.is_valid():
                form.save()
            return redirect('instructor_info')
    except ObjectDoesNotExist as e:
        error = e
    return render(request, 'historia/editar/ed_consulta_medico.html', {'form': form, 'error': error})
# ELIMINAR INFORMACION


def Eliminated_inf_medico(request, id):
    error = None
    try:
        ant = instructor.objects.get(id=id)
        if request.method == 'POST':
            ant.delete()
            return redirect('instructor_info')
    except ObjectDoesNotExist as e:
        error = e
    return render(request, 'historia/borrar/delete_consulta_medico.html', {'ant': ant, 'error': error})

class RegistrationView(CreateView):
    template_name = 'usuarios/registro.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(
            *args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url


class ProfileView(UpdateView):
    model = colaborador
    fields = ['name', 'apellidos', 'documento', 'email', 'direccion',
              'fecha_nacimiento', 'tipo_sangre', 'sexo', 'estado_civil', 'phone', 'picture']
    template_name = 'usuarios/perfil.html'

    def get_success_url(self):
        return reverse('inicio')

    def get_object(self):
        return self.request.user

# -----------------------------------------------------------------


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.date.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# ---------------------------------------------------------------


class CalendarView(LoginRequiredMixin, generic.ListView):
    global member
    global memberDC
    member = ""
    memberDC = ""
    login_url = 'signup'
    model = Event
    template_name = 'calendario/calendario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


@ login_required(login_url='signup')
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        Titulo = form.cleaned_data['Titulo']
        Descripcion = form.cleaned_data['Descripcion']
        Tiempo_inicial = form.cleaned_data['Tiempo_inicial']
        Tiempo_final = form.cleaned_data['Tiempo_final']
        Event.objects.get_or_create(
            user=request.user,
            Titulo=Titulo,
            Descripcion=Descripcion,
            Tiempo_inicial=Tiempo_inicial,
            Tiempo_final=Tiempo_final,
        )
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'calendario/eventos.html', {'form': form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ['Titulo', 'Descripcion', 'Tiempo_inicial',
              'Tiempo_final', 'cita_cumplida']
    template_name = 'calendario/eventos.html'


@ login_required(login_url='signup')
def event_delete(request, event_id):
    event_delete = Event.objects.get(id=event_id)
    event_delete.delete()
    event_delete = Event.objects.all()
    return HttpResponseRedirect(reverse('calendar'))


@ login_required(login_url='signup')
def event_details(request, event_id):
    global evento_principal
    evento_principal = event_id
    print(evento_principal)
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    eventmemberDC = EventMemberDC.objects.filter(evento=event)
    context = {
        'event': event,
        'eventmember': eventmember,
        'eventmemberDC': eventmemberDC
    }
    return render(request, 'calendario/eventos_det.html', context)


def add_eventmember(request, event_id):
    global member
    global evento_principal
    evento_principal = event_id
    print(evento_principal)
    forms = AddMemberForm()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() < 1:
                paciente = forms.cleaned_data['paciente']
                EventMember.objects.create(
                    event=event,
                    paciente=paciente
                )
                context = {
                    'event': event,
                    'eventmember': member,
                    'eventmemberDC': memberDC,
                }
                return render(request, 'calendario/eventos_det.html', context)
            else:
                messages.success(request, f'Supero el limite de inscripciones')
                context = {
                    'event': event,
                    'eventmember': member,
                    'eventmemberDC': memberDC,
                }
                return render(request, 'calendario/eventos_det.html', context)
    context = {
        'form': forms,
    }
    return render(request, 'calendario/adicion.html', context)


def add_eventdoctor(request, event_id):
    global memberDC
    global evento_principal
    evento_principal = event_id
    print(event_id)
    formsDC = AddMemberFormDC()
    if request.method == 'POST':
        formsDC = AddMemberFormDC(request.POST)
        if formsDC.is_valid():
            memberDC = EventMemberDC.objects.filter(evento=event_id)
            evento = Event.objects.get(id=event_id)
            if memberDC.count() < 1:
                medico = formsDC.cleaned_data['medico']
                EventMemberDC.objects.create(
                    evento=evento,
                    medico=medico
                )
                context = {
                    'event': evento,
                    'eventmember': member,
                    'eventmemberDC': memberDC,
                }
                return render(request, 'calendario/eventos_det.html', context)
            else:
                messages.success(request, f'Supero el limite de inscripciones')
                context = {
                    'event': evento,
                    'eventmember': member,
                    'eventmemberDC': memberDC,
                }
                return render(request, 'calendario/eventos_det.html', context)
    context = {
        'formDC': formsDC
    }
    return render(request, 'calendario/adiciondc.html', context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'calendario/eventos_del.html'


class EventMemberDeleteViewDC(generic.DeleteView):
    global memberDC
    memberDC = ""
    model = EventMemberDC
    template_name = 'calendario/eventos_del.html'
    success_url = reverse_lazy('calendar')
# ------------------------------------------------------------
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = colaborador.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "contra/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'sistelemedicinacf.herokuapp.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('password_reset_done')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="contra/reinicio_c.html", context={"password_reset_form": password_reset_form})

def signupUser(request):
    global GLOBAL_Entry
    if request.method == 'POST':
        username = request.POST['documento']
        password = request.POST['contraseña']
        user = authenticate(request, username=username, password=password)
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''
        if result['success']:
            if user is not None:
                login(request, user)
                GLOBAL_Entry = username
                print(GLOBAL_Entry)
                return redirect('inicio')
            else:
                messages.error(
                    request, 'Usuario invalido. Por favor intentalo de nuevo.')
                return redirect('login')
        else:
            messages.error(
                request, 'reCAPTCHA INVALIDO. Por favor intentalo de nuevo.')
        return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'usuarios/login.html', {'form': form})

    generic['process time'] = time.time() - start
    d['generic'] = generic
    d['med'] = medinfo

    print(colored(d, 'red'))
    return JsonResponse(d)


def app_render(request):
    print(settings.BASE_DIR)
    d = {'title': 'Visor DICOM', 'info': 'RENDER LATERAL DEL SERVIDOR DICOM'}
    return render(request, "chat/dicom.html", d)

class Error404View(TemplateView):
    template_name = "error/error_404.html"


class Custom500View(TemplateView):
    template_name = "error/error_500.html"


class Error505View(TemplateView):
    template_name = "error/error_505.html"

    @classmethod
    def as_error_view(cls):

        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r
        return view

