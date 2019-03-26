# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from aptechapp.models import Course, Branch, User
from aptechapp.forms import CourseForm, UserForm

# Register your models here.

admin.site.register(Branch)

@admin.register(Course)
class CreateCourse(admin.ModelAdmin):
    form = CourseForm

@admin.register(User)
class CreateUser(admin.ModelAdmin):
    form = UserForm


