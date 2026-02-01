from django.contrib import admin
from .models import Category, Actor, Cinema, Comment, ProfileUser, IpVisitor

# Register your models here.
admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(Cinema)
admin.site.register(Comment)
admin.site.register(ProfileUser)
admin.site.register(IpVisitor)