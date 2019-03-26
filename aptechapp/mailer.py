from __future__ import unicode_literals
from django.core.mail import send_mail
from django.conf import settings

class SendPasswordMail(object):

    def __init__(self, user, password=None):
        self.password = password
        self.user = user
        self.subject = '[Aptech Connect] - User Password'
        self.message = 'Message from Aptech Connect'

    @property
    def html_message(self):
        return '''<!DOCTYPE html>
                <html lang="en" dir="ltr">
                    <head>
                        <meta charset="utf-8">
                        <link href="https://fonts.googleapis.com/css?family=Poppins:100,200,400,300,500,600,700" rel="stylesheet">
                        <style type="text/css">
                            *{
                                font-family: Poppins, Avenir, Century Gothic !important;
                            }
                            body{
                                width: 100% !important
                                background:  #DDD !important;
                                padding: 80px 0 !important
                            }
                            .swb-container{ 
                                background:  #FFF;
                                border: 2px solid red
                                padding: 40px
                                margin: auto
                                width: 40%
                            }
                            .swb-header{
                                border-bottom: 1px solid rgba(0, 0, 0, 0.1)
                                padding-bottom: 20px
                            }
                            .swb-header h2{
                                margin: 0 !important
                                color: red
                            }
                            .swb-footer{
                                color: red
                                font-size: 10px
                                margin: 0 !important
                            }

                            .swb-content{
                                margin-bottom: 20px
                            }
                        </style>
                    </head>
                    <body>
                        <div class="swb-container">
                            <div class="swb-header">
                                <h2> Aptech Connect </h2>
                            </div>
                            <div class="swb-content">
                                <p>Hello ''' + self.user.name + '''</p>
                                <p>Your ''' + self.user.user_type + ''' account has been created successfully and here are your credentials : </p>
                                <p><strong>Email Address : </strong>''' + self.user.email + '''</p>
                                <p><strong>Password : </strong>''' + self.password + '''</p>
                            </div>
                            <p class="swb-footer"> Sent By Aptech Connect </p>
                        </div>
                    </body>
                </html>
            ''' # % (self.admin.name, self.admin.email, self.password)

    
    def send(self):
        send_mail(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            [self.admin.email],
            html_message=self.html_message,
            fail_silently=True
        )
