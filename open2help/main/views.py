# utils
from django.shortcuts import render,redirect
import datetime

# Django forms
from .forms import SignUpMentorForm, SignUpMenteeForm, PetitionForm,EventForm, TimeSlotForm

# Django models
from .models import Mentor, How_did_you_meet_us, Interest, Mentee, Education, Petition,  Event, Meeting, CustomUser, TimeSlot

# Django misc
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from django.template import Context, loader
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

# URL parsing decoding
from urllib.parse import unquote

# error handling
from django.db import IntegrityError

# Jitsi API
from .videocall import create_instant_call

# create views here
def index(request):
    """Summary line

    creates main views built on base_generic.html

    Args:
        request (HttpRequest): Http request for Django type

    Returns: 
        HttpResponse: rendering index.html

    """

    # redirect to 
    if(request.user.has_perm('main.is_nantik')):
        return redirect("nantik")
    elif(request.user.has_perm('main.is_immune')):
        return redirect("immune")

    if (request.user.is_authenticated):
        userId = request.user.pk
        eventList = Event.objects.filter(user__exact=userId)

        mentor = None
        mentors = None
        solicitudes = []
        timeslotList = []
        mentor_timeslots = []
        meetingList = []

        try:
            mentor = Mentor.objects.get(pk=userId)
            mentors = Mentor.objects.all()

            for timeslot in TimeSlot.objects.filter(user__exact=userId):
                timeslotList.append(timeslot)

            for solicitud in Petition.objects.filter(user_mentor = mentor):
                solicitudes.append(solicitud)

            # meetingList for mentor
            meetingList = Meeting.objects.filter(user_mentor=userId)

        except:
            # if user (pass for mentor statement, extract all petitions)
            mentee  = Mentee.objects.get(pk=userId)

            for solicitud in Petition.objects.filter(user_mentee = mentee):
                solicitudes.append(solicitud)

            
            for solicitud in solicitudes:
                mentor_timeslots.append(TimeSlot.objects.filter(user=solicitud.user_mentor).order_by('day').distinct())

            # meetingList for mentees
            meetingList = Meeting.objects.filter(user_mentee=userId)

            """
            NOTICE:
            - By flattening list of querysets, you are grabbing each petition, regardless of the mentor,
            and adding it to a specific petition. This is fine as long as the mentee only has one petition at a time
            - For future development, where mentees can have multiple mentors, create a key-pair mapping where 
            each timeslot list for each petition is identified by a mentor to avoid multiple different timeslot displays
            """
            mentor_timeslots = TimeSlot.objects.none().union(*mentor_timeslots)

        context = {
            "eventList" : eventList,
            "timeslotList": timeslotList,
            'solicitudes': solicitudes,
            'mentorTimeslots': mentor_timeslots,
            'meetingList': meetingList,
            'mentor':mentor,
            'mentors': mentors,
        }
    else:
        # creates empty context
        context = {
        }

    return render(request, "index.html", context)

@permission_required("main.is_nantik")
def nantik_administration(request):
    """Summary line

    renders Nantik administration view for mentor verification; requires
    permission for Nantik main view

    Args:
        request (HttpRequest): Http request for Django type

    Returns:
        HttpResponse: rendering nantik_administration.html

    """

    users = []
    
    for i in Mentor.objects.all():
        users.append(i)
        
    context = {"users": users}
        
    return render(request, "nantik_administration.html", context)

@permission_required("main.is_immune") 
def immune_administration(request):
    """Summary line

    renders Immune administration view for mentor disabling

    Args:
        request (HttpRequest): Http request for Django type

    Returns:
        HttpResponse: rendering immune_administration.html

    """

    users = []
    
    for i in Mentor.objects.all():
        users.append(i)
        
    for i in Mentee.objects.all():
        users.append(i)
        
    context = {"users":users}
        
    return render(request, "immune_administration.html", context)

@permission_required("main.is_immune")
def deactive_user(request, pk):
    """Summary line

    deactivates user, requires adminitrator permission

    Args:
        request (HttpRequest): Http request for Django type
        pk (int): primary key for customuser or subclass Mentor/Mentee

    Returns:
        HttpResponse: redirects (renders) to immune administration after deactivating user

    """

    try:
        user= Mentor.objects.get(pk=pk)
    except:
        user= Mentee.objects.get(pk=pk)
    user.is_active=False
    user.save()
    return redirect("immune")

@permission_required("main.is_nantik")
def verify_mentor(request, pk):
    """Summary line

    verify mentor; required nantik moderator permission

    Args:
        request (HttpRequest): Http request for Django type
        pk (int): primary key for Mentor when verifying (modifies is_verified attribute)

    Returns:
        HttpResponse: redirects (renders) to Nantik administration after verifying mentor

    """

    user = Mentor.objects.get(pk=pk)
    user.is_verified=True
    user.is_active = True
    user.save()
    return redirect("nantik")

# registering mentor using sign up; gets form from Django and writes to model attributes
def register_mentor(request):
    """Summary line

    reads mentor register form, cleans data
    sends mentor email for verification and data privacy form

    Args:
        request (HttpRequest): Http request for Django type

    Returns:
        HttpResponse: redirects to same page with context including error messages

    """

    form = SignUpMentorForm()

    sent = False
    err_list = []

    if request.method == "POST":
        form = SignUpMentorForm(request.POST, request.FILES)

        # if form created correctly
        if form.is_valid():
            try:
                # create mentor
                mentor = Mentor()

                if not form.data["username"]:
                    err_list.append("Por favor, introduzca un nombre de usuario.")
                if not form.data["email"]:
                    err_list.append("Por favor, introduzca una dirección de correo electrónico.")
                if not form.data["first_name"]:
                    err_list.append("Por favor, introduzca su nombre.")
                if not form.data["last_name"]:
                    err_list.append("Por favor, introduzca sus apellido/s.")
                if not form.data["password1"]:
                    err_list.append("Por favor, introduzca una contraseña.")
                if not form.data["password2"] or form.cleaned_data["password1"] != form.cleaned_data["password2"]:
                    err_list.append("Las contraseñas no coinciden.")
                if not form.data["city"]:
                    err_list.append("Por favor, introduzca su ciudad.")
                if not form.data["province"]:
                    err_list.append("Por favor, introduzca su provincia.")
                if not form.data["linkedin"]:
                    err_list.append("Por favor, introduzca la URL de su perfil de LinkedIn.")
                if not form.data["cp"]:
                    err_list.append("Por favor, introduzca su código postal.")
                if not form.data["company"]:
                    err_list.append("Por favor, introduzca el nombre de su empresa.")
                if not form.data["charge"]:
                    err_list.append("Por favor, introduzca su puesto o cargo.")
                if not form.data["how_you_found_us"]:
                    err_list.append("Por favor, seleccione cómo nos ha conocido.")
                if not form.data["knowledge"]:
                    err_list.append("Por favor, seleccione un conocimiento.")

                mentor.username = form.cleaned_data["username"]
                mentor.email = form.cleaned_data["email"]
                mentor.first_name = form.cleaned_data["first_name"]
                mentor.last_name = form.cleaned_data["last_name"]
                mentor.set_password(form.cleaned_data["password1"])

                # default address to None if not provided (optional field)
                if not form.data["address"]:
                    mentor.address = None
                else:
                    mentor.address = form.cleaned_data["address"]

                mentor.city = form.cleaned_data["city"]
                mentor.province = form.cleaned_data["province"]
                mentor.linkedin = form.cleaned_data["linkedin"]

                # optional foto
                try:
                    if not form.data["foto"]:
                        mentor.foto = "images/anonymous_pfp.jpg"
                except:
                    mentor.foto = form.cleaned_data["foto"]

                # optional phone number
                if not form.data["phone"]:
                    mentor.phone = None
                else:
                    mentor.phone = form.cleaned_data["phone"]

                mentor.cp = form.cleaned_data["cp"]
                mentor.how_you_found_us = How_did_you_meet_us.objects.get(name = form.cleaned_data["how_you_found_us"])
                mentor.company = form.cleaned_data["company"]
                mentor.charge = form.cleaned_data["charge"]
                mentor.is_active = False
                mentor.is_verified = False

                # save current mentor profile status
                mentor.save()

                for element in form.cleaned_data["knowledge"]:
                    print(element)
                    mentor.knowledge.add(Interest.objects.get(name = element))

                mentor.save()
                form = SignUpMentorForm()
                messages.success(request, "La operación se ha realizado con éxito.")
                
                context = { 'username': mentor.username }
                msg_html = render_to_string('mentor.html', context)

                send_mail(
                    settings.EMAIL_MENTOR_SUBJECT,
                    "",
                    "",
                    [mentor.email],
                    html_message=msg_html,
                    fail_silently=False,
                )
                
                # redirects to login if no errors messages (correct entires for reigster form)
                return redirect("login")
                
            except Exception as e:
                if "email" in str(e) and e.args[0] == 1062:
                    err_list.append("La dirección de correo electrónico ya esta registrado.")
                elif "username" in str(e) and e.args[0] == 1062:
                    err_list.append("El nombre de usuario ya esta registrado.")
                else:
                    err_list.append(str(e))

        else:
            err_list.append("Error, form no valid")
    else:
        form = SignUpMentorForm()

    context = {
        "form": form,
        "messageExists": sent,
        "errors": err_list or None
    }
    
    return render(request, "registration/register_mentor.html", context = context)

def register_mentee(request):
    """Summary line

    reads mentee register form, cleans data
    sends mentee email for verification and data privacy form

    Args:
        request (HttpRequest): Http request for Django type

    Returns:
        HttpResponse: redirects to same page with context including error messages

    """

    form = SignUpMenteeForm()

    sent = False
    err_list = []

    if request.method == "POST":
        form = SignUpMenteeForm(request.POST, request.FILES)

        # if form created correctly
        if form.is_valid():
            try:
                # create mentee
                mentee = Mentee()

                if not form.data["username"]:
                    err_list.append("Por favor, introduzca un nombre de usuario.")
                if not form.data["email"]:
                    err_list.append("Por favor, introduzca una dirección de correo electrónico.")
                if not form.data["first_name"]:
                    err_list.append("Por favor, introduzca su nombre.")
                if not form.data["last_name"]:
                    err_list.append("Por favor, introduzca sus apellido/s.")
                if not form.data["password1"]:
                    err_list.append("Por favor, introduzca una contraseña.")
                if not form.data["password2"] or form.cleaned_data["password1"] != form.cleaned_data["password2"]:
                    err_list.append("Las contraseñas no coinciden.")
                if not form.data["city"]:
                    err_list.append("Por favor, introduzca su ciudad.")
                if not form.data["province"]:
                    err_list.append("Por favor, introduzca su provincia.")
                if not form.data["linkedin"]:
                    err_list.append("Por favor, introduzca la URL de su perfil de LinkedIn.")
                if not form.data["cp"]:
                    err_list.append("Por favor, introduzca su código postal.")
                if not form.data["birth"]:
                    err_list.append("Por favor, introduzca su fecha de nacimiento.")
                if not form.data["company"]:
                    err_list.append("Por favor, introduzca el nombre de su empresa.")
                if not form.data["charge"]:
                    err_list.append("Por favor, introduzca su puesto o cargo.")
                if not form.data["how_you_found_us"]:
                    err_list.append("Por favor, selecciona cómo nos ha conocido.")
                if not form.data["wants_to_undertake"]:
                    err_list.append("Por favor, selecciona lo que te gustaría emprender.")
                if not form.data["occupation"]:
                    err_list.append("Por favor, selecciona su ocupación.")
                if not form.data["education"]:
                    err_list.append("Por favor, selecciona su nivel educativo.")
                if not form.data["interests"]:
                    err_list.append("Por favor, selecciona un interés.")

                mentee.username = form.cleaned_data["username"]
                mentee.email = form.cleaned_data["email"]
                mentee.first_name = form.cleaned_data["first_name"]
                mentee.last_name = form.cleaned_data["last_name"]
                mentee.set_password(form.cleaned_data["password1"])

                if not form.data["address"]:
                    mentee.address = None
                else:
                    mentee.address = form.cleaned_data["address"]

                mentee.city = form.cleaned_data["city"]
                mentee.province = form.cleaned_data["province"]
                mentee.linkedin = form.cleaned_data["linkedin"]

                try:
                    if not form.data["foto"]:
                        mentee.foto = "images/anonymous_pfp.jpg"
                except:
                    mentee.foto = form.cleaned_data["foto"]

                if not form.data["phone"]:
                    mentee.phone = None
                else:
                    mentee.phone = form.cleaned_data["phone"]

                mentee.cp = form.cleaned_data["cp"]
                mentee.how_you_found_us = How_did_you_meet_us.objects.get(name = form.cleaned_data["how_you_found_us"])
                mentee.birth = form.cleaned_data["birth"]
                mentee.wants_to_undertake = form.cleaned_data["wants_to_undertake"]
                mentee.company = form.cleaned_data["company"]
                mentee.charge = form.cleaned_data["charge"]
                mentee.occupation = form.cleaned_data["occupation"]
                mentee.education = Education.objects.get(name = form.cleaned_data["education"])
                mentee.save()

                for element in form.cleaned_data["interests"]:
                    mentee.interests.add(Interest.objects.get(name = element))
                mentee.save()

                form = SignUpMenteeForm()
                messages.success(request, "La operación se ha realizado con éxito.")

                context = { 'username': mentee.username }
                msg_html = render_to_string('mentees.html', context)

                send_mail(
                    settings.EMAIL_MENTEE_SUBJECT,
                    "",
                    "",
                    [mentee.email],
                    html_message=msg_html,
                    fail_silently=False,
                )

                # redirects to login if no errors messages (correct entires for reigster form)
                return redirect("login")

            except (IntegrityError, Exception) as e:
                if "email" in str(e) and e.args[0] == 1062:
                    err_list.append("La dirección de correo electrónico ya esta registrado.")
                elif "username" in str(e) and e.args[0] == 1062:
                    err_list.append("El nombre de usuario ya esta registrado.")
                else:
                    err_list.append(str(e))

        else:
            err_list.append("Error, form no valid")
    else:
        form = SignUpMenteeForm()

    context = {
        "form": form,
        "messageExists": sent,
        "errors": err_list or None
    }

    return render(request, "registration/register_mentee.html", context=context)

@login_required
def perfil(request):
    """Summary line

    profile view for mentor/mentee profile

    Args:
        request (HttpRequest): Http request for Django type

    Returns:
        HttpResponse: directs to profile view for mentee and mentor

    """

    context = {
    }

    return render(request, "perfil.html", context)

@login_required
def filter(request):
    """Summary line

    filters mentors by request queries (i.e., conocimientos)

    Args:
        request (HttpRequest): Http request for Django type

    Returns:
        HttpResponse: redirects back to filter.html but with updated query results

    """

    areas = []
    results = []
    applied = []
    
    for i in Interest.objects.all():
        areas.append(i)
        
    if request.method == "POST":
        filters = request.POST
       
        for i in Interest.objects.all():
            if filters.get(i.name):
                applied.append(i)
                for j in Mentor.objects.filter(knowledge__exact=i):
                    results.append(j)
                
    if not applied:
        for i in Mentor.objects.all():
            results.append(i)

    context = {
        "applied":applied,
        "areas":areas,
        "results":results,
    }
    
    return render(request, "filter.html", context = context)

@login_required
def calendar(request):
    """Summary line

    singular calendar view for mentor and mentee
    integrates FullCalendar

    Args:
        request (HttpRequest): Http request for Django type

    Returns:
        HttpResponse: redirects to calendar.html

    """

    userId = request.user.pk
    eventList = Event.objects.filter(user__exact=userId)
    timeslotList = []

    try:
        # sanity check to crash for mentor check rather than timeslots
        mentor = Mentor.objects.get(pk=request.user.pk)

        for timeslot in TimeSlot.objects.filter(user__exact=userId):
            timeslotList.append(timeslot)
    except:
        pass

    context = {
        "eventList" : eventList,
        "timeslotList": timeslotList,
    }

    return render(request, "calendar.html", context=context)

def mentor_detail(request, pk):
    mentor = Mentor.objects.get(pk=pk)
    
    context = {
        "mentor": mentor,
    }

    # renders mentor details
    return render(request, "mentor_detail.html", context = context)

def mentee_detail(request, pk):
    mentee = Mentee.objects.get(pk=pk)
    
    context = {
        "mentee": mentee,
    }

    # renders mentor details
    return render(request, "mentee_detail.html", context = context)

@login_required
def perfil_mentee(request):
    mentee=Mentee.objects.get(pk=request.user.pk)

    # instantiates context
    context = {
        'mentee': mentee,
    }

    # renders mentee profile
    return render(request, "perfil_mentee.html", context)

@login_required
def perfil_mentor(request):
    mentor = Mentor.objects.get(pk=request.user.pk)

    # instantiates context
    context = {
        'mentor': mentor,
    }

    # renders mentor profile with designated context
    return render(request,"perfil_mentor.html", context)

@login_required
def solicitudes_mentor(request):
    mentor = Mentor.objects.get(pk=request.user.pk)
    mentors = Mentor.objects.all()

    solicitudes = []
    for solicitud in Petition.objects.filter(user_mentor = mentor):
        solicitudes.append(solicitud)

    # instantiates context
    context = {
        'mentor': mentor,
        'solicitudes': solicitudes,
        'mentors': mentors,
    }

    # renders mentor profile with designated context
    return render(request,"solicitudes_mentor.html", context)

def estado_aceptado(request,pk):
    """
    Accepted status: update 
    """

    petition = Petition.objects.get(pk = pk)

    mentee = petition.user_mentee
    mentor = petition.user_mentor

    ### generar Jitsi videollamada
    title_builder = f"{mentee.username}<>{mentor.username}"
    videocall_url = create_instant_call(title_builder)

    petition.state = "a"
    petition.videocall_url = videocall_url

    petition.save()

    print(f'Petition: {petition.state}; Videocall URL: {petition.videocall_url}')

    context = {
        'mentee': mentee,
        'mentor': mentor,
        'videocall_url': videocall_url,
    }

    msg_html = render_to_string('aceptado.html', context)
    
    # uses Django's email API to send email for accepted mentee request
    send_mail(
        settings.EMAIL_ACEPTADO_SUBJECT,
        "",
        "",
        [mentee.email],
        html_message=msg_html,
        fail_silently=False,
    )

    return redirect('solicitudes_mentor')

def estado_denegado(request,pk):

    petition = Petition.objects.get(pk = pk)

    petition.state = "d"
    petition.save()

    mentee = petition.user_mentee
    mentor = petition.user_mentor
    context = {
        'mentee': mentee,
        'mentor': mentor,
    }

    msg_html = render_to_string('denegado.html', context)
    send_mail(
        settings.EMAIL_DENEGADO_SUBJECT,
        "",                    
        "",
        [mentee.email],
        html_message=msg_html,
        fail_silently=False,
    )

    return redirect('solicitudes_mentor')

def estado_recomendado(request,pk):

    recomended = None

    if request.method == "POST":
        recomended = request.POST.get("search")

    petition = Petition.objects.get(pk = pk)

    petition.state = "r"
    petition.save()

    mentee = petition.user_mentee
    mentor = petition.user_mentor
    
    context = {
        'mentee': mentee,
        'mentor': mentor,
        "recomended":recomended,
    }

    msg_html = render_to_string('recomendado.html', context)
    send_mail(
        settings.EMAIL_RECOMENDADO_SUBJECT,
        "",                    
        "",
        [mentee.email],
        html_message=msg_html,
        fail_silently=False,
    )
    return redirect('solicitudes_mentor')
    
@login_required
def enviar_solicitud(request, pk):

    if request.method == "POST":
        form = PetitionForm(request.POST)
        if form.is_valid():
            try:
                petition = Petition()
                petition.user_mentee = Mentee.objects.get(pk=request.user.pk)
                petition.user_mentor = Mentor.objects.get(pk=pk)

                petition.message = form.cleaned_data["message"]
                petition.state = "p"
                petition.save()
                form = PetitionForm()

                context = {
                    "mentee": petition.user_mentee,
                    "petition": petition,
                    "mentor": petition.user_mentor,
                }

                msg_html = render_to_string('petition.html', context)

                send_mail(
                    settings.EMAIL_PETITION_SUBJECT,
                    "",
                    "",
                    [petition.user_mentor.email],
                    html_message=msg_html,
                    fail_silently=False,
                )

                return redirect("filter")

            except Exception as e:
                print(e)
                message = e
        else:
            message = "Error, form no valid"
    else:
        form = PetitionForm()
        
    mentor = Mentor.objects.get(pk=pk)
    
    
    context = {
        "form" : form,
        "mentor": mentor,
    }

    return render(request, "enviar_solicitud.html", context)

@login_required
def crear_meeting(request, pk, timeslot_id, day, start_time, end_time, title, videocall_url):

    try:
        # update timeslot reservation status
        timeslot = TimeSlot.objects.get(id=timeslot_id)
        timeslot.is_reserved = 1 - timeslot.is_reserved
        timeslot.save()
        
        if timeslot.is_reserved == 1:
            meeting = Meeting.objects.filter(timeslot_id=timeslot_id).first()
            
            if not meeting:
                meeting = Meeting()
                meeting.user_mentee = Mentee.objects.get(pk=request.user.pk)
                meeting.user_mentor = Mentor.objects.get(pk=pk)
                meeting.timeslot = TimeSlot.objects.get(id=timeslot_id)

                meeting.day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
                meeting.start_time = datetime.datetime.strptime(start_time, "%H:%M").time()
                meeting.end_time = datetime.datetime.strptime(end_time, "%H:%M").time()
                meeting.title = f"{title} videocall"
                meeting.videocall_url = unquote(videocall_url)

                meeting.save()
        else:
            meeting = Meeting.objects.filter(timeslot_id=timeslot_id)
            print(meeting)
            if meeting:
                meeting.delete()

    except Exception as e:
        print(e)
        message = e

    return redirect('index')

@login_required
def crear_evento(request):

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = Event()
            event.user = CustomUser.objects.get(pk=request.user.pk)
            event.day = form.cleaned_data["day"]
            event.start_time = form.cleaned_data["start_time"]
            event.end_time = form.cleaned_data["end_time"]
            event.title = form.cleaned_data["title"]
            event.notes = form.cleaned_data["note"]
            event.save()
            form = EventForm()
            return redirect('index')
        else:
            message = "Error, form not valid"
    else:
        form = EventForm()
        message = "No"

    context = {
        "form": form,
    }

    return render(request, "crear_eventos.html", context=context)

@login_required
def eliminar_evento(request, event_id):
    event = Event.objects.get(id=event_id)

    # event existence sanity check
    if event:
        event.delete()

    return redirect('index')

@login_required
def eliminar_timeslot(request, timeslot_id):
    timeslot = TimeSlot.objects.get(id=timeslot_id)

    # event existence sanity check
    if timeslot:
        timeslot.delete()

    return redirect('index')

@login_required
def crear_timeslot(request):

    if request.method == "POST":
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            timeslot = TimeSlot()
            timeslot.user = CustomUser.objects.get(pk=request.user.pk)
            timeslot.day = form.cleaned_data["day"]
            timeslot.start_time = form.cleaned_data["start_time"]
            timeslot.end_time = form.cleaned_data["end_time"]
            timeslot.title = form.cleaned_data["title"]
            timeslot.notes = form.cleaned_data["note"]
            timeslot.is_reserved = 0
            timeslot.save()
            return redirect('index')
        else:
            message = "Error, form not valid"
    else:
        form = TimeSlotForm()
        message = "No"

    context = {
        "form": form
    }

    return render(request, "crear_timeslot.html", context=context)

@login_required
def modificar_rating(request, pk, rating):
    """Summary line



    """
    mentor = Mentor.objects.get(pk=pk)

    if mentor:
        if mentor.rating is None or mentor.rating == 0:
            mentor.rating = rating
        else:
            total_rating = mentor.rating * mentor.num_ratings
            mentor.rating = (total_rating + rating) / (mentor.num_ratings + 1)

        mentor.num_ratings += 1
        mentor.save()

    return redirect('index')