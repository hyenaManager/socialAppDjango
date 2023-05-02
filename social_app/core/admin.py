from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(RelationShip)


# Register your models here.
