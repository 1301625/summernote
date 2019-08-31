from django.db import models

from django import forms
from django.core.exceptions import ValidationError

from datetime import date,timedelta
from account.models import user


def date_check(value):
    if date.today() > value:
            raise ValidationError("지난 날짜는 선택할수 없습니다")
    else:
        return value

class Post(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()

    user_max_count = models.PositiveIntegerField(default=0)
    user_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deadline = models.DateField(validators=[date_check])

    users = models.ManyToManyField(user, related_name='post_users')

    def __str__(self):
        return self.title

    def deta(self):
        return date.today() > self.deadline
    #기간 체크
    def date_overlap(self):
        return self.deadline < date.today()

    #인원 체크
    def count_overlap(self):
        return  self.user_count >= self.user_max_count

    def user_count_plus(self):
        return self.user_count+1

    def user_count_minus(self):
        return self.user_count-1


    # def count_overlap(self):
    #     if self.user_count < self.user_max_count:
    #         return ValueError("넘지 못함")
