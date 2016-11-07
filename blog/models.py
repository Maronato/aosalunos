
# -*- coding: UTF-8 -*-
from django.db import models
from app.models import Profile


class Post(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
