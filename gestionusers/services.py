from .models import Speciality, Person
import django.contrib.auth.password_validation as validators


class SpecialityRepository(object):

    @staticmethod
    def list():
        return Speciality.objects.all()

    @staticmethod
    def retrieve(speciality_id):
        return Speciality.objects.get(speciality_id)

    @staticmethod
    def create(speciality: dict):
        speciality_object = Speciality(name=speciality['name'], description=speciality.get('description'))
        speciality_object.save()
        return speciality_object

    @staticmethod
    def delete(speciality_id):
        return Speciality.objects.get(speciality_id).delete()


class PersonRepository(object):

    @staticmethod
    def list():
        return Person.objects.all()

    @staticmethod
    def get(user_id):
        return Person.objects.get(user_id)

    @staticmethod
    def create(person: dict):
        person_object = Person.objects.create_user(name=person['name'], familyName=person['familyName'],
                                                   cin=person['cin'], telephone=person['telephone'],
                                                   password=person['password'], email=person['email'])
        return person_object

    @staticmethod
    def delete(user_id):
        try:
            Person.objects.get(user_id).delete()
        except Exception as exception:
            return exception


class SpecialityService(object):

    def __init__(self):
        self.speciality_repository = SpecialityRepository()

    def list(self):
        return self.speciality_repository.list()

    def retrieve(self, speciality_id):
        return self.speciality_repository.retrieve(speciality_id)

    def add(self, speciality: dict):
        try:
            return self.speciality_repository.create(speciality=speciality)
        except Exception as exception:
            return exception

    def delete(self, speciality_id):
        try:
            self.speciality_repository.delete(speciality_id)
            return True
        except Exception as exception:
            print(exception)
            return False

    def create(self, speciality: dict):
        try:
            return self.speciality_repository.create(speciality)
        except Exception as exception:
            return exception


class PersonService(object):

    def __init__(self):
        self.person_repository = PersonRepository()

    def list(self):
        return self.person_repository.list()

    def retrieve(self, user_id):
        return self.person_repository.get(user_id)

    def add(self, person: dict):
        try:
            return self.person_repository.create(person=person)
        except Exception as exception:
            return exception

    def delete(self, user_id):
        try:
            self.person_repository.delete(user_id)
            return True
        except Exception as exception:
            print(exception)
            return False

    @staticmethod
    def login(email, password):
        user = Person.objects.filter(email=email).first()
        if user is not None:
            try:
                validators.validate_password(password=password, user=user)
                return user
            except Exception as exception:
                return exception
