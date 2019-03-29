from __future__ import unicode_literals
from aptechapp.models import User
from django.contrib.auth.hashers import check_password

class UserAuthentication(object):

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password
        self.admin = None
    
    def check_email(self):
        try:
            self.admin = User.objects.get(email=self.email)
        except User.DoesNotExist:
            pass
    
    def check_pswd(self):
        self.check_email()
        if self.admin != None:
            return self.admin if check_password(self.password, self.admin.password) == True else None
        else:
            return None

    @property
    def authenticate(self):
        return self.check_pswd()


class StudentAuthentication(object):

    def __init__(self, roll_no=None, password=None):
        self.roll_no = roll_no
        self.password = password
        self.user = None
    
    def check_email(self):
        try:
            self.user = User.objects.get(roll_no=self.roll_no)
        except User.DoesNotExist:
            pass
    
    def check_pswd(self):
        self.check_email()
        if self.user != None:
            return self.user if check_password(self.password, self.user.password) == True else None
        else:
            return None

    def check_user_type(self):
        if self.check_pswd() is not None:
            return self.user if self.user.user_type == 'student' else None
        else:
            return None

    def authenticate(self):
        return self.check_user_type()