from django.contrib.auth.forms import UserCreationForm
from .models import Mentee, Mentor, How_did_you_meet_us, Interest, Education, Occupation, Interest
from django import forms
from django.forms.models import ModelMultipleChoiceField
from django.utils.safestring import SafeText

# entries for mentor sign up form
class SignUpMentorForm(forms.Form):
    username = forms.CharField(
        label=SafeText('<i class="fas fa-user"></i> Nombre de usuario<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nombre de usuario', 
            'required': 'required',
        }),
        error_messages = {'required': 'El campo es obligatorio'}
    )
    email = forms.EmailField(
        label=SafeText('<i class="fas fa-envelope"></i> Correo electrónico<span class="asterisk">*</span>'), 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Correo electrónico', 
            'required': 'required',
        }),
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    first_name = forms.CharField(
        label=SafeText('<i class="fas fa-user"></i> Nombre<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nombre', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    last_name = forms.CharField(
        label=SafeText('<i class="fas fa-user"></i> Apellido<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Apellido', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    password1 = forms.CharField(
        label=SafeText('<i class="fas fa-lock"></i> Contraseña<span class="asterisk">*</span>'), 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    password2 = forms.CharField(
        label=SafeText('<i class="fas fa-lock"></i> Confirmar contraseña<span class="asterisk">*</span>'), 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirmar contraseña', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    address = forms.CharField(
        label=SafeText('<i class="fas fa-home"></i> Dirección'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección',
        }), 
        required=False
    )
    city = forms.CharField(
        label=SafeText('<i class="fas fa-map-marker-alt"></i> Ciudad<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ciudad', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    province = forms.CharField(
        label=SafeText('<i class="fas fa-map-marker-alt"></i> Provincia<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Provincia', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    linkedin = forms.CharField(
        label=SafeText('<i class="fab fa-linkedin"></i> Linkedin<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Linkedin',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    foto = forms.ImageField(
        label=SafeText('<i class="fas fa-camera"></i> Foto'), 
        widget=forms.FileInput(attrs={
            'class': 'formFoto form-control'
        }), 
        required = False
    )
    phone = forms.CharField(
        label=SafeText('<i class="fas fa-phone"></i> Teléfono'), 
        widget=forms.TextInput(attrs={
            'type': 'number','class': 
            'form-control', 
            'placeholder': 'Teléfono',
        }), 
        required= False, 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    cp = forms.CharField(
        label=SafeText('<i class="fas fa-map-marker-alt"></i> Código postal<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Código postal', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    company = forms.CharField(
        label=SafeText('<i class="fas fa-building"></i> Empresa<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Empresa', 
            'required': 'required',
        }), 
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    charge = forms.CharField(
        label=SafeText('<i class="fas fa-user-tie"></i> Cargo<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Cargo', 
            'required': 'required',
        }),
        error_messages = {'required' : 'El campo es obligatorio'}
    )
    how_you_found_us = forms.ModelChoiceField(
        queryset=How_did_you_meet_us.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'required': 'required',
        }),
        label=SafeText('<i class="fas fa-users"></i> ¿Cómo nos conociste?<span class="asterisk">*</span>')
    )
    knowledge = ModelMultipleChoiceField(
        queryset=Interest.objects.all(), 
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control', 
            'required': 'required',
        }),
        label=SafeText('<i class="fas fa-lightbulb"></i> ¿Qué conocimientos tienes?<span class="asterisk">*</span>')
    )

# entries for mentee sign up form
class SignUpMenteeForm(forms.Form):
    username = forms.CharField(
        label=SafeText('<i class="fas fa-user"></i> Nombre de usuario<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nombre de usuario', 
            'required': 'required'
        })
    )
    email = forms.EmailField(
        label=SafeText('<i class="fas fa-envelope"></i> Correo electrónico<span class="asterisk">*</span>'), 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Correo electrónico', 
            'required': 'required'
        })
    )
    first_name = forms.CharField(
        label=SafeText('<i class="fas fa-user"></i> Nombre<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nombre', 
            'required': 'required'
        })
    )
    last_name = forms.CharField(
        label=SafeText('<i class="fas fa-user"></i> Apellido<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Apellido', 
            'required': 'required'
        })
    )
    password1 = forms.CharField(
        label=SafeText('<i class="fas fa-lock"></i> Contraseña<span class="asterisk">*</span>'), 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña', 
            'required': 'required'
        })
    )
    password2 = forms.CharField(
        label=SafeText('<i class="fas fa-lock"></i> Confirmar contraseña<span class="asterisk">*</span>'), 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirmar contraseña', 
            'required': 'required'
        })
    )
    address = forms.CharField(
        label=SafeText('<i class="fas fa-home"></i>  Dirección'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Dirección'
        }), 
        required=False
    )
    city = forms.CharField(
        label=SafeText('<i class="fas fa-map-marker-alt"></i> Ciudad<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ciudad', 
            'required': 'required'
        })
    )
    province = forms.CharField(
        label=SafeText('<i class="fas fa-map-marker-alt"></i> Provincia<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Provincia', 
            'required': 'required'
        })
    )
    linkedin = forms.CharField(
        label=SafeText('<i class="fab fa-linkedin"></i> LinkedIn<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'LinkedIn', 
            'required': 'required'
        })
    )
    foto = forms.ImageField(
        label=SafeText('<i class="fas fa-camera"></i> Foto'), 
        widget=forms.FileInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Foto'
        }), 
        required=False
    )
    phone = forms.CharField(
        label=SafeText('<i class="fas fa-phone"></i> Teléfono'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Teléfono'
        }), 
        required= False
    )
    cp = forms.CharField(
        label=SafeText('<i class="fas fa-map-marker-alt"></i> Código postal<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Código postal', 
            'required': 'required'
        })
    )
    birth = forms.DateField(
        label=SafeText('<i class="fas fa-calendar"></i> Fecha de nacimiento<span class="asterisk">*</span>'), 
        widget=forms.DateInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Fecha de nacimiento', 
            'required': 'required', 
            'type': 'date'
        })
    )
    company = forms.CharField(
        label=SafeText('<i class="fas fa-building"></i> Empresa<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Empresa', 
            'required': 'required'
        })
    )
    charge = forms.CharField(
        label=SafeText('<i class="fas fa-user-tie"></i> Cargo<span class="asterisk">*</span>'), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Cargo', 
            'required': 'required'
        })
    )
    how_you_found_us = forms.ModelChoiceField(
        queryset=How_did_you_meet_us.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'placeholder': '¿Cómo nos has encontrado?', 
            'required': 'required'
        }),
        label=SafeText('<i class="fas fa-users"></i> ¿Cómo nos has encontrado?<span class="asterisk">*</span>')
    )
    wants_to_undertake = forms.BooleanField(
        widget=forms.CheckboxInput,
        initial=False,
        disabled=False,
        required=False,
        label=SafeText('<i class="fas fa-lightbulb"></i> ¿Quieres emprender?<span class="asterisk">*</span>')
    )
    occupation = forms.ModelChoiceField(
        queryset=Occupation.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'placeholder': 'Ocupación', 
            'required': 'required'
        }), 
        label=SafeText('<i class="fas fa-laptop-code"></i> Ocupación<span class="asterisk">*</span>')
    )
    education = forms.ModelChoiceField(
        queryset=Education.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'placeholder': 'Educación', 
            'required': 'required'
        }), 
        label =SafeText('<i class="fas fa-user-graduate"></i> Nivel educativo<span class="asterisk">*</span>')
    )
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(), 
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control', 
            'placeholder': 'Intereses', 
            'required': 'required'
        }), 
        label = SafeText('<i class="fas fa-shield-alt"></i> Intereses<span class="asterisk">*</span>')
    )

# petition for mentor form
class PetitionForm(forms.Form):
    # Hacer un campo textarea para la petición
    message = forms.CharField(
        label=SafeText('<i class="fas fa-pen"></i> Mensaje<span class="asterisk">*</span>'),
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Mensaje para el mentor', 
            'required': 'required'
        }), 
        max_length=500,
        required=True
    )

# mentor (OR) mentee event form
class EventForm(forms.Form):
    day = forms.DateField(
        label=SafeText('<i class="fas fa-calendar"></i> Fecha de evento'), 
        widget=forms.DateInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Fecha de Evento', 
            'required': 'required', 'type': 'date'
        })
    )
    start_time = forms.TimeField(
        label=SafeText("Hora de inicio"), 
        widget=forms.TimeInput(attrs={
            'class': 'form-control', 
            'placeholder': 'HH:MM', 
            'step': '300',"type":"time",},
            format='%H:%M'
        )
    )
    end_time = forms.TimeField(
        label=SafeText("Hora de finalización"), 
        widget=forms.TimeInput(attrs={
            'class': 'form-control', 
            'placeholder': 'HH:MM', 
            'step': '300',
            "type":"time",},
            format='%H:%M'
        )
    )
    title = forms.CharField(
        label=SafeText("Titulo"), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Titulo', 
            'required': 'required'
        })
    )
    note = forms.CharField(
        label=SafeText("Descripcion"), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Descripcion', 
            'required': 'required'}
        )
    )

# mentor <> mentee timeslot form
class TimeSlotForm(forms.Form):
    day = forms.DateField(
        label=SafeText('<i class="fas fa-calendar"></i> Fecha de Timeslot'), 
        widget=forms.DateInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Fecha de Timeslot', 
            'required': 'required', 'type': 'date'
        })
    )
    start_time = forms.TimeField(
        label=SafeText("Hora de inicio"), 
        widget=forms.TimeInput(attrs={
            'class': 'form-control', 
            'placeholder': 'HH:MM', 
            'step': '300',"type":"time",},
            format='%H:%M'
        )
    )
    end_time = forms.TimeField(
        label=SafeText("Hora de finalización"), 
        widget=forms.TimeInput(attrs={
            'class': 'form-control', 
            'placeholder': 'HH:MM', 
            'step': '300',
            "type":"time",},
            format='%H:%M'
        )
    )
    title = forms.CharField(
        label=SafeText("Titulo"), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Titulo', 
            'required': 'required'
        })
    )
    note = forms.CharField(
        label=SafeText("Descripcion"), 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Descripcion', 
            'required': 'required'}
        )
    )
