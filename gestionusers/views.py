from django.urls import path
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import PersonSerializer, SpecialitySerializer
from .services import PersonService, SpecialityService
from rest_framework_simplejwt.tokens import RefreshToken


class SpecialityViewSet(ModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speciality_serializer = SpecialitySerializer
        self.speciality_service = SpecialityService()

    def list(self, request, **kwargs):
        speciality_list = self.speciality_service.list()
        response = []
        if len(speciality_list) != 0:
            for i in speciality_list:
                response.append(self.speciality_serializer(i).data)
        return Response(data=response, status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        speciality = self.speciality_service.retrieve(pk)
        if speciality is None:
            return Response(data={"error": "user not found"}, status=404)
        else:
            return Response(data=self.speciality_serializer(data=speciality).data, status=200)

    def create(self, request, *args, **kwargs):
        print(request.data.get('title'))
        print(request.FILES.getlist('photo')[0])
        if request.data.get('title') is None:
            return Response(data={'error': 'title required'}, status=500)
        if request.data.get('description') is None:
            return Response(data={'error': 'description required'}, status=500)
        if request.FILES.getlist('photo') is None:
            return Response(data={'error': 'photo required'}, status=500)
        request.data['photo'] = request.FILES.getlist('photo')[0]
        speciality_object = self.speciality_service.create(request.data)
        if isinstance(speciality_object, Exception):
            return Response(data={'error': str(speciality_object)}, status=500)
        else:
            return Response(data=SpecialitySerializer(speciality_object).data, status=201)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            self.speciality_service.delete(speciality_id=pk)
            return Response(data={'response': True}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersonViewSet(ModelViewSet):
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
