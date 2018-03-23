# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "User first_name cannot be empty"
        if any(char.isdigit() for char in postData['first_name']) == True:
            errors['first_name'] = "User first_name cannot contain numbers"

        if len(postData['last_name']) < 1:
            errors['last_name'] = "User last_name cannot be empty"
        if any(char.isdigit() for char in postData['last_name']) == True:
            errors['last_name'] = "User last_name cannot contain numbers"

        if len(postData['email']) < 1:
            errors['email'] = "User email cannot be empty"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "User email is not a valid email"
        
        for user in User.objects.all():
            if user.email == postData['email']:
                errors['email'] = "User email is already registered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be more than 8 characters!"
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password must be the same as Confirm PW"
        
        if postData['bday'] == "":
            errors['bday'] = "Birthday is not set"
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])) < 1:
            errors['email'] = "User email not found"
            return errors
        get = User.objects.get(email= postData['email'])
        if bcrypt.checkpw(postData['password'].encode(), get.password.encode()) == False:
            errors['password'] = "User password incorrect"
        return errors
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 3:
            errors['quoted_by'] = "Quoted By must be more than 3 characters"
        if len(postData['message']) < 10:
            errors['message'] = "Message must be more than 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    bday = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {}, {}, {}, {}>".format(self.first_name,self.last_name,self.email,self.password,self.bday)


class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.CharField(max_length=1000)
    contributer = models.ForeignKey(User, related_name="quotes_contributed")
    liked_users = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<Quote object: {}, {}, {}, {}".format(self.quoted_by,self.message,self.contributer,self.liked_users)

