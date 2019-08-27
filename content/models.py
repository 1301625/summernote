from django.db import models

from django import forms
from django.core.exceptions import ValidationError
from datetime import date,timedelta


def date_check(value):
    if date.today() > value:
            raise ValidationError("지난 날짜는 선택할수 없습니다")
    else:
        return value

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    user_max_count = models.PositiveIntegerField(default=0)
    user_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deadline = models.DateField(validators=[date_check])


    def __str__(self):
        return self.title

    #기간 체크
    def date_overlap(self):
        return self.deadline < date.today()

    def count_overlap(self):
        return  self.user_count >= self.user_max_count


    # def count_overlap(self):
    #     if self.user_count < self.user_max_count:
    #         return ValueError("넘지 못함")
