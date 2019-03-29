# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, request
from django.urls import reverse
from django.contrib import messages
from aptechapp.models import User, Course, Branch, Article, Event, Library, Comment, Message, FeedBack
from aptechapp.backend import StudentAuthentication
from aptechapp.forms import UserForm, ArticleForm, EventForm, LibraryForm, ProfileImageForm, FeedBackForm
from aptechapp.responses import ResponseObject, HttpJsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.db.models import Q
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
	                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400), 400)
		else:
			return response_response(ResponseObject('error', 'Unknown User', 400), 400)
	else:
		return response_response(ResponseObject('error', 'Bad Request', 400), 400)


def api_get_users(request, token):
	user = User.objects.filter(token=token).first()
	if user is not None:
		users = User.objects.filter(user_type=user.user_type).order_by('-created_at')
		return data_response([u.to_json() for u in users], 200)
	else:
		return response_response(ResponseObject('error', 'Unknown Token', 401), 401)


@csrf_exempt
def api_update_user_image(request, token):
	if request.method == 'POST':
		user = User.objects.filter(token=token).first()
		if user != None:
			
			image_form = ProfileImageForm(request.POST, request.FILES)

			if image_form.is_valid():
				sessuser = User.objects.get(pk=user.pk)
				sessuser.image = image_form.cleaned_data['image']
				sessuser.save()

				return data_response(sessuser.to_json(), 200)
			else:
				return response_response(
	                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400), 400)
		else:
			return response_response(ResponseObject('error', 'Unknown User', 400), 400)
	else:
		return response_response(ResponseObject('error', 'Bad Request', 400), 400)


def api_get_messages(request, token, user_id):
	user = User.objects.filter(token=token).first()
	if user is not None:
		messages = Message.objects.filter(Q(user__id=user.pk, receiver__id=user_id) | Q(user__id=user_id, receiver__id=user.pk)).order_by('created_at')
		return data_response([mess.to_json() for mess in messages], 200)
	else:
		return response_response(ResponseObject('error', 'Unknown Token', 401), 401)


@csrf_exempt
def api_send_message(request, token, user_id):
	if request.method == 'POST':
		data = json.loads(request.body)
		text = data["message"]

		sender = User.objects.get(token=token)
		receiver = User.objects.get(pk=user_id)

		if text != "":

			if sender != None and receiver != None:

				message = Message(
						user=sender,
						receiver=receiver,
						message=text
					)
				message.save()

				return response_response(ResponseObject('success', 'Message Sent', 200), 200)	
			else:
				return response_response(ResponseObject('error', 'Unknown Users', 400), 400)
		else:
			return response_response(ResponseObject('error', 'Message Cannot Be Empty', 400), 400)
	else:
		return response_response(ResponseObject('error', 'Bad Request', 400), 400)


def api_get_books(request, token):
	user = User.objects.filter(token=token).first()
	if user is not None:
		books = Library.objects.all().order_by('created_at')
		return data_response([book.to_json() for book in books], 200)
	else:
		return response_response(ResponseObject('error', 'Unknown Token', 401), 401)


@csrf_exempt
def api_post_feed_back(request, token):
	if request.method == 'POST':
		user = User.objects.filter(token=token).first()
		if user != None:
			
			feedback = FeedBackForm(request.POST, instance=FeedBack(
					user=User.objects.get(token=token)
				))

			if feedback.is_valid():
				feedback.save()

				return response_response(ResponseObject('success', 'FeedBack Sent Successfully !!!', 200), 200)
			else:
				return response_response(
	                ResponseObject('error', 'Fill All Fields With Rignt Data, Please !!!', 400), 400)
		else:
			return response_response(ResponseObject('error', 'Unknown User', 400), 400)
	else:
		return response_response(ResponseObject('error', 'Bad Request', 400), 400)
