from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from app.core.serializers import CustomTokenObtainPairSerializer, AuthCustomTokenSerializer

from rest_framework.authtoken.models import Token

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rest_framework import status, parsers, views, renderers
from rest_framework.response import Response

from django.contrib.auth import get_user_model


from .forms import NewUserForm


User = get_user_model()

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        req_data = request.data.copy()
        try:
            current_user = User.objects.get(username=req_data['username'])
        except User.DoesNotExist:
            raise AuthenticationFailed('O usuário não existe')
        if current_user is not None:
            if not current_user.is_active:
                raise Exception('Você precisa ativar a conta clicando no link enviado para o seu email')
            else:
                pass
        serializer = self.get_serializer(data=request.data)
        try:
            # error
            serializer.is_valid()
        except Exception as e:
            print(e)
            # raise InvalidUser(e.args[0]) 
        except TokenError as e:
            print(e)
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    
class ObtainAuthToken(views.APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key
        }

        return Response(content)
