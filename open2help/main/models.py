from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator
import datetime

## create models here
# occupation (profession/subject area)
class Occupation(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# education/taught background
class Education(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

# interests & activities
class Interest(models.Model):
    name=models.CharField(max_length=200,null=True)

    def get_absolute_url(self):
        return reverse('filter',args=[str(self.pk)])

    def __str__(self):
        return self.name

# how did you meet us
class How_did_you_meet_us(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user;

    # create superuser with staff priviledges
    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user;

# customer users extending on base abstract user
class CustomUser(AbstractBaseUser, PermissionsMixin):
    address=models.CharField(max_length=200,null=True, blank=True)
    city=models.CharField(max_length=60,null=False, default="", blank=True)
    province=models.CharField(max_length=60,null=False, default="", blank=True)
    linkedin=models.CharField(max_length=400,null=False, default="", blank=True)
    foto = models.ImageField(upload_to='images', null=True)
    phone = models.IntegerField(null=True, blank=True)
    cp = models.IntegerField(null=False, blank=True)
    how_you_found_us = models.ForeignKey('How_did_you_meet_us',on_delete=models.SET_NULL,null=True,blank=True)
    first_name = models.CharField(max_length=40, null=False, default="", blank=True)
    last_name = models.CharField(max_length=40, null=False, default="", blank=True)

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True, default=None)

    is_staff = models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_absolute_url_deactive(self):
        return reverse('deactive_user',args=[str(self.pk)])

    class Meta:
        permissions = (("is_nantik", "Nantik admin"),
                       ("is_immune", "Immune admin"))

# mentor abstract model
class Mentor(CustomUser):
    company = models.CharField(max_length=60,null=False)
    charge = models.CharField(max_length=60,null=False)
    knowledge = models.ManyToManyField('Interest', help_text="select your fields of knowledge.")
    is_verified = models.BooleanField(default=False)

    rating = models.FloatField(null=True, default=None, validators=[MaxValueValidator(5.0)])
    num_ratings = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('mentor_detail',args=[str(self.pk)])

    def get_absolute_url_verify(self):
        return reverse('verify_mentor',args=[str(self.pk)])

    """ def get_absolute_url_2(self):
        return reverse('enviar_solicitud',args=[str(self.pk)]) """

# mentee abstract model
class Mentee(CustomUser):
    birth = models.DateField(null=True, blank=True)
    wants_to_undertake = models.BooleanField(default=False)
    company = models.CharField(max_length=60,null=True)
    charge = models.CharField(max_length=60,null=True)
    occupation = models.ForeignKey('Occupation',on_delete=models.SET_NULL,null=True,blank=True)
    interests = models.ManyToManyField('Interest', help_text="select your interests.")
    education = models.ForeignKey('Education',on_delete=models.SET_NULL,null=True,blank=True)

    def get_absolute_url(self):
        return reverse('mentee_detail',args=[str(self.pk)])

    def clean(self):
        if self.birth and self.birth > timezone.now().date():
            raise ValidationError({'birth': _('Birth date cannot be in the future.')})
        super().clean()

# petition abstract model
class Petition(models.Model):
    user_mentee = models.ForeignKey("Mentee",on_delete=models.SET_NULL,null=True,blank=True)
    user_mentor = models.ForeignKey("Mentor",on_delete=models.SET_NULL,null=True,blank=True)
    message = models.CharField(max_length=200,null=False, default="", blank=True)

    # accepted verifier
    def get_absolute_url_estado_aceptado(self):
        return reverse('estado_aceptado',args=[str(self.pk)])

    def get_absolute_url_estado_denegado(self):
        return reverse('estado_denegado',args=[str(self.pk)])

    def get_absolute_url_estado_recomendado(self):
        return reverse('estado_recomendado',args=[str(self.pk)])

    PETITION_STATUS = (
        ('a', 'Aceptado'),
        ('d', 'Denegado'),
        ('r', 'Redirigido'),
        ('p', 'Pendiente'),
    )

    state = models.CharField(max_length=1,choices=PETITION_STATUS, default="p", blank=True, help_text='Estado de la solicitud')
    # intializing Jitsi videocall (for when accepted)
    videocall_url = models.URLField(blank=True, help_text='URL para petición aceptada')

# videocall meeting
class Meeting(models.Model):
    user_mentee = models.ForeignKey("Mentee",on_delete=models.SET_NULL,null=True,blank=True)
    user_mentor = models.ForeignKey("Mentor",on_delete=models.SET_NULL,null=True,blank=True)

    day = models.DateField(help_text='Dia del evento', null=False, default=datetime.date.today)
    start_time = models.TimeField(help_text='Inicio del evento', null=False, default=datetime.datetime.now().time())
    end_time = models.TimeField(help_text='Final del evento',  null=False, default=datetime.datetime.now().time())
    title = models.TextField(help_text='Titulo del evento',  null=False, default="Evento")

    videocall_url = models.URLField(blank=True, help_text='URL para petición aceptada')
    timeslot = models.ForeignKey("TimeSlot",on_delete=models.SET_NULL,null=True,blank=True)

    """ def __str__(self):
            return self.title + " — " + self.start_time.strftime("%H:%M") + " - " + self.end_time.strftime("%H:%M") """

    def __str__(self):
        return self.title + " [VIDEOCALL]"

    # validation for values (date/time)
    def clean(self):
        super().clean()

        if self.day < datetime.date.today():
            raise ValidationError(_('El día no puede ser anterior al día actual.'))

        if self.start_time >= self.end_time:
            raise ValidationError(_('La hora de inicio debe ser antes de la hora final.'))

# events models
class Event(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateField(help_text='Dia del evento', null=False, default=datetime.date.today)
    start_time = models.TimeField(help_text='Inicio del evento', null=False, default=datetime.datetime.now().time())
    end_time = models.TimeField(help_text='Final del evento',  null=False, default=datetime.datetime.now().time())
    title = models.TextField(help_text='Titulo del evento',  null=False, default="Evento")
    notes = models.TextField(help_text='Notas del evento', null=True, blank=True)

    def __str__(self):
        return self.title + " [EVENT]"

    # validation for values (date/time)
    def clean(self):
        super().clean()

        if self.day < datetime.date.today():
            raise ValidationError(_('El día no puede ser anterior al día actual.'))

        if self.start_time >= self.end_time:
            raise ValidationError(_('La hora de inicio debe ser antes de la hora final.'))

# timeslot model
class TimeSlot(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateField(help_text='Dia del timeslot disponible', null=False, default=datetime.date.today)
    start_time = models.TimeField(help_text='Inicio del timeslot', null=False, default=datetime.datetime.now().time())
    end_time = models.TimeField(help_text='Final del timeslot',  null=False, default=datetime.datetime.now().time())
    title = models.TextField(help_text='Titulo del timeslot',  null=False, default="Timeslot")
    notes = models.TextField(help_text='Notas del timeslot', null=True, blank=True)

    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " [TIMESLOT]"

    # validation for values (date/time)
    def clean(self):
        super().clean()

        if self.day < datetime.date.today():
            raise ValidationError(_('El día no puede ser anterior al día actual.'))

        if self.start_time >= self.end_time:
            raise ValidationError(_('La hora de inicio debe ser antes de la hora final.'))