from .models import Localisation, Speciality, Person
from django.contrib.auth.hashers import check_password
from common.services import Repository, Service


class LocalisationRepository(Repository):
    def __init__(self, model=Localisation):
        super().__init__(model)


class LocalisationService(Service):
    def __init__(self, repository=LocalisationRepository()):
        super().__init__(repository)


class SpecialityRepository(Repository):
    def __init__(self, model=Speciality):
        super().__init__(model)


class PersonRepository(Repository):

    def __init__(self, model=Person):
        super().__init__(model)


class SpecialityService(Service):

    def __init__(self, repository=SpecialityRepository()):
        super().__init__(repository=repository)


class PersonService(Service):

    def __init__(self, repository=PersonRepository()):
        super().__init__(repository=repository)

    def create(self, data: dict):
        localisation = Localisation.objects.filter(**data['localisation'])
        localisation = Localisation.objects.create(**data['localisation']) if localisation is None else localisation
        if isinstance(localisation, Exception):
            return localisation
        else:
            data['localisation'] = localisation.id
            return super().create(data)

    @staticmethod
    def login(email, password):
        user = Person.objects.filter(email=email).first()
        if user is not None:
            if check_password(password=password, encoded=user.password):
                return user
            else:
                return Exception('كلمة السر غير صحيحة')
        else:
            return Exception('الحساب غير موجود')
