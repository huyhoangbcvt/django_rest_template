from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django import template, forms

register = template.Library()
from datetime import datetime
from django.contrib import auth, admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from django.utils.http import (
    urlsafe_base64_decode,
    url_has_allowed_host_and_scheme,
)
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, DetailView
from django.views.generic import (
    FormView, UpdateView, View
)
from django.utils.functional import cached_property
from django.conf import settings
from django.core import mail, serializers
from django.core.mail import BadHeaderError
from django.urls import reverse, reverse_lazy
from ..models.account_model import Profile
# from .form_auth_ctrl import *
from .form_auth_ctrl import (
    UserForm,
    SignUpForm,
    LoginForm,
    ProfileForm,
    ResetPassForm,
    ResetPassToEmailForm,
)
try:
    from django_rest_template.local_settings import *
except ImportError:
    pass
# Atomic queries
from django.db import transaction


# @crumb('Staff')  # This is the root crumb -- it doesnâ€™t have a parent
def index(request):
    # return HttpResponse('Hello, welcome to the index page.')
    # profile = request.session.get('profile') #print("________: "+json.dumps(profile)+profile['first_name'] )
    print('Run debug ok')
    if request.user.is_authenticated:  # print("_______: "+json.dumps(profile)+profile['first_name'] )
        return redirect('user:home')  # HttpResponseRedirect("/home/")

    return render(request, "index.html",
                  {
                      'title': "Index page",
                      # 'next':'/home/',
                      'content': "Example app page for Django.",
                      'year': datetime.now().year,
                      'design': "Hà Huy Hoàng"
                  }
                  )


# Create your views here.
@login_required
def homepage(request):
    """Renders the home page."""
    try:
        # profile = request.session.get('profile')
        # print("___: "+json.dumps(profile)+profile['first_name'] )
        # if profile and request.session.test_cookie_worked():
        # request.session.set_test_cookie()
        context = {
            'title': "Home page",
            'next': '/home/',
            'link': 'list/',
            'year': datetime.now().year
        }
        return render(request, "home.html", context)  # messages.error(request, 'Please enable cookie')
    # return HttpResponseRedirect("/accounts/login/")
    except Exception as e:
        return redirect("user:login")


#     return TemplateResponse(request, 'index.html')

# class Homepage(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
class Homepage(LoginRequiredMixin, TemplateView):  # LoginRequiredMixin check Ä‘Äƒng nháº­p
    template_name = 'home.html'
    # media_root = settings.MEDIA_ROOT
    # _profile = Profile.objects.all()
    # context_object_name = 'prof'
    # _profile = form_auth.ProfileForm(instance=Profile)

    extra_context = {
        'title': "Home page",
        # 'next':'/home/',
        'list': 'list/',
        # 'profile_form': _profile,
        # 'image_profile': os.listdir(media_root + '/images'), #'image_profile': os.listdir(media_root + '/images/'),
        'year': datetime.now().year
    }
    # extra_context['form'] = form_auth.UserForm
    # extra_context['profile_form'] = form_auth.ProfileForm
    # form_class = extra_context
    # crumbs = []
    crumbs = []


# class TestHomeView(BaseBreadcrumbMixin, TemplateView):
class TestHomeView(TemplateView):
    template_name = 'demo/index.html'
    crumbs = []


# ========= Login ==========
def loginAdminView(request):
    return redirect("/admin/")


class loginUser(View):
    def get(self, request):
        form = LoginForm
        extra_context = {'title': "Đăng nhập", 'next': '/home/', 'year': datetime.now().year, 'form': form}
        return render(request, 'registration/login.html', extra_context)

    def post(self, request):
        # pass
        form = LoginForm
        extra_context = {'title': "Đăng nhập", 'next': '/home/', 'year': datetime.now().year, 'form': form}
        username = request.POST['username']
        passw = request.POST['password']
        if form.is_valid():
            # user = authenticate(request, username=username, password=passw)
            # login with both email or username
            try:
                user = auth.authenticate(request, username=User.object.get(email='username'), password=passw)
            except:
                user = auth.authenticate(request, username=username, password=passw)

            if user is not None:
                auth_login(request, user)
                return redirect('user:home')  # return render(request, 'home.html')
            else:
                extra_context['errors'] = 'Please enter a correct user name and password.'
                return render(request, "registration/login.html", extra_context)
        else:
            return render(request, "registration/login.html", extra_context)

    def form_valid(self, request):
        form_class = LoginForm
        """Security check complete. Log the user in."""
        auth_login(self.request, form_class)
        return HttpResponseRedirect(self.get_success_url())


# class AuthView(DetailBreadcrumbMixin, FormView):
class AuthView(FormView):
    """Renders the home page."""
    form_class = LoginForm  # AuthenticationForm
    template_name = 'registration/login.html'
    extra_context = {
        'title': "Đăng nhập",
        'next': '/home/',
        'site_header': 'Đăng nhập',
        'year': datetime.now().year
    }
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = reverse_lazy('user:index')  # reverse_lazy('user:home')  # '/home/'
    crumbs = [('Đăng nhập', 'login')]  # OR reverse_lazy

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class LoginSocialView(FormView):
    pass


# class LoginView(DetailBreadcrumbMixin, FormView):
class LoginView(FormView):
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

    """
    Provides the ability to login as a user with a username and password
    """
    form_class = LoginForm  # AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    success_url = reverse_lazy('user:index')
    crumbs = [('Đăng nhập', 'login')]  # OR reverse_lazy
    extra_context = {
        'title': "Đăng nhập",
        'title_social': "Đăng nhập mạng xã hội:",
        # 'next': 'home/',
        'site_header': 'Đăng nhập',
        'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
        'year': datetime.now().year
    }
    authentication_form = None
    redirect_authenticated_user = False

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # if self.redirect_authenticated_user and self.request.user.is_authenticated:
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        user = auth.authenticate(username=self.request.POST.get('username', ''),
                                 password=self.request.POST.get('password', ''))
        # profile = Profile.objects.filter(id=user.id).select_related('user') # prefetch_related
        # hhh = serialize('json', profile, cls=DjangoJSONEncoder)
        if user is not None and user.is_active:
            self.request.session.set_test_cookie()
        # self.request.session['profile'] = {"username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "images": '', } #True
        # request.session['profile'] = True #True
        return url or resolve_url('user:home')  # settings.LOGIN_REDIRECT_URL

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context


def login_test(request):
    '''Shows a login form and a registration link.'''
    form_class = LoginForm
    extra_context = {'title': "Ä�Äƒng nháº­p", 'next': '/home/', 'year': datetime.now().year, 'form': form_class}
    # if request.method == 'POST':
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth_login(request, user)  # auth.login(request, user)
            # request.session['first_name'] = user.first_name
            # print(user)
            # request.session['profile'] = {"username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name} #True
            return HttpResponseRedirect("/home/")

        else:
            extra_context['errors'] = 'Please enter a correct user name and password.'
            extra_context['form'] = form_class
            # return HttpResponse("Invalid login. Please try again.")
    # auth_login(request, form_class.get_user())
    # if not POST then return login form
    return render(request, "registration/login.html", extra_context)  # registration/login_test.html


def serialize(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial


def json_modelAPI(valueObject):
    SomeModel_json = serializers.serialize("json", valueObject)
    data = {"SomeModel_json": SomeModel_json}
    return JsonResponse(data)


# ======================== FORM Log out ===============================
class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}


@login_required()
def user_logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    auth_logout(request)
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', True):
        user = None
    #     user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()

    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    #     if request.session.get('profile'):
    #         del request.session['profile'] #xoa session
    return render(request, 'registration/logged_out.html')

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        return self.get(request, *args, **kwargs)


# ======================== sign_up ===============================
class RegistrationAuthorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField}


class RegistrationAuthorView(FormView):  # via template
    template_name = 'registration/register_auth.html'
    # form_class = UserCreationForm
    form_class = RegistrationAuthorForm


# CreateView
# class RegistrationUser(DetailBreadcrumbMixin, FormView):  # via template
class RegistrationUser(FormView):  # via template
    form_class = SignUpForm  # UserCreationForm
    template_name = 'registration/register_auth.html'  # template_name = 'auth/sign_up_auth.html'
    email_template_name = 'registration/password_reset_email.html',
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('user:login')  # '/accounts/login/'
    crumbs = [('Đăng nhập', reverse_lazy('user:login')),
              ('Đăng ký tài khoản', reverse_lazy('user:sign_up'))]  # OR reverse_lazy
    extra_context = {
        'title': "Đăng ký tài khoản",
        'site_header': "Đăng ký tài khoản",
        'next': '/accounts/login/',
        # 'crumbs': crumbs,
        'year': datetime.now().year
    }

    @transaction.atomic
    def form_valid(self, form):
        data = form.cleaned_data  # form.save()  # form data will be saved
        auth_user = User.objects.filter(username=data['username'])
        from pprint import pprint;
        pprint(auth_user)

        if auth_user is not None:
            auth_user = User.objects.create_user(
                username=data['username'],
                password=data['password1'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
        # instance = Profile(
        #     birthday=data['birthday'],
        #     phone_number=data['phone_number'],
        #     user_id=auth_user.id
        # )
        # instance.save()
        return super(RegistrationUser, self).form_valid(form)

    # Phần redirect giữa url & process data
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    # Phần gửi dữ liệu context lên template
    # def get_context_data(self, **kwargs):
    #     # extra_context = super.get_context_data(**kwargs)
    #     extra_context = {
    #         'title': "Đăng ký tài khoản",
    #         'site_header': "Đăng ký tài khoản",
    #         'next': '/accounts/login/',
    #         #         'crumbs': crumbs,
    #         'year': datetime.now().year
    #     }
    #     extra_context['username'] = self.request.GET.get('username')
    #     return extra_context


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def sign_up(request):  # via form
    # extra_context = {}
    form_class = UserCreationForm(request.POST or None)
    if request.POST:  #
        if form_class.is_valid():
            user = form_class.save()
            auth_login(request, user)
            return render(request, 'auth/login_auth.html')

    extra_context = {'title': "Ä�Äƒng kÃ½ tÃ i khoáº£n", 'next': '/accounts/login/', 'year': datetime.now().year,
                     'form': form_class}
    return render(request, 'auth/sign_up_auth.html', extra_context)


# class RegistrationUserProfile(DetailBreadcrumbMixin, FormView):
class RegistrationUserProfile(FormView):
    # Here I say which classes i'm gonna use
    # (It's not mandatory, it's just that I find it easier)
    user_form_class = SignUpForm
    profile_form_class = ProfileForm
    template_name = 'registration/register_auth_full.html'
    email_template_name = 'registration/password_reset_email.html',
    subject_template_name = 'registration/password_reset_subject.txt'
    crumbs = [('Trang chá»§', reverse_lazy('user:index')), ('Ä�Äƒng nháº­p', reverse_lazy('user:login')),
              ('Ä�Äƒng kÃ½ tÃ i khoáº£n', reverse_lazy('user:sign_up'))]

    def get(self, request, *args, **kwargs):
        # price_lte = request.GET['price_lte']
        if self.request.user.is_authenticated:
            return render(request, 'registration/login.html')
        extra_context = {
            'title': "Ä�Äƒng kÃ½ tÃ i khoáº£n",
            'next': '/accounts/login/',
            'year': datetime.now().year
        }
        # Here I make instances of my form classes and pass them None
        # which tells them that there is no additional data to display (errors, for example)
        extra_context['user_form'] = self.user_form_class(None)
        extra_context['profile_form'] = self.profile_form_class(None)
        extra_context['crumbs'] = self.crumbs
        # and then just pass them to my template
        return render(request, self.template_name,
                      extra_context)  # {'user_form': user_form, 'profile_form': profile_form}

    def post(self, request, *args, **kwargs):
        # price_lte = request.GET['price_lte']
        user_form = self.user_form_class(request.POST)
        profile_form = self.profile_form_class(request.POST)
        extra_context = {
            'title': "Ä�Äƒng kÃ½ tÃ i khoáº£n",
            'next': '/accounts/login/',
            'user_form': user_form,
            'profile_form': profile_form,
            'year': datetime.now().year
        }

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'images' in request.FILES:
                print('found it')
                profile.images = request.FILES['images']
            profile.save()

            return redirect('login')  # render(request,'auth/login.html')#return redirect('user:private_profile')
        # else: # form not valid - each form will contain errors in form.errors
        return render(request, self.template_name,
                      extra_context)  # {'user_form': user_form,'profile_form': profile_form}


# ======================== FORM reset pass ===============================
class PassResetView(FormView):  #
    # template_name = 'auth/sign_up_auth.html'
    template_name = 'registration/password_reset_confirm.html'
    form_class = ResetPassForm  ##UserCreationForm
    success_url = reverse_lazy('user:password_reset_complete')  # '/accounts/reset/done/'

    def post(self, request, *args, **kwargs):
        form = ResetPassForm(request.POST or None, user=User)
        self.form_valid(form)

    def form_valid(self, form):
        form.save()  # form data will be saved
        # self.save(commit=True)
        return super(PassResetView, self).form_valid(form)


#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data['password2'])
#         if commit:
#             self.user.save()
#         return self.user

# ======================== reset password ===============================
class PasswordResetView(FormView):
    extra_context = {
        'title': 'Láº¥y láº¡i máº­t kháº©u',  # 'For get password',
        'next': '/accounts/password-reset/done/',
        'year': datetime.now().year
    }
    template_name = 'registration/password_reset_form.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    email_template_name = 'registration/password_reset_email.html',
    form_class = ResetPassToEmailForm
    success_url = reverse_lazy('user:password_reset_done')  # 'done/'

    #     send_mail('Subject', 'Here is the message.', 'hoang.hh@ts24corp.com', ['huyhoangbcvt@gmail.com'], fail_silently=False,)
    def post(self, request, *args, **kwargs):
        data = request.POST
        # name = data.get('first_name', '')
        # subject = "subject: Title header"
        # info_message = "body ms" #data.get('message', '')
        from_email = settings.EMAIL_HOST_USER
        to_email = data.get('email', '')
        # mail.send_mail(subject, info_message, from_email, [to_email], fail_silently=False, )
        context = {
            'title': 'Láº¥y láº¡i máº­t kháº©u',  # 'For get password',
            'next': '/accounts/password-reset/done/',
            'year': datetime.now().year
        }
        subject = render_to_string('registration/password_reset_subject.txt', context=context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        message = render_to_string('registration/password_reset_email.html', context=context)
        mail.send_mail(subject, message, from_email, [to_email],
                       auth_user=None, auth_password=None, fail_silently=False,
                       html_message='', )
        # if html_message:  mail.attach_alternative(html_message=text_body, 'text/html')
        # html_message.attach('auth/Attachment.pdf', file_to_be_sent, 'file/pdf')
        # html_message = render_to_string(template_name='registration/password_reset_email.html')
        # plain_message = strip_tags(html_message)
        # mail.send_mail(subject, plain_message, from_email, [to_email], html_message=html_message, )
        # html_message.attach('auth/Attachment.pdf', file_to_be_sent, 'file/pdf')
        return redirect('password_reset_done')


def resetPassword(req):
    context = {
        'title': 'For get password',
        'year': datetime.now().year
    }
    form_class = ResetPassToEmailForm(req.POST or None)
    # req_method = req.method
    if req.POST:
        if form_class.is_valid():
            subject = "subject: Title header"
            # message = "Body ms2"
            html_message = render_to_string('registration/password_reset_email.html',
                                            {'context': 'values'})  # Error at here
            message = strip_tags(html_message)
            to_email = req.POST.get('email', '')
            rep_list = [to_email]
            try:
                mail.send_mail(subject, message, settings.EMAIL_HOST_USER, rep_list, fail_silently=False, )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return HttpResponseRedirect('/accounts/login/')
        #    return render(request, "auth/reset_password.html", {'next':'/auth/login'})
        #    return HttpResponse('Hello, welcome to the index page.')
        #    return HttpResponse('Mail Sended')
    context['form'] = form_class
    return render(req, 'registration/password_reset_form.html', context)


# WEB Controllers: hoanghh
# ======================== Blog ===============================


class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about/about.html"


# Add this view
class DataPageView(TemplateView):
    # we will pass this context object into the template so that we can access the data list in the template
    def get(self, request, *args, **kwargs):
        context = {
            'data': [
                {
                    'name': 'Celeb 1',
                    'worth': '3567892'
                },
                {
                    'name': 'Celeb 2',
                    'worth': '23000000'
                },
                {
                    'name': 'Celeb 3',
                    'worth': '1000007'
                },
                {
                    'name': 'Celeb 4',
                    'worth': '456789'
                },
                {
                    'name': 'Celeb 5',
                    'worth': '7890000'
                },
                {
                    'name': 'Celeb 6',
                    'worth': '12000456'
                },
                {
                    'name': 'Celeb 7',
                    'worth': '896000'
                },
                {
                    'name': 'Celeb 8',
                    'worth': '670000'
                }
            ]
        }
        return render(request, 'data/data.html', context)


# ============== Profile ================
class RoleManager():  # (models.Manager)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated is None:
            return render(request, 'registration/login.html')

        profile = ProfileForm(instance=request.user.profile)
        ROLE_CHOICES_LIST = ['Student', 'Teacher', 'Supervisor']
        str_role = ''
        # return instance.profile.role
        for index, value in enumerate(ROLE_CHOICES_LIST):
            if (profile.role == index + 1):
                str_role = value
                break
        return str_role


# class TestDetailView(DetailBreadcrumbMixin, DetailView):
class TestDetailView(DetailView):
    model = Profile
    #     home_label = _('My custom home')
    template_name = 'profile/profile_edit.html'


def get_user(request):
    user = request.user
    return user


def get_profile(request):
    return request.user.profile


# class ProfileView(LoginRequiredMixin, DetailBreadcrumbMixin, TemplateView):
class ProfileView(TemplateView):
    model = Profile
    # from pprint import pprint; pprint('author')
    context_object_name = 'profile'
    template_name = 'profile/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # author = Profile.objects.all()[:1] # Lấy 1 loại tk: 1 local or 3 Social
        # context['author'] = author[0]
        # from pprint import pprint; pprint(context['author'])
        return context

    # Phần gửi dữ liệu context lên template
    # def get_context_data(self, **kwargs):
    #     extra_context = super.get_context_data(**kwargs)
    #     extra_context = {
    #         'title': "Thông tin cá nhân",
    #         'role_label': role_value,
    #         'year': datetime.now().year
    #     }
    #     extra_context['author'] = Profile.objects.all()
    #     # extra_context['username'] = self.request.GET.get('username')
    #     return extra_context

    # extra_context = {
    #     'title': "Thông tin cá nhân",
    #     'role_label': role_value,
    #     'year': datetime.now().year
    # }
    # crumbs = [('Thông tin cá nhân', reverse_lazy('user:profile'))]


# class EditUserProfileView_Test(LoginRequiredMixin, ListBreadcrumbMixin, UpdateView):  # Note that we are using UpdateView and not FormView
class EditUserProfileView_Test(UpdateView):  # Note that we are using UpdateView and not FormView
    # https://django.cowhite.com/blog/adding-and-editing-model-objects-using-django-class-based-views-and-forms/
    # model = Profile #form_class = form_auth.ProfileForm
    # user_form_class = UserForm
    # profile_form_class = ProfileForm
    form_class = ProfileForm
    template_name = "profile/profile_edit_full.html"
    extra_context = {
        'title': "Thay đổi thông tin cá nhân",
        'year': datetime.now().year
    }
    crumbs = [('Thông tin cá nhân', reverse_lazy('user:profile')),
              ('Thay đổi thông tin cá nhân', reverse_lazy('user:profile_edit'))]

    def get_object(self, *args, **kwargs):
        # user = get_object_or_404(User, pk=self.kwargs['pk'])
        user = self.request.user
        # We can also get user object using self.request.user  but that doesnt work for other models.
        return user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("user:profile")


# class EditUserProfileView(LoginRequiredMixin, ListBreadcrumbMixin, UpdateView):  # Note that we are using UpdateView and not FormView
class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    # https://django.cowhite.com/blog/adding-and-editing-model-objects-using-django-class-based-views-and-forms/
    # model = Profile #form_class = form_auth.ProfileForm
    # user_form_class = UserForm
    profile_form_class = ProfileForm
    success_url = reverse_lazy('user:profile')
    template_name = "profile/profile_edit.html"
    add_home = False
    extra_context = {
        'title': "Thay đổi thông tin cá nhân",
        'year': datetime.now().year
    }

    @cached_property
    def crumbs(self):
        return [('Trang chá»§', reverse_lazy('user:home')), ('ThÃ´ng tin cÃ¡ nhÃ¢n', reverse_lazy('user:profile')),
                ('Thay Ä‘á»•i thÃ´ng tin cÃ¡ nhÃ¢n', reverse_lazy('user:profile_edit'))]

    # def form_valid(self, form):
    # form.save()  # form data will be saved
    # # post_save.connect(create_user_profile, sender=User)
    # return super(EditUserProfileView, self).form_valid(form)
    # success_url = '/home/'

    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and 'price_lte' in request.GET:
            price_lte = request.GET['price_lte']
            print(price_lte)
        if request.user.is_authenticated is None:
            return render(request, 'registration/login.html')
        # Here I make instances of my form classes and pass them None. # which tells them that there is no additional data to display (errors, for example)
        self.extra_context['user_form'] = UserForm(instance=request.user)  # user_form = self.user_form_class(None)
        self.extra_context['profile_form'] = ProfileForm(instance=request.user.profile)  # profile_form = self.profile_form_class(None)
        self.extra_context['crumbs'] = self.crumbs
        # and then just pass them to my template
        return render(request, self.template_name, self.extra_context)  # {'user_form': user_form, 'profile_form': profile_form}

    #     def get_object(self, *args, **kwargs):
    #         #user = get_object_or_404(User, pk=self.kwargs['pk'])
    #         user = self.request.user
    #         # We can also get user object using self.request.user  but that doesnt work for other models.
    #         return user.profile

    def post(self, request, *args, **kwargs):
        if request.POST and 'price_lte' in request.GET:
            price_lte = request.GET['price_lte']
            print(price_lte)
        # Here I also make instances of my form classes but this time I fill
        # them up with data from POST request
        # user_form = self.user_form_class(request.POST)
        # profile_form = self.profile_form_class(request.POST)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file

        if user_form.is_valid() and profile_form.is_valid():
            user_save = user_form.save()
            custom_save = profile_form.save(False)
            custom_save.user = user_save
            custom_save.save()
            return redirect('user:profile')
        # else: # form not valid - each form will contain errors in form.errors
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("user:profile")


@login_required
def edit_profile_pk(request, gu_id):
    crumbs = [('Trang chá»§', reverse('home')), ('ThÃ´ng tin cÃ¡ nhÃ¢n', reverse('user:profile')),
              ('Thay Ä‘á»•i thÃ´ng tin cÃ¡ nhÃ¢n', reverse('user:profile_edit'))]
    #     @cached_property
    #     def crumbs(self):
    #         return [('Trang chá»§', reverse('home')), ('ThÃ´ng tin cÃ¡ nhÃ¢n', reverse('profile')), ('Thay Ä‘á»•i thÃ´ng tin cÃ¡ nhÃ¢n', reverse('profile_edit'))] #[('My Test Breadcrumb', reverse('profile_edit'))]

    if request.POST:  # request.method == 'POST':
        #         user_form = Book.objects.get(pk=gu_id)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)  # request.FILES is show the selected image or file

        if user_form.is_valid() and profile_form.is_valid():
            print(request.user.get_username())
            #             user_form["username"] = 'hoanghh'
            user_save = user_form.save()
            profile_save = profile_form.save(False)
            #             user_save["username"] = 'hoanghh'
            profile_save.user = user_save
            profile_save.save()
            return redirect('user:profile')

        return render(request, 'profile/profile_edit.html',
                      {'user_form': user_form, 'profile_form': profile_form, 'crumbs': crumbs})
    else:
        context = {'title': "Thay Ä‘á»•i thÃ´ng tin cÃ¡ nhÃ¢n", 'role_label': get_role_func(request),
                   'year': datetime.now().year, 'user_form': UserForm(instance=request.user),
                   'profile_form': ProfileForm(instance=request.user.profile), 'crumbs': crumbs}
        # context.update(csrf(request))
        # args['formatedDate'] = profile_form.birthday.strftime("%Y-%m-%d %H:%M:%S")
        return render(request, 'profile/profile_edit.html', context)


def get_role_func(request):
    SOCIAL_CHOICES = ['Google', 'Facebook', 'Linkedin']
    # return instance.profile.role
    str_role = ''
    for index, value in enumerate(SOCIAL_CHOICES):
        if (request.user.profile.role == index + 1):
            str_role = value
            break
    return str_role


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'
    fk_name = 'user'


# Chá»‰ dÃ¹ng cho admin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'get_address', 'get_phone_number', 'get_role',
        'get_image']
    list_select_related = ('profile',)

    def get_address(self, instance):
        if instance.profile.address:
            return instance.profile.address
        return ''

    get_address.short_description = 'Ä�á»‹a chá»‰'

    def get_phone_number(self, instance):
        if instance.profile.phoneNumber:
            return instance.profile.phoneNumber
        return ''

    get_phone_number.short_description = 'Sá»‘ Ä‘iá»‡n thoáº¡i'

    def get_role(self, instance):
        SOCIAL_CHOICES = ['Google', 'Facebook', 'Linkedin']
        # return instance.profile.role
        str_role = ''
        for index, value in enumerate(SOCIAL_CHOICES):
            if (instance.profile.role == index + 1):
                str_role = value
                break
        return str_role

    get_role.short_description = 'Máº¡ng xÃ£ há»™i'

    def get_image(self, instance):
        if instance.profile.images:
            return instance.profile.images.url
        return ''

    #         return instance.profile.images.url
    get_image.short_description = 'HÃ¬nh áº£nh'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
