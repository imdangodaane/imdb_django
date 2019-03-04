from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import is_password_usable, make_password, check_password
from imdb.models import Login, MyUser, Movie, Actor, Award
from datetime import datetime

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)


class LoginForm(forms.ModelForm):
    # user_name = forms.CharField(label='Username', max_length=100, widget=forms.TextInput)
    # password = forms.CharField(widget=forms.PasswordInput)
    # message = forms.CharField(widget=forms.Textarea)
    # date = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    # favorite_colors = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=FAVORITE_COLORS_CHOICES,
    # )

    class Meta:
        model = Login
        fields = ('username', 'password')
        labels = {
            'username': _('Username'),
            'password': _('Password'),
        }
        widgets = {
            'password': forms.PasswordInput,
        }
        help_texts = {
            # 'username': _('Your username.'),
            # 'password': _('Your password.'),
        }
        error_messages = {
            'username': {
                'max_length': _("This username is too long.")
            },
        }


class SignupForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('username', 'password', 'password_confirm', 'email_address')

        labels = {
            'username' : _('Username *'),
            'email_address': _('Email address *'),
            'password': _('Password *',)
        }
        widgets = {
            'password': forms.PasswordInput,
            'password_confirm': forms.PasswordInput,
            'email_address': forms.EmailInput,
        }
        help_texts = {
            'username': _('Username may only contain alphanumeric characters or single hyphens, and cannot begin or end with a hyphen.'),
            'email_address': _('We’ll occasionally send updates about your account to this inbox. We’ll never share your email address with anyone.'),
            'password': _("Make sure it's more than 15 characters OR at least 8 characters including a number and a lowercase letter."),
            'password_confirm': _("Re-enter your password.",)
        }
        error_messages = {
            'username': {
                'max_length': _("This username is too long.")
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
        USERNAME_LIST = list(MyUser.objects.values_list('username', flat=True))
        username = cleaned_data.get('username')
        if username in USERNAME_LIST:
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
        CUR_YEAR = datetime.today().year
        YEAR_RANGE = tuple([i for i in range(1900, CUR_YEAR + 1)])
        #    favorite_colors = forms.MultipleChoiceField(
        #     required=False,
        #     widget=forms.CheckboxSelectMultiple,
        #     choices=FAVORITE_COLORS_CHOICES,
        # )
        
        model = Movie
        fields = "__all__"
        widgets = {
            'release_date': forms.SelectDateWidget(years=YEAR_RANGE),
            'actors': forms.CheckboxSelectMultiple,
        }


class ActorForm(forms.ModelForm):  
    
    class Meta:
        CUR_YEAR = datetime.today().year
        YEAR_RANGE = tuple([i for i in range(1980, CUR_YEAR + 1)])
        model = Actor
        fields = "__all__"
        widgets = {
            'birthdate': forms.SelectDateWidget(years=YEAR_RANGE),
        }


class AwardForm(forms.ModelForm):
    
    class Meta:
        model = Award
        fields = "__all__"
