from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from django.views.static import serve
from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from gestionUsuarios.views import RegistrationView, ProfileView
from .vistas import classs,assignments,submissions,home

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('inicio/', views.Inicio.as_view(), name='inicio'),
    path('registro/', RegistrationView.as_view(), name='registro'),
    path('perfil/', ProfileView.as_view(), name='perfil'),
    
    path('login/', views.signupUser, name='login'),
    path('logout/', LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
    path("password_reset/", views.password_reset_request, name="password_reset"),

    path('seleccion/', views.seleccion_paciente, name="seleccion"),

    path('calendario', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.create_event, name='event_new'),
    path('event/<int:event_id>',views.event_delete, name="remove"),
    path('event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    path('event/detail/<int:event_id>/',views.event_details, name='event-detail'),
    path('add_event/colaborador/<int:event_id>/',views.add_eventmember, name='add_eventmember'),
    path('add_event/doctor/<int:event_id>/',views.add_eventdoctor, name='add_eventdoctor'),
    path('event/remove/<int:pk>/',views.EventMemberDeleteView.as_view(), name="remove_event"),
    path('eventDC/remove/<int:pk>/',views.EventMemberDeleteViewDC.as_view(), name="remove_eventDC"),

    path('historia/medico/crear_medico/', views.Create_inf_medico.crear_medico, name="cr_consulta_medico"),
    path('historia/medico/editar_medico/<int:id>', views.editar_inf_medico, name="ed_consulta_medico"),
    path('historia/medico/eliminar_medico/<int:id>', views.Eliminated_inf_medico, name="eliminar_consulta_medico"),

    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),

    
    path('home/',home.home,name='home'),
    path('landing_page/',home.landing_page,name='landing_page'),
    path('class/<int:id>',classs.render_class,name='render_class'),
    path('create_assignment/<int:classroom_id>',assignments.create_assignment,name='create_assignment'),
    path('assignment_summary/<int:assignment_id>',assignments.assignment_summary,name='assignment_summary'),
    path('delete_assignment/<int:assignment_id>',assignments.delete_assignment,name='delete_assignment'),
    path('unenroll_class/<int:classroom_id>',classs.unenroll_class,name='unenroll_class'),
    path('delete_class/<int:classroom_id>',classs.delete_class,name='delete_class'),
    path('create_class_request/',classs.create_class_request,name='create_class_request'),
    path('join_class_request/',classs.join_class_request,name='join_class_request'),
    path('submit_assignment_request/<int:assignment_id>',submissions.submit_assignment_request,name='submit_assignment_request'),
    path('mark_submission_request/<int:submission_id>/<int:teacher_id>',submissions.mark_submission_request,name='mark_submission_request'),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
