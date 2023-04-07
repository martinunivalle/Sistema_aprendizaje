from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ugettext as _
from django.utils.timesince import timesince
import datetime
# Create your models here.

class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, phone, password, **extra_fields):
        values = [email, name, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, phone, password, **extra_fields)

    def create_superuser(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, phone, password, **extra_fields)

class colaborador(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    documento = models.CharField('Documento de identidad',max_length=200,blank=False, null=False, unique=True)
    name = models.CharField('Nombre',max_length=200, blank=False, null=False)
    apellidos = models.CharField('Apellidos',max_length=200, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField('Telefono',max_length=50,blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(default='usuario.png')
    BLOOD_CHOICES = (
        ('O-', 'O-',),
        ('O+', 'O+',),
        ('A-', 'A-',),
        ('A+', 'A+',),
        ('B-', 'B-',),
        ('B+', 'B+',),
        ('AB-', 'AB-',),
        ('AB+', 'AB+',),
    )
    tipo_sangre = models.CharField(
        max_length=3,
        choices=BLOOD_CHOICES,
        blank=True,
    )
    SEX_CHOICES = (
        ('F', 'Femenino',),
        ('M', 'Masculino',),
        ('N', 'No declarado',),
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        blank=True,
    )
    CIVIL_CHOICES = (
        ('C', 'Casado',),
        ('S', 'Soltero',),
        ('D', 'Divorciado',),
        ('V', 'Viudo',),
        ('U', 'Union Libre',),
    )
    estado_civil = models.CharField(
        max_length=1,
        choices=CIVIL_CHOICES,
        blank=True,
    )
    ocupacion = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    
    objects = AccountManager()

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['name', 'phone','email']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]
    
    def __str__(self):
        return '{} NUIP={}'.format(self.name, self.documento)
   
    class Meta:
        permissions = (
            ('es_colaborador', _('Es colaborador')),
            ('es_instructor', _('Es Instructor')),
        ) 

class instructor(models.Model):
    cedula_instructor = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    nombre_instructor = models.CharField(max_length=200, blank=False, null=False)
    apellido_instructor = models.CharField(max_length=200, blank=True, null=True)

    def get_full_name(self):
        return self.nombre_instructor

    def get_short_name(self):
        return self.nombre_instructor.split()[0]

    def __str__(self):
        return '{} {} CC={}'.format(self.nombre_instructor, self.apellido_instructor, self.cedula_instructor)

class instructor_datos(models.Model):
    informacion_instructor = models.OneToOneField(
        colaborador, on_delete=models.CASCADE, blank=False, null=False)
    fecha_inscripcion_instructor = models.DateTimeField(auto_now_add=True)
    especialidad_instructor = models.CharField(max_length=200, blank=True, null=True)
    direccion_instructor = models.CharField(max_length=200, blank=True, null=True)
    telefono_instructor = models.IntegerField(blank=True, null=True)

class Event(models.Model):
    user = models.ForeignKey(colaborador, on_delete=models.CASCADE)
    Titulo = models.CharField(max_length=200, blank=True, null=True)
    Descripcion = models.TextField(blank=True, null=True)
    Tiempo_inicial = models.DateTimeField()
    Tiempo_final = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    clase_cumplida = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Titulo)

    def get_absolute_url(self):
        return reverse('event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.Titulo} </a>'

class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(colaborador, on_delete=models.CASCADE)

    class Meta:
       unique_together = ['event', 'colaborador']

class EventMemberDC(models.Model):
    evento = models.ForeignKey(Event, on_delete=models.CASCADE)
    instructor = models.ForeignKey(instructor, on_delete=models.CASCADE)

    class Meta:
       unique_together = ['evento', 'instructor']

class Classrooms(models.Model):
    classroom_name=models.CharField(max_length=100)
    section = models.CharField(max_length=100,default='Third Year')
    class_code = models.CharField(max_length = 10,default='0000000')

    def __str__(self):
        return self.classroom_name
  
class Students(models.Model):
    student_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)

class Teachers(models.Model):
    teacher_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)

class Assignments(models.Model):
    assignment_name=models.CharField(max_length=50)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)
    due_date=models.DateField()
    due_time=models.TimeField(default=datetime.time(10,10))
    posted_date=models.DateField(auto_now_add=True)
    instructions=models.TextField()
    total_marks=models.IntegerField(default=100)

    def __str__(self):
        return self.assignment_name

class Submissions(models.Model):
    assignment_id=models.ForeignKey(Assignments,on_delete=models.CASCADE)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    submitted_date=models.DateField(auto_now_add=True)
    submitted_time=models.TimeField(auto_now_add=True)
    submitted_on_time=models.BooleanField(default=True)
    marks_alloted=models.IntegerField(default=0)
    submission_file = models.FileField(upload_to='documents')
