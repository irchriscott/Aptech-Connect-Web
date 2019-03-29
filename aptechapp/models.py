# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from aptechapp.mailer import SendPasswordMail
from aptechapp.languages import LANGUAGES_CHOICES
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
    languages = models.TextField(max_length=255, blank=False, null=False, default='English')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.pk,
            'country': self.country,
            'town': self.town,
            'name': self.name,
            'languages': self.languages.replace("[", "").replace("]", "").replace("u'", "").replace("'", "").replace(" ", "").split(','),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
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
        if self.pk == None:
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
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class User(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=20, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    password = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to=user_image_path, null=True, blank=True)
    user_type = models.CharField(max_length=200, null=False, blank=False)
    roll_no = models.CharField(unique=True, max_length=100, null=True, blank=True)
    batch_no = models.CharField(max_length=100, null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True)
    branch = models.ForeignKey(Branch, null=False, blank=False)
    token = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self):
        if self.pk == None:
            randompass = get_random_string(6)
            mail = SendPasswordMail(user=self, password=randompass)
            mail.send()
            self.password = make_password(randompass)
            self.token = get_random_string(64)
            self.roll_no = self.roll_no.upper()
            self.batch_no = self.batch_no.upper()
            self.image = 'default/user.jpg'
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(User, self).save()

    def update(self):
        self.updated_at = timezone.now()
        super(User, self).save()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'gender': self.gender,
            'dob': self.date_of_birth,
            'image': self.image.url,
            'user_type': self.user_type,
            'roll_no': self.roll_no,
            'batch_no': self.batch_no,
            'course': self.course.to_json(),
            'branch': self.branch.to_json(),
            'token': self.token,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


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
        if self.pk == None:
            self.uuid = "%s-%s" % (self.title.lower().replace(' ', '-'), get_random_string(12).lower())
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Article, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(Article, self).save(self)

    @property
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
            'comments': [comment.to_json() for comment in self.comments] if self.comments.count() > 0 else [],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
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
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
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
        if self.pk == None:
            self.uuid = '%s-%s' % (self.name.lower().replace(' ', '-'), get_random_string(12).lower())
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Event, self).save()

    def update(self):
        self.updated_at = timezone.now()
        super(Event, self).save()

    def to_json(self):
        return {
            'id': self.pk,
            'user': self.user.to_json(),
            'uuid': self.uuid,
            'date': self.date.strftime('%Y-%m-%d'),
            'time': self.time,
            'name': self.name,
            'description': self.description,
            'image': self.image.url,
            'venue': self.venue,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Library(models.Model):
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    book = models.FileField(upload_to=book_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self):
        if self.pk == None:
            self.uuid = '%s-%s' % (self.title.lower().replace(' ', '-'), get_random_string(12).lower())
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Library, self).save()

    def update(self):
        self.updated_at = timezone.now()
        super(Library, self).save(self)

    @property
    def book_file(self):
        return self.book.url

    def to_json(self):
        return {
            'id': self.id,
            'user': self.user.to_json(),
            'title': self.title,
            'author': self.author,
            'book': self.book_file,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Message(models.Model):
    user = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    message = models.TextField(blank=False, null=False)
    #image = models.ImageField(upload_to=message_image_path, null=True, blank=True)
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
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class FeedBack(models.Model):
    user = user = models.ForeignKey(User)
    about = models.CharField(max_length=255, null=False, blank=False)
    feedback = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.about

    def __str__(self):
        return self.about

    def save(self):
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(FeedBack, self).save(self)

    def update(self):
        self.updated_at = timezone.now()
        super(FeedBack, self).save(self)
