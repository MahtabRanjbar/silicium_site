from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.forms import ProfileForm, SignupForm
from accounts.mixins import (AuthorAccessMixin, AuthorsAccessMixin,
                             FieldsMixin, FormValidMixin, SuperUserAccessMixin)
from accounts.models import CustomUser
from accounts.tokens import account_activation_token


# Create your views here.
class ArticleList(AuthorsAccessMixin, ListView):
    context_object_name = 'articles'
    template_name = 'registration/adminlte/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Article
    fields = ['author', 'title', 'slug', 'category', 'description', 'thumbnail', 'published_at', 'status']
    template_name = 'registration/adminlte/article-create-update.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    model = Article
    fields = ['author', 'title', 'slug', 'category', 'description', 'thumbnail', 'published_at', 'status' ]
    template_name = 'registration/adminlte/article-create-update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('accounts:home')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'registration/adminlte/profile.html'
    form_class = ProfileForm

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def get_success_url(self) -> str:
        if self.request.user.is_superuser or self.request.user.is_author:
            return reverse_lazy('accounts:home')
        else:
            return reverse_lazy("accounts:profile")


class Login(LoginView):
    def get_success_url(self) -> str:
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy("accounts:home")
        else:
            return reverse_lazy('accounts:profile')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('accounts:password-change-done')
    template_name = 'registration/password_change.html'


class SignUp(CreateView):
    form_class = SignupForm
    template_name = 'registration/sign_up.html'

    def form_valid(self, form) -> HttpResponse:
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
