from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from .models import Post




class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'title',
           'postCategory',
           'text',
       ]

       def clean(self):
           cleaned_data = super().clean()
           title = cleaned_data.get("title")
           text = cleaned_data.get("text")
           if title is not None and len(description) < 20:
               raise ValidationError({
                   "description": "Текст не может быть менее 20 символов."
               })
               return cleaned_data


           if text == title:
               raise ValidationError(
                   "Текст не должен быть идентичен названию."
           )
               return cleaned_data