from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.conf import settings

from .models import user


from phone_field import forms as Phone

#유저 생성
class signupform(forms.ModelForm):
    email = forms.EmailField(required=True,label="이메일", max_length=255
                            ,help_text="이메일 주소 입력",
                             error_messages={"invalid":"올바른 이메일 주소를 입력하세요 (예:example@gmail.com)"}
                             ,widget=forms.EmailInput(attrs={'class':'form-control',
                                                             'placeholder': '이메일',
                                                             'required': 'True',}))
    nickname = forms.RegexField(label="닉네임(선택)", regex=r'^[\wㄱ-힣]+$',
                                help_text="영문,숫자,한글 만 입력",
                                error_messages={'invalid':"영문,숫자,한글 만 입력해주세요  (예:test테스트123 )"},
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'nickname',
                                }))
    name= forms.RegexField(label="이름", required=True, max_length=10,
                          regex=r'^[ㄱ-힣]+$',
                          help_text="이름 입력",
                          error_messages={'invalid':"한글만 입력하세요"},
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'name',
                               'required':'True',
                           }))
    phone = Phone.PhoneFormField()


    password1 = forms.CharField(label='패스워드',required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'패스워드',
                                    'required':'True',
                                }))
    password2 = forms.CharField(label='패스워드 확인',required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': '패스워드 확인',
                                    'required': 'True',
                                }))

    class Meta:
        model = user
        fields = ['email', 'name', 'nickname', 'phone']

    # 모델에 validator를 적용시키면 폼에서 적용시킬필요가없다

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):


    email = forms.EmailField(label="Email",required=True, max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': ('Email address'),
            'required': True,
            'autofocus': True,
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True,
        }
    )
    )

    class Meta:
        fields = ['email', 'password']