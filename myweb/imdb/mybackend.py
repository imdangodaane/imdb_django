from imdb.models import MyUser, CustomUser
from django.contrib.auth.hashers import check_password

class MyBackend:
    def authenticate(self, request, username=None, password=None):
        """
        The authenticate method takes a request argument and credentials
        as keyword arguments.

        Either way, authenticate() should check the credentials it gets
        and return a user object that matches those credentials if the
        credentials are valid. If they’re not valid, it should return None.
        """
        username_valid = (username in list(CustomUser.objects.values_list('username', flat=True)))
        if username_valid:
            try:
                user = CustomUser.objects.get(username=username)
                password_valid = check_password(password, user.password)
                if password_valid:
                    return user
            except CustomUser.DoesNotExist:
                return None
        return None

    def get_user(self, username):
        """
        The get_user method takes a user_id – which could be a username,
        database ID or whatever, but has to be the primary key of your
        user object – and returns a user object or None.
        """
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None