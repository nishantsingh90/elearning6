from django.contrib import admin
from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import MyUser

from .models import Course,Lesson,Post,Profile,Comment,Author,Category,Follow


# admin.site.register(MyUser)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
# admin.site.unregister(Group)
admin.site.register(Follow)



