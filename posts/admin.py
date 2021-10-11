from django.contrib import admin
from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ("content", "groups", "author", "created" ,"updated")
    list_filter = ("groups","created")
    # search_fields = ("author",)
    # readonly_fields = ("content",)





admin.site.register(models.Post,PostAdmin)
admin.site.register(models.PostImage)
admin.site.register(models.Comment)
admin.site.register(models.Like)
