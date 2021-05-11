from django.urls import path
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import PersonSerializer, SpecialitySerializer
from .services import PersonService, SpecialityService
from rest_framework_simplejwt.tokens import RefreshToken


class SpecialityController(ModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speciality_serializer = SpecialitySerializer
        self.speciality_service = SpecialityService()

    def list(self, request, **kwargs):
        speciality_list = self.speciality_service.list()
        response = []
        if len(speciality_list) != 0:
            for i in self.speciality_service.list():
                response.append(self.speciality_serializer(data=i).data)
        return Response(data=response, status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        speciality = self.speciality_service.retrieve(pk)
        if speciality is None:
            return Response(data={"error": "user not found"}, status=404)
        else:
            return Response(data=self.speciality_serializer(data=speciality).data, status=200)

    def create(self, request, *args, **kwargs):
        if request.data.get('title') is None:
            return Response(data={'error': 'title required'}, status=500)
        if request.data.get('description') is None:
            return Response(data={'error': 'description required'}, status=500)
        if request.data.get('image') is None:
            return Response(data={'error': 'image required'}, status=500)
        return SpecialitySerializer(self.speciality_service.create(request.data)).data


class PersonController(ModelViewSet):
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes.append(IsAdminUser)
        elif self.action == 'retrieve':
            permission_classes.append(IsAuthenticated)
        elif self.action == 'signup' or self.action == 'login':
            permission_classes.append(AllowAny)
        return [permission() for permission in permission_classes if permission is not None]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.person_serializer = PersonSerializer
        self.person_service = PersonService()

    def list(self, request, **kwargs):
        person_list = []
        for i in self.person_service.list():
            person_list.append(self.person_serializer(data=i).data)
        return Response(data=person_list, status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.person_service.retrieve(pk)
        if user is None:
            return Response(data={"error": "user not found"}, status=404)
        else:
            return Response(data=self.person_serializer(data=user).data, status=200)

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
        user = self.person_service.add(request.data)
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


users_list = PersonController.as_view({
    'get': 'list',
    'post': 'create'
})

user_retrieve_update_delete = PersonController.as_view({
    'delete': 'delete'
})
login = PersonController.as_view({
    'post': 'login'
})
signup = PersonController.as_view({
    'post': 'signup'
})
urlpatterns = [
    path('', users_list),
    path('<int:user_id>', user_retrieve_update_delete),
    path('login', login),
    path('signup', signup)
]
