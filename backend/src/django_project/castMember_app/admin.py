from django.contrib import admin
from django_project.castMember_app.models import CastMember

class CastMemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(CastMember, CastMemberAdmin)