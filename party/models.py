
# -*- coding: UTF-8 -*-
from django.db import models
from app.models import Profile


class Promise(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Text(models.Model):

    home_1_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    home_1_text = models.TextField(null=True, blank=True, default=" ")
    home_2_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    home_2_text = models.TextField(null=True, blank=True, default=" ")

    consu_1_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    consu_1_text = models.TextField(null=True, blank=True, default=" ")
    consu_2_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    consu_2_text = models.TextField(null=True, blank=True, default=" ")

    promise_1_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    promise_1_text = models.TextField(null=True, blank=True, default=" ")
    promise_2_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    promise_2_text = models.TextField(null=True, blank=True, default=" ")

    us_1_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    us_1_text = models.TextField(null=True, blank=True, default=" ")
    us_2_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    us_2_text = models.TextField(null=True, blank=True, default=" ")

    join_1_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    join_1_text = models.TextField(null=True, blank=True, default=" ")
    join_2_title = models.CharField(max_length=200, null=True, blank=True, default=" ")
    join_2_text = models.TextField(null=True, blank=True, default=" ")

    def home(self):
        res = {
            'title_1': self.home_1_title,
            'text_1': self.home_1_text,
            'title_2': self.home_2_title,
            'text_2': self.home_2_text,
        }
        return res

    def consu(self):
        res = {
            'title_1': self.consu_1_title,
            'text_1': self.consu_1_text,
            'title_2': self.consu_2_title,
            'text_2': self.consu_2_text,
        }
        return res

    def about(self):
        res = {
            'title_1': self.us_1_title,
            'text_1': self.us_1_text,
            'title_2': self.us_2_title,
            'text_2': self.us_2_text,
        }
        return res

    def promise(self):
        res = {
            'title_1': self.promise_1_title,
            'text_1': self.promise_1_text,
            'title_2': self.promise_2_title,
            'text_2': self.promise_2_text,
        }
        return res

    def join(self):
        res = {
            'title_1': self.join_1_title,
            'text_1': self.join_1_text,
            'title_2': self.join_2_title,
            'text_2': self.join_2_text,
        }
        return res

    @staticmethod
    def get_text():
        try:
            text = Text.objects.get(pk=1)
            return text
        except:
            text = Text()
            text.save()
            return text


class Members(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    picture = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    @staticmethod
    def create_member(ra):
        try:
            p = Profile.objects.get(ra=ra)
        except:
            return None
        p.is_mod = True
        p.save()
        try:
            m = Members.objects.get(profile=p)
            return m
        except:
            pass
        m = Members(profile=p)
        m.save()
        return m
