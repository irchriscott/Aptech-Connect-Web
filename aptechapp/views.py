# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, request
from django.urls import reverse

# Create your views here.

def home(request):
	return HttpResponseRedirect(reverse('apcon_admin_index'))
