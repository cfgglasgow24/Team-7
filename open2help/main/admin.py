from django.contrib import admin

from .models import CustomUser, Mentee, Mentor, Occupation, Education, Interest, How_did_you_meet_us, Petition, Event, TimeSlot, Meeting

# register models
admin.site.register(CustomUser)
admin.site.register(Mentee)
admin.site.register(Mentor)
admin.site.register(Occupation)
admin.site.register(Education)
admin.site.register(Interest)
admin.site.register(How_did_you_meet_us)
admin.site.register(Event)
admin.site.register(Petition)
admin.site.register(Meeting)
admin.site.register(TimeSlot)
