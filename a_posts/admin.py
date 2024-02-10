from django.contrib import admin
from .models import *


class TagModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
# Register your models here.
admin.site.register(Post)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikedPost)
admin.site.register(LikedComment)
admin.site.register(LikedReply)
