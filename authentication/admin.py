from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog.models import Ticket, Review, UserFollows
from .models import User

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
