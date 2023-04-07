from datetime import datetime
from django import forms
from django.forms.fields import EmailField
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from gestionUsuarios.models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = colaborador
        fields = ('name', 'documento', 'email', 'fecha_nacimiento','phone', 'picture', 'password')
        widgets = {
            'fecha_nacimiento': DateInput(format='%Y/%m/%d', attrs={'type': 'date', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserCreationForm(forms.ModelForm):    
    email = EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirma Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = colaborador
        fields = ['name', 'documento', 'email', 'fecha_nacimiento', 'picture','password1', 'password2']
        widgets = {
            'fecha_nacimiento': DateInput(format='%Y/%m/%d', attrs={'type': 'date', 'class': 'form-control'}),
        }
        help_texts = {k: "" for k in fields}

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = colaborador
        fields = ('email', 'documento','name', 'phone', 'fecha_nacimiento', 'picture', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'Tiempo_inicial': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'Tiempo_final': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ['user','cita_cumplida']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['Tiempo_inicial'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['Tiempo_final'].input_formats = ('%Y-%m-%dT%H:%M',)

class SignupForm(forms.Form):
    documento = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Documento'}))
    contraseña = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ['colaborador']

class AddMemberFormDC(forms.ModelForm):
    class Meta:
        model = EventMemberDC
        fields = ['instructor']        

class directory(forms.ModelForm):
    class Meta:
        model = colaborador
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': DateInput(format='%Y/%m/%d', attrs={'type': 'date', 'class': 'form-control'}),
        }

class instructor_principal(ModelForm):
    class Meta:
        model = instructor
        fields = '__all__'

class instructor_informacion(ModelForm):
    class Meta:
        model = instructor_datos
        fields = '__all__'

class colaborador(ModelForm):
    class Meta:
        model = colaborador
        fields =['documento']   

class CreateClassForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(CreateClassForm,self).__init__()
        self.fields['class_name'].label='Nombre de clase'
        self.fields['section'].label='Sección'
        self.fields['class_name'].widget.attrs['placeholder']='Nombre de clase'
        self.fields['section'].widget.attrs['placeholder']='Sección'
    
    class_name = forms.CharField(max_length=100,label='Nombre de clase')
    section = forms.CharField(max_length=100,label='Sección')

class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10,label='codigo')

class CreateAssignmentForm(forms.Form):
    assignment_name = forms.CharField(max_length=50,label='Nombre')
    due_date = forms.DateField(initial=datetime.date.today(),label='Fecha entrega')
    due_time = forms.TimeField(initial=datetime.time(10,10),label='Tiempo entrega')
    instructions = forms.CharField(label='Instrucciones',widget=forms.Textarea)
    total_marks = forms.IntegerField(label='Marcas totales')

class SubmitAssignmentForm(forms.Form):
    submission_file = forms.FileField()