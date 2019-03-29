# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, request
from django.urls import reverse
from django.contrib import messages
from aptechapp.models import User, Course, Branch, Article, Event, Library, Comment
from aptechapp.backend import StudentAuthentication
from aptechapp.forms import UserForm, ArticleForm, EventForm, LibraryForm
from aptechapp.responses import ResponseObject, HttpJsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import datetime
import json

# Create your views here.

def data_response(data, status=200):
	response = HttpResponse(json.dumps(data, default=str, indent=4), content_type="application/json", status=status)
	response['Access-Control-Allow-Origin'] = "*"
	response['Access-Control-Allow-Headers'] = "origin, x-requested-with, content-type"
	response['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
	return response

def response_response(data, status=200):
	response = HttpJsonResponse(data, status=status)
	response['Access-Control-Allow-Origin'] = "*"
	response['Access-Control-Allow-Headers'] = "origin, x-requested-with, content-type"
	response['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
	return response


def check_user_token(token):
	user = User.objects.filter(token=token).first()
	if user is not None:
		request.session['student'] = user.pk
	else:
		return response_response(ResponseObject('error', 'Unknown Token', 401), 401)


@csrf_exempt
def api_login(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		roll_no = data["roll_no"].upper()
		password = data["password"]

		user = User.objects.filter(roll_no=roll_no).first()
		if user != None:
			if check_password(password, user.password) == True and user.user_type == 'student':
				return data_response(user.to_json(), 200)
			else:
				return response_response(ResponseObject('error', 'Incorrect Roll Number or Password', 400), 400)	
		else:
			return response_response(ResponseObject('error', 'Incorrect Roll Number or Password', 400), 400)
	else:
		return response_response(ResponseObject('error', 'Bad Request', 400), 400)


def api_get_users(request):
	users = User.objects.all()
	return data_response([user.to_json() for user in users], 200)


def api_get_articles(request, token):
	user = User.objects.filter(token=token).first()
	if user is not None:
		articles = Article.objects.all().order_by('-created_at')
		return data_response([article.to_json() for article in articles], 200)
	else:
		return response_response(ResponseObject('error', 'Unknown Token', 401), 401)


@csrf_exempt
def api_post_comment(request, token):
	if request.method == 'POST':
		data = json.loads(request.body)
		text = data["comment"]
		article = data["article"]
		user = User.objects.filter(token=token).first()
		if user != None:
			comment = Comment(
					user=User.objects.get(pk=user.pk),
					comment=text,
					article=Article.objects.get(pk=article)
				)
			comment.save()
			return data_response(comment.to_json(), 200)	
		else:
			return response_response(ResponseObject('error', 'Unknown User', 400), 400)
	else:
		return response_response(ResponseObject('error', 'Bad Request', 400), 400)


def api_get_events(request, token):
	user = User.objects.filter(token=token).first()
	if user is not None:
		events = Event.objects.filter(user__branch__pk=user.branch.pk).order_by('-created_at')
		return data_response([event.to_json() for event in events], 200)
	else:
		return response_response(ResponseObject('error', 'Unknown Token', 401), 401)

@csrf_exempt
def api_post_article(request, token):
	if request.method == 'POST':
		user = User.objects.filter(token=token).first()
		if user != None:
			article = ArticleForm(request.POST, request.FILES, instance=Article(
	                user=User.objects.get(pk=user.id)
	            ))
			if article.is_valid():
				article.save()
				return response_response(ResponseObject('success', 'Article Added Successfully !!!', 200), 200)
			else:
				return response_response(
	                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400, msgs=article.errors.items()), 400)
		else:
			return response_response(ResponseObject('error', 'Unknown User', 400), 400)
	else:
		return response_response(ResponseObject('error', 'Bad Request', 400), 400)


