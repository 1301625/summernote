from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail

from phone_field import PhoneField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



class user_manager(BaseUserManager):

    def _create_user(self,email,name,password,is_staff,is_admin,**extra_fields):
        if not name:
            raise ValueError("필수로 입력해야 합니다")
        if not email:
            raise ValueError("필수로 입력해야 합니다")
        user = self.model(
            email=self.normalize_email(email), # 대문자 소문자로 변경

            name=name,
            is_staff=is_staff,
            is_admin=is_admin,
            is_active=True,
            date_joined=timezone.now(),
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email,name,password=None,**extra_fields):
        return self._create_user(email,name,password,False,False,**extra_fields)
    def create_superuser(self,email,name,password,**extra_fields):
        return self._create_user(email,name,password,True,True,**extra_fields)

# Create your models here.
class user(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    '''
        닉네임을 공백으로 하려면
        null=True 추가하고 unique 제거 , 또는 blank 제거,
        닉네임을 blank 비워두고 싶지만 나중에 더 좋은방법을 생각할것 
    '''
    nickname = models.CharField(
        help_text='nickname',
        max_length=10,
        blank=True,
        unique=True,
        validators=[
            validators.RegexValidator(r'^[\w가-힣]+$', '영문,숫자,한글만 입력해주세요  (예:test테스트123 )', 'invalid')
        ]

    )
    name = models.CharField(
        help_text='name',
        max_length=10,
        validators=[
            validators.RegexValidator(r'^[가-힣]+$', "한글 이름만 입력하세요 (예:홍길동)", 'invalid')
        ]
    )
    phone = PhoneField(unique=True,help_text='Contact phone number' , blank=True) #삭제 예정
    thumbnail = ProcessedImageField(default='default.png' , upload_to='user_image', processors=[ResizeToFill(100,100)],
                                    format="JPEG", options={'quality': 80})

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    object=user_manager()

    #EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'# 이메일을 ID로 사용한다 명시해준다.
    REQUIRED_FIELDS = ['name','phone']

    def __str__(self):
        return self.email

    def get_nickname(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)