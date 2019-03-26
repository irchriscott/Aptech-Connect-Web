# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from aptechapp.mailer import SendPasswordMail
from time import time

# Create your models here.

def user_image_path(instance, filename):
    return "users/%s_%s" % (str(time()).replace('.', '_'), filename)

def article_image_path(instance, filename):
    return "articles/%s_%s" % (str(time()).replace('.', '_'), filename)

def event_image_path(instance, filename):
    return "events/%s_%s" % (str(time()).replace('.', '_'), filename)

def book_file_path(instance, filename):
    return "ebooks/%s_%s" % (str(time()).replace('.', '_'), filename)

def message_image_path(instance, filename):
    return "events/%s_%s" % (str(time()).replace('.', '_'), filename)


class Branch(models.Model):
    country = models.CharField(max_length=255, blank=False, null=False)
    town = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    languages = models.CharField(max_length=255, blank=False, null=False, default='English')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self):
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Branch, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Branch, self).save(self)

    def to_json(self):
        return {
            'id': self.pk,
            'country': self.country,
            'town': self.town,
            'name': self.name,
            'languages': self.languages.split(','),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Course(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    initials = models.CharField(max_length=20, blank=False, null=False)
    duration = models.IntegerField(blank=False, null=False)
    duration_type = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self):
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Course, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Course, self).save(self)

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.name,
            'initials': self.initials,
            'duration': self.duration,
            'duration_type': self.duration_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class User(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=20, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    password = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to=user_image_path, null=True, blank=True)
    user_type = models.CharField(max_length=200, null=False, blank=False)
    roll_no = models.CharField(max_length=100, null=False, blank=False)
    batch_no = models.CharField(max_length=100, null=False, blank=False)
    course = models.ForeignKey(Course, null=True, blank=True)
    branch = models.ForeignKey(Branch, null=True, blank=True)
    token = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self):
        randompass = get_random_string(6)
        mail = SendPasswordMail(user=self, password=randompass)
        mail.send()
        self.password = make_password(randompass)
        self.token = get_random_string(64)
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(User, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(User, self).save(self)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'gender': self.gender,
            'dob': self.date_of_birth,
            'image': self.image_url.url,
            'user_type': self.user_type,
            'roll_no': self.roll_no,
            'batch_no': self.batch_no,
            'course': self.course.to_json(),
            'branch': self.branch.to_json(),
            'token': self.token,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @property
    def image_url(self):
        return self.image if self.image is not None else 'default/user.jpg'


class Article(models.Model):
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=255, unique=True, null=False, blank=True)
    title = models.CharField(max_length=255, null=False, blank=False, default='article')
    text = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to=article_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text

    def save(self):
        self.uuid = "%s-%s" % (self.title.lower(), get_random_string(12).lower())
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Article, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Article, self).save(self)

    def comments(self):
        return Comment.objects.filter(article__pk=self.pk).order_by('-created_at')

    def to_json(self):
        return {
            'id': self.pk,
            'user': self.user.to_json(),
            'uuid': self.uuid,
            'title': self.title,
            'text': self.text,
            'image': self.image.url,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Comment(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    comment = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment

    def __str__(self):
        return self.comment

    def save(self):
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Comment, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Comment, self).save(self)

    def to_json(self):
        return {
            'id': self.pk,
            'user': self.user.to_json(),
            'comment': self.comment,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Event(models.Model):
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to=event_image_path, null=True, blank=True)
    venue = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self):
        self.uuid = '%s-%s' % (self.name.lower(), get_random_string(12).lower())
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Event, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Event, self).save(self)

    def to_json(self):
        return {
            'id': self.pk,
            'user': self.user.to_json(),
            'uuid': self.uuid,
            'date': self.date,
            'time': self.time,
            'name': self.name,
            'description': self.description,
            'image': self.image.url,
            'venue': self.venue,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Library(models.Model):
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    book = models.FileField(upload_to=book_file_path, null=True, blank=True)
    is_link = models.BooleanField(default=True)
    book_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self):
        self.uuid = '%s-%s' % (self.title.lover(), get_random_string(12).lower())
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Library, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Library, self).save(self)

    @property
    def book_file(self):
        return self.book_link if self.is_link is True else self.book.url

    def to_json(self):
        return {
            'id': self.id,
            'user': self.user.to_json(),
            'title': self.title,
            'author': self.author,
            'book': self.book_file,
            'is_link': self.is_link,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Message(models.Model):
    user = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    message = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to=message_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message

    def __str__(self):
        return self.message

    def save(self):
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Message, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Message, self).save(self)

    def to_json(self):
        return {
            'id': self.pk,
            'user': self.user.to_json(),
            'receiver': self.receiver.to_json(),
            'message': self.message,
            'image': self.image.url if self.image is not None else '',
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
