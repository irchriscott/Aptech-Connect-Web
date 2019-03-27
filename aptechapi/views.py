# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, request
from django.urls import reverse
from django.contrib import messages
from aptechapp.models import User, Course, Branch, Article, Event, Library
from aptechapp.backend import StudentAuthentication
from aptechapp.forms import UserForm, ArticleForm, EventForm, LibraryForm
from aptechapp.responses import ResponseObject, HttpJsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

# Create your views here.

def data_response(data, status=200):
	response = HttpJsonResponse(data, status=status)
	response['Access-Control-Allow-Origin'] = "*"
	response['Access-Control-Allow-Headers'] = "origin, x-requested-with, content-type"
	response['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
	return response


def check_user_token(token):
	user = User.objects.get(token=token)
	if user != None:
		request.session['student'] = user.pk
	else:
		return data_response(ResponseObject('error', 'Unknown Token', 401), 401)


@csrf_exempt
def api_login(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		roll_no = data["roll_no"]
		password = data["password"]
		user = StudentAuthentication(roll_no=roll_no, password=password)

		if user.authenticate != None:
			return data_response(user.to_json(), 200)
		else:
			return data_response(ResponseObject('error', 'Incorrect Roll Number or Password', 400), 400)
	else:
		return data_response(ResponseObject('error', 'Bad Request', 400), 400)


def api_get_users(request):
	users = User.objects.all()
	return data_response([user.to_json() for user in users], 200)


def api_get_articles(request, token):
	check_user_token(token)


