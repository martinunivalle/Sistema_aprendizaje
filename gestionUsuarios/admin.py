from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import  *
from django.utils.html import format_html

# clase para mejorar el panel de control


class colaboradorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'apellidos',
        'documento',
        'email',
        'foto',

    )
    search_fields = ('name', 'apellidos', 'documento',)

    def foto(self, obj):
        return format_html('<img src={} width="130 height="100"/>', obj.picture.url)

class eventoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'Titulo',
        'Descripcion',
        'Tiempo_inicial',
        'Tiempo_final',
        'created_date',
        'clase_cumplida',
    )
class EventMemberAdmin(admin.ModelAdmin):
    model = EventMember
    list_display = ['id', 'colaborador', 'event']


class EventMemberAdminDC(admin.ModelAdmin):
    model = EventMemberDC
    list_display = ['id', 'instructor', 'evento']


class instructorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_instructor',
        'apellido_instructor',
        'cedula_instructor',

    )
    search_fields = ('nombre_instructor', 'cedula_instructor', 'apellido_instructor',)


class instructorAdmindatos(admin.ModelAdmin):
    list_display = (
        'id',
        'informacion_instructor',
        'especialidad_instructor',
        'direccion_instructor',
        'telefono_instructor',
        'fecha_inscripcion_instructor',

    )
    search_fields = ('instructor__cedula_instructor', 'especialidad_instructor',)
    list_filter = ('especialidad_instructor',)

admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(colaborador, colaboradorAdmin)
admin.site.register(instructor, instructorAdmin)
admin.site.register(Event, eventoAdmin)
admin.site.register(EventMember, EventMemberAdmin)
admin.site.register(EventMemberDC, EventMemberAdminDC)
admin.site.register(Classrooms)
admin.site.register(Students)
admin.site.register(Teachers)
admin.site.register(Assignments)
admin.site.register(Submissions)
