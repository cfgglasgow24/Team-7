from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, ValidationError
import datetime

# Create your models here.
class Profession(models.Model):
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
    
# user manager
class CustomUserManager():
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user;

# customer users extending on base abstract user
class CustomUser():
    linkedin=models.CharField(max_length=400,null=False, default="", blank=True)
    foto = models.ImageField(upload_to='images', null=True)
    first_name = models.CharField(max_length=40, null=False, default="", blank=True)
    last_name = models.CharField(max_length=40, null=False, default="", blank=True)

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

# mentor abstract model
class Mentor(CustomUser):
    company = models.CharField(max_length=60,null=False)
    charge = models.CharField(max_length=60,null=False)
    knowledge = models.ManyToManyField('Interest', help_text="select your fields of knowledge.")

    def get_absolute_url(self):
        return reverse('mentor_detail',args=[str(self.pk)])

    def get_absolute_url_verify(self):
        return reverse('verify_mentor',args=[str(self.pk)])
    
# mentee abstract model
class Mentee(CustomUser):
    occupation = models.ForeignKey('Occupation',on_delete=models.SET_NULL,null=True,blank=True)
    interests = models.ManyToManyField('Interest', help_text="select your interests.")

    def get_absolute_url(self):
        return reverse('mentee_detail',args=[str(self.pk)])
    
# events models
class EventAbstract(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateField(help_text='Event day', null=False, default=datetime.date.today)
    start_time = models.TimeField(help_text='Event start', null=False, default=datetime.datetime.now().time())
    end_time = models.TimeField(help_text='Event end',  null=False, default=datetime.datetime.now().time())
    title = models.TextField(help_text='Event title',  null=False, default="Evento")
    notes = models.TextField(help_text='Event notes', null=True, blank=True)

    def __str__(self):
        return self.title + " [EVENT]"

    # validation for values (date/time)
    def clean(self):
        super().clean()

        if self.day < datetime.date.today():
            raise ValidationError((''))

        if self.start_time >= self.end_time:
            raise ValidationError((''))
