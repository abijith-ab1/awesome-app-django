from django.contrib import admin
from .models import *


class TagModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
# Register your models here.
admin.site.register(Post)
admin.site.register(Tag, TagModelAdmin)
