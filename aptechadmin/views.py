# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, request
from django.urls import reverse
from django.contrib import messages
from aptechapp.models import User, Course, Branch, Article, Event, Library
from aptechapp.backend import UserAuthentication
from aptechapp.responses import ResponseObject, HttpJsonResponse

# Create your views here.

def check_user_login(func):
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session.keys():
            messages.error(request, 'Login Required, Please !!!')
            return HttpResponseRedirect(reverse('apcon_admin_login'))
        return func(request, *args, **kwargs)
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper

def check_admin_login(func):
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session.keys():
            admin = User.objects.get(pk=request.session['user'])
            if admin.user_type != 'user' or admin.user_type != 'superadmin':
                messages.error(request, 'Exclusively For Administrator Only !!!')
                return HttpResponseRedirect(reverse('apcon_admin_index'))
        return func(request, *args, **kwargs)
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def super_admin_only(func):
    def wrapper(request, *args, **kwargs):
        if 'user' in request.session:
            admin = User.objects.get(pk=request.session['user'])
            if admin.user_type != 'superadmin':
                messages.error(request, 'Exclusively For Super Administrator Only !!!')
                return HttpResponseRedirect(reverse('apcon_admin_index'))
        return func(request, *args, **kwargs)
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


class AdminLogin(TemplateView):

    template = 'adm/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            auth = UserAuthentication(email=email, password=password)

            if auth.authenticate != None:
                request.session['user'] = auth.authenticate.pk
                messages.success(request, 'User Logged In Successfully !!!')
                return HttpResponseRedirect(reverse('apcon_admin_index'))
            else:
                messages.error(request, 'Invalid Email or Password !!!')
                return HttpResponseRedirect(reverse('apcon_admin_login'))
        else:
            messages.error(request, 'Bad Request')
            return HttpResponseRedirect(reverse('apcon_admin_login'))


def admin_logout(request):
    try:
        del request.session['user']
        messages.success(request, 'User Logged Out Successfully !!!')
        return HttpResponseRedirect(reverse('apcon_admin_login'))
    except KeyError:
        pass


@check_user_login
@check_admin_login
def dashboard(request):
    return render(request, 'adm/dashboard.html', {})


@check_user_login
@check_admin_login
def students(request):
    user = User.objects.get(pk=request.session['user'])
    students = User.objects.filter(user_type='student', branch__id=user.branch.id).order_by('-created_at')
    courses = Course.objects.all()
    return render(request, 'adm/students.html', {'students': students, 'user': user, 'courses': courses})


@check_admin_login
@check_user_login
def add_new_student(request):
    if request.method == 'POST':
        session = User.objects.get(pk=request.session['user'])
        user = UserForm(request.POST, instance=User(
                branch=Branch.objects.get(pk=session.branch.id),
                course=Course.objects.get(pk=request.POST.get('course')),
                user_type='student'
            ))
        if user.is_valid():
            user.save()
            messages.success(request, 'Student Added Successfully !!!')
            return HttpJsonResponse(ResponseObject('success', 'Student Added Successfully !!!', 200, 
                reverse('apcon_admin_students')))
        else:
            return HttpJsonResponse(
                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400, msgs=user.errors.items()))
    else:
        return HttpJsonResponse(ResponseObject('error', 'Bad Request', 400))


@check_user_login
@check_admin_login
def articles(request):
    user = User.objects.get(pk=request.session['user'])
    articles = Article.objects.filter(user__pk=user.id).order_by('-created_at')
    return render(request, 'adm/articles.html', {'articles': articles, 'user': user})


@check_user_login
@check_admin_login
def add_new_article(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['user'])
        article = ArticleForm(request.POST, request.FILES, instance=Article(
                user=User.objects.get(pk=user.id)
            ))
        if article.is_valid():
            article.save()
            messages.success(request, 'Article Added Successfully !!!')
            return HttpJsonResponse(ResponseObject('success', 'Article Added Successfully !!!', 200, 
                reverse('apcon_admin_articles')))
        else:
            return HttpJsonResponse(
                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400, msgs=article.errors.items()))
    else:
        return HttpJsonResponse(ResponseObject('error', 'Bad Request', 400))


@check_user_login
@check_admin_login
def events(request):
    user = User.objects.get(pk=request.session['user'])
    events = Event.objects.filter(user__branch__pk=user.branch.pk).order_by('-created_at')
    return render(request, 'adm/events.html', {'events': events, 'user': user})


@check_admin_login
@check_user_login
def add_new_event(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['user'])
        event = EventForm(request.POST, request.FILES, instance=Event(
                user=User.objects.get(pk=user.pk)
            ))
        if event.is_valid():
            event.save()
            messages.success(request, 'Event Added Successfully !!!')
            return HttpJsonResponse(ResponseObject('success', 'Event Added Successfully !!!', 200, 
                reverse('apcon_admin_events')))
        else:
            return HttpJsonResponse(
                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400, msgs=event.errors.items()))
    else:
        return HttpJsonResponse(ResponseObject('error', 'Bad Request', 400))


@check_user_login
@check_admin_login
def ebooks(request):
    user = User.objects.get(pk=request.session['user'])
    ebooks = Library.objects.all().order_by('-created_at')
    return render(request, 'adm/ebooks.html', {'books': ebooks, 'user': user})


@check_admin_login
@check_user_login
def add_new_book(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['user'])
        is_link = False if request.FILES.get('book') is not None else True
        book = LibraryForm(request.POST, request.FILES, instance=Library(
                user=User.objects.get(pk=user.pk),
                is_link=is_link
            ))
        if book.is_valid():
            book.save()
            messages.success(request, 'E-Book Added Successfully !!!')
            return HttpJsonResponse(ResponseObject('success', 'E-Book Added Successfully !!!', 200, 
                reverse('apcon_admin_ebooks')))
        else:
            return HttpJsonResponse(
                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400, msgs=event.errors.items()))
    else:
        return HttpJsonResponse(ResponseObject('error', 'Bad Request', 400))