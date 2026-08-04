from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        login = username or kwargs.get(get_user_model().USERNAME_FIELD)
        if login is None or password is None:
            return None

        UserModel = get_user_model()
        lookup = {"email__iexact": login} if "@" in login else {"username": login}

        try:
            user = UserModel._default_manager.get(**lookup)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
