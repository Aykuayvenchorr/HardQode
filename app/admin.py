from django.contrib import admin

# Register your models here.
from app.models import User, Teacher, Product, Lesson, Group

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)

