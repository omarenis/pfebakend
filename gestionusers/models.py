from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import CharField, EmailField, Model, TextField
from rest_framework.serializers import ModelSerializer


class UserManager(BaseUserManager):
    def create_user(self, name, familyName, cin, telephone, email, password):
        try:
            user = Person(name=name, familyName=familyName, cin=cin, telephone=telephone,
                          email=self.normalize_email(email), accountId=None)
            user.username = name + ' ' + familyName
            user.set_password(password)
            user.save()
            return user
        except Exception as exception:
            print(exception)
            return exception


class Speciality(Model):
    title = TextField(unique=True)
    description = TextField(null=True)
    photo = TextField(null=True)

    class Meta:
        db_table = 'specialities'


class Person(AbstractUser):
    objects: UserManager = UserManager()
    name: TextField = TextField(null=False)
    familyName: TextField = TextField(null=False)
    cin: CharField = CharField(max_length=255, null=False, unique=True)
    email: EmailField = EmailField(null=False, unique=True)
    telephone: CharField = CharField(max_length=255, null=False, unique=True)
    password: TextField = TextField(null=False)
    typeUser: TextField = TextField(null=False, choices=[('teacher', 'Teacher'), ('instructor', 'Inscructor')],
                                    db_column='type_user')
    accountId: TextField = TextField(unique=True, null=True, db_column='account_id')

    class Meta:
        db_table = 'persons'


class SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'familyName', 'cin', 'email', 'telephone']
