# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from aptechapp.models import Course, Branch, User
from aptechapp.forms import CourseForm, AdminUserForm, BranchForm

# Register your models here.

@admin.register(Branch)
class CreateBranch(admin.ModelAdmin):
    form = BranchForm

@admin.register(Course)
class CreateCourse(admin.ModelAdmin):
    form = CourseForm

@admin.register(User)
class CreateUser(admin.ModelAdmin):
    form = AdminUserForm


