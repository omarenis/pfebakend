from django.urls import path
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.views import ViewSet
from .models import PersonSerializer, SpecialitySerializer
from .services import PersonService, SpecialityService


class SpecialityViewSet(ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(service=SpecialityService(), serializer_class=SpecialitySerializer,
                         required_fields=('title', 'description', 'photo'), fields=('title', 'description', 'photo'),
                         *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.data.get('title') is None:
            return Response(data={'error': 'title required'}, status=500)
        if request.data.get('description') is None:
            return Response(data={'error': 'description required'}, status=500)
        if request.FILES.getlist('photo') is None:
            return Response(data={'error': 'photo required'}, status=500)
        request.data['photo'] = request.FILES.getlist('photo')[0]
        speciality_object = self.service.create(request.data)
        if isinstance(speciality_object, Exception):
            return Response(data={'error': str(speciality_object)}, status=500)
        else:
            return Response(data=SpecialitySerializer(speciality_object).data, status=201)


class PersonViewSet(ViewSet):

    def __init__(self, service=SpecialityService(), serializer_class=PersonSerializer,
                 required_fields=('name', 'family_name', 'cin', 'telephone', 'email', 'password'),
                 fields=('name', 'family_name', 'cin', 'telephone', 'email', 'password', 'localisation_id'), **kwargs):
        super().__init__(service=service, serializer_class=serializer_class, required_fields=required_fields,
                         fields=fields, **kwargs)
        self.person_serializer = PersonSerializer
        self.person_service = PersonService()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes.append(IsAdminUser)
        elif self.action == 'retrieve':
            permission_classes.append(IsAuthenticated)
        elif self.action == 'signup' or self.action == 'login':
            permission_classes.append(AllowAny)
        return [permission() for permission in permission_classes if permission is not None]

    def login(self, request):
        email = request.data.get('email')
        if email is None:
            return Response(data={"error": "email not found"}, status=400)
        password = request.data.get('password')
        if password is None:
            return Response(data={"error": "password not found"}, status=400)
        user = self.person_service.login(email, password)
        if isinstance(user, Exception):
            return Response(data={"error": str(user)}, status=500)
        token = RefreshToken.for_user(user=user)
        return Response(data={
            "access": str(token.access_token),
            "refresh": str(token),
            "userId": user.id
        })

    def signup(self, request):
        user = self.service.create(request.data)
        if isinstance(user, Exception):
            print(user)
            return Response(data={"error": str(user)}, status=500)
        else:
            token = RefreshToken.for_user(user=user)
            return Response(data={
                "access": str(token.access_token),
                "refresh": str(token),
                "userId": user.id
            })


users_list = PersonViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_retrieve_update_delete = PersonViewSet.as_view({
    'delete': 'delete'
})
login = PersonViewSet.as_view({
    'post': 'login'
})
signup = PersonViewSet.as_view({
    'post': 'signup'
})
specialties = SpecialityViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
specialty = SpecialityViewSet.as_view({
    'delete': 'delete'
})
urlpatterns = [
    path('users', users_list),
    path('users/<int:user_id>', user_retrieve_update_delete),
    path('users/login', login),
    path('users/signup', signup),
    path('specialties', specialties),
    path('specialties/<int:speciality_id>', specialty)
]
