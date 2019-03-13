from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import is_password_usable, make_password, check_password
from imdb.models import Login, MyUser, Movie, Actor, Award, CustomUser
from django.contrib.auth.models import User
from datetime import datetime

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)


class LoginForm(forms.Form):
    # user_name = forms.CharField(label='Username', max_length=100, widget=forms.TextInput)
    # password = forms.CharField(widget=forms.PasswordInput)
    # message = forms.CharField(widget=forms.Textarea)
    # date = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    # favorite_colors = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=FAVORITE_COLORS_CHOICES,
    # )
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)
    class Meta:
        # model = Login
        fields = ('username', 'password')
        # labels = {
        #     'username': _('Username'),
        #     'password': _('Password'),
        # }
        # widgets = {
        #     'password': forms.PasswordInput,
        # }
        # help_texts = {
            # 'username': _('Your username.'),
            # 'password': _('Your password.'),
        # }
        # error_messages = {
        #     'username': {
        #         'max_length': _("This username is too long.")
        #     },
        # }

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        username_list = list(User.objects.values_list('username', flat=True))
        if username not in username_list:
            raise forms.ValidationError(
                'Username not found, please create an account.'
            )
        user_obj = User.objects.get(username=username)
        if not check_password(password, user_obj.password):
            raise forms.ValidationError(
                'Password invalid, please try again.'
            )



class SignupForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, help_text="Re-enter your password.")

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm',)

        labels = {
            'username' : _('Username'),
            # 'email_address': _('Email address *'),
            'password': _('Password'),
            'password_confirm': _('Password confirmation'),
        }
        widgets = {
            'password': forms.PasswordInput,
            # 'password_confirm': forms.PasswordInput,
            # 'email_address': forms.EmailInput,
        }
        help_texts = {
            'username': _('Username may only contain alphanumeric characters or single hyphens, and cannot begin or end with a hyphen.'),
            # 'email_address': _('We’ll occasionally send updates about your account to this inbox. We’ll never share your email address with anyone.'),
            'password': _("Make sure it's more than 15 characters OR at least 8 characters including a number and a lowercase letter."),
            # 'password_confirm': _("Re-enter your password.",)
        }
        error_messages = {
            'username': {
                'max_length': _("This username is too long."),
            },
        }

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if not check_password(password_confirm, password):
            raise forms.ValidationError(
                'Password and confirmation password does not match.'
            )
        username_list = list(User.objects.values_list('username', flat=True))
        username = cleaned_data.get('username')
        if username in username_list:
            raise forms.ValidationError(
                'This name has exist, please choose another name.'
            )

    def clean_password(self):
        encrypt_password = make_password(self.cleaned_data['password'])
        if encrypt_password:
            return encrypt_password
        else:
            raise forms.ValidationError(
                'Password encryption fail, please choose another password'
            )


class MovieForm(forms.ModelForm):

    class Meta:
        #    favorite_colors = forms.MultipleChoiceField(
        #     required=False,
        #     widget=forms.CheckboxSelectMultiple,
        #     choices=FAVORITE_COLORS_CHOICES,
        # )

        
        model = Movie
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your movie name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Movie description', 'rows': '3',}),
            'release_date': forms.SelectDateWidget(years=range(datetime.today().year, 1800, -1), attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'custom-select d-block w-100',}),
            'actors': forms.CheckboxSelectMultiple,
            'logo': forms.FileInput(attrs={'class': 'custom-file-input',}),
        }


class ActorForm(forms.ModelForm):  
    
    class Meta:
        model = Actor
        fields = "__all__"
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',}),
            'birthdate': forms.SelectDateWidget(years=range(datetime.today().year, 1800, -1), attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'custom-select d-block w-100',}),
            'nationalities': forms.Select(attrs={'class': 'custom-select d-block w-100',}),
            'alive': forms.Select(attrs={'class': 'custom-select d-block w-100',}),
        }


class AwardForm(forms.ModelForm):
    
    class Meta:
        model = Award
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',}),
            'kind': forms.Select(attrs={'class': 'custom-select d-block w-100',}),
        }
