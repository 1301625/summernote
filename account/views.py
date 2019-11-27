from django.shortcuts import render, redirect, HttpResponseRedirect

from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import CreateView , FormView
from django.views.generic.base import TemplateView

from .forms import signupform, LoginForm ,VerificationEmailForm


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list')
    else:
        form = signupform()
    return render(request, 'account/signup.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:  #로그인 체크
        return redirect('list')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)

            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('list')
            else:
                form.add_error(None, "아이디 또는 비밀번호가 올바르지 않습니다")

        else:
            form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('list')

#회원가입 뷰
class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = signupform
    template_name = 'account/signup.html'

    success_url = '/account/login/'

    email_template_name = 'account/registration_verification.html'

    token_generator = default_token_generator  # 토큰 생성

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response

    #확인 이메일 보내는 함수
    def send_verification_email(self,user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user,token)
        html_message = render(self.request, self.email_template_name, {'url': url}).content.decode('utf-8')
        user.email_user('회원가입을 축하드립니다.', '다음 주소로 이동하셔서 인증하세요. {}'.format(url),
                        from_email=settings.EMAIL_HOST_USER , html_message=html_message)
        messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

    #확인 이메일 링크 생성
    def build_verification_link(self, user, token):
        return '{}/account/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)


class UserVerificationView(TemplateView):
    model = get_user_model()
    redirect_url = '/account/login/'

    token_generator = default_token_generator

    def get(self ,request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료 되었습니다')
        else:
            messages.error(request, '인증이 실패되었습니다')
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.object.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()
        return is_valid


class ResendVerifyEmailView(FormView):

    model = get_user_model()
    form_class =  VerificationEmailForm
    success_url = '/account/login/'
    template_name = 'account/resend_verify_email.html'
    email_template_name = 'account/registration_verification.html'

    token_generator = default_token_generator

    def send_verification_email(self,user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user,token)
        html_message = render(self.request, self.email_template_name, {'url': url}).content.decode('utf-8')
        user.email_user('회원가입을 축하드립니다.', '다음 주소로 이동하셔서 인증하세요. {}'.format(url),
                        from_email=settings.EMAIL_HOST_USER , html_message=html_message)
        messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

    def build_verification_link(self, user, token):
        return '{}/account/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

    def form_valid(self,form):
        email = form.cleaned_data['email']
        try :
            user = self.model.object.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')

        else:
            self.send_verification_email(user)

        return super().form_valid(form)
