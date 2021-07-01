from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import CharField, EmailField, FloatField, ForeignKey, ImageField, Model, PROTECT, TextField
from rest_framework.serializers import ModelSerializer


class UserManager(BaseUserManager):
    def create(self, name, family_name, cin, telephone, email, password, localisation=None, *args, **kwargs):
        try:
            user = Person(name=name, familyName=family_name, cin=cin, telephone=telephone,
                          email=self.normalize_email(email), accountId=None, localisation_id=localisation)
            user.username = name + ' ' + family_name
            user.set_password(password)
            user.save()
            return user
        except Exception as exception:
            return exception


class Localisation(Model):
    governorat: TextField = TextField(null=False)
    delegation: TextField = TextField(null=False)
    locality: TextField = TextField(null=False)
    zipCode: FloatField = FloatField(null=False)

    class Meta:
        db_table = 'localisations'
        unique_together = (('governorat', 'delegation', 'locality', 'zipCode'),)


class Speciality(Model):
    title = TextField(unique=True)
    description = TextField(null=True)
    photo = ImageField(null=True, upload_to='images')

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
    localisation = ForeignKey(Localisation, on_delete=PROTECT, db_column='localisation', null=True)

    class Meta:
        db_table = 'persons'


class SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'


class LocalisationSerilizer(ModelSerializer):

    class Meta:
        model = Localisation
        exclude = ('persons_set', )


class PersonSerializer(ModelSerializer):
    localisation = LocalisationSerilizer(read_only=True, allow_null=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'familyName', 'cin', 'email', 'telephone', 'localisation']
