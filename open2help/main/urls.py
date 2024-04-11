from django.urls import path, re_path
from main.views import index, register_mentee, register_mentor, perfil, filter, perfil_mentee, perfil_mentor, solicitudes_mentor, mentor_detail, mentee_detail, estado_aceptado, estado_denegado, calendar, estado_recomendado, enviar_solicitud, crear_evento, eliminar_evento, eliminar_timeslot, crear_meeting, crear_timeslot, nantik_administration, immune_administration, deactive_user, verify_mentor, modificar_rating

# url patterns
urlpatterns = [
     path("", 
         index, 
         name="main"),
     path("index", 
          index, 
          name="index"),
     path("perfil/", 
          perfil, 
          name="perfil"),
     path("registrar_mentee/", 
          register_mentee, 
          name="register_mentee"),
     path("registrar_mentor/", 
          register_mentor, 
          name="register_mentor"),
     path("filtro/", 
          filter,
          name="filter"),
     path("detalles_mentor/<int:pk>/", 
          mentor_detail, 
          name="mentor_detail"),
     path("detalles_mentee/<int:pk>/",
          mentee_detail,
          name="mentee_detail"),
     path("perfil_mentor/", 
          perfil_mentor, 
          name="perfil_mentor"),
     path("solicitudes_mentor/", 
          solicitudes_mentor, 
          name="solicitudes_mentor"),
     path("perfil_mentee/", 
          perfil_mentee, 
          name="perfil_mentee"),
     path("estado_aceptado/<int:pk>/", 
          estado_aceptado, 
          name="estado_aceptado"),
     path("estado_denegado/<int:pk>/", 
          estado_denegado, 
          name="estado_denegado"),
     path("estado_recomendado/<int:pk>/", 
          estado_recomendado, 
          name="estado_recomendado"),
     path("perfil/calendario", 
          calendar,
          name="calendar"),
     path("enviar_solicitud/<int:pk>/", 
          enviar_solicitud, 
          name="enviar_solicitud"),
     re_path(r"^crear_meeting/(?P<pk>[0-9]+)/(?P<timeslot_id>[0-9]+)/(?P<day>[^/]+)/(?P<start_time>[^/]+)/(?P<end_time>[^/]+)/(?P<title>[^/]+)/(?P<videocall_url>.+)/$",
          crear_meeting,
          name="crear_meeting"),
     path("nantik_administracion", 
          nantik_administration, 
          name="nantik"),
     path("immune_administracion", 
          immune_administration, 
          name="immune"),
     path("deactivate_user/<int:pk>/", 
          deactive_user, 
          name="deactive_user"),
     path("verify_mentor/<int:pk>/", 
          verify_mentor, 
          name="verify_mentor"),
     path("events/", 
          crear_evento, 
          name="eventos"),
     path("eliminar_evento/<int:event_id>/", 
          eliminar_evento, 
          name="eliminar_evento"),
     path("eliminar_timeslot/<int:timeslot_id>/", 
          eliminar_timeslot, 
          name="eliminar_timeslot"),
     path("timeslots/", 
          crear_timeslot, 
          name="timeslots"),
     path("modificar_rating/<int:pk>/<int:rating>/",
          modificar_rating,
          name="modificar_rating"),
]
