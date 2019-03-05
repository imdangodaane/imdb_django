from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from imdb.models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(label='Password', widget=forms.PasswordInput)
        password_confirm = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
        model = CustomUser
        fields = ('username', 'email_address')

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password don't match.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_password(self):
        return self.initial['password']


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email_address', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email_address',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'class': ('wide',),
            'fields': ('username', 'password', 'password_confirm', 'email_address',)}
        )
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_hozirontal = ()

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.unregister(Group)