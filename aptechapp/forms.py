from __future__ import unicode_literals
from django import forms
from aptechapp.models import Course, User, Article, Event, Library, Branch, FeedBack
from aptechapp.languages import LANGUAGES_CHOICES

DURATION_TYPE = (
    ('Days', 'Days'),
    ('Months', 'Months'),
    ('Years', 'Years'),
    ('Semesters', 'Semesters')
)

USER_TYPE = (
    ('admin', 'Admin'),
    ('student', 'Student')
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class CourseForm(forms.ModelForm):

    duration_type = forms.ChoiceField(widget=forms.Select, choices=DURATION_TYPE)
    
    class Meta:
        model = Course
        fields = ('name', 'initials', 'duration', 'duration_type',)


class BranchForm(forms.ModelForm):

    languages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        choices=LANGUAGES_CHOICES)

    class Meta:
        model = Branch
        fields = ('country', 'town', 'name', 'languages',)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'gender', 'roll_no', 'batch_no', 'course',)


class AdminUserForm(forms.ModelForm):

    user_type = forms.ChoiceField(widget=forms.Select, choices=USER_TYPE)
    gender = forms.ChoiceField(widget=forms.Select, choices=GENDER)

    class Meta:
        model = User
        fields = ('name', 'email', 'gender', 'date_of_birth', 'user_type', 'branch',)


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text', 'image')


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'date', 'time', 'description', 'venue', 'image',)


class LibraryForm(forms.ModelForm):

    class Meta:
        model = Library
        fields = ('title', 'author', 'book',)


class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('image',)


class FeedBackForm(forms.ModelForm):

    class Meta:

        model = FeedBack
        fields = ('about', 'feedback',)