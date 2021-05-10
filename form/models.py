from django.db.models import BooleanField, CASCADE, ForeignKey, Model, TextField, IntegerField
from rest_framework.serializers import ModelSerializer
from gestionusers.models import Person


class Domain(Model):
    name = TextField(null=False)

    class Meta:
        db_table = 'domain'


class AgeRange(Model):
    label = TextField(unique=True)
    minimumAge = IntegerField(db_column='minimum_age')
    maximumAge = IntegerField(db_column='maximum_age')

    class Meta:
        db_table = 'age_range'


class Question(Model):
    label = TextField(null=False, unique=True)
    ageRange = ForeignKey(AgeRange, db_column='age_range', on_delete=CASCADE, null=True)
    domain = ForeignKey(Domain, db_column='domain', on_delete=CASCADE, null=True)

    class Meta:
        db_table = 'question'


class Patient(Model):
    blockId = TextField(unique=True, null=True, db_column='block_id')
    person = ForeignKey(to=Person, on_delete=CASCADE, db_column='person', null=True)
    age = IntegerField(null=False)

    class Meta:
        db_table = 'patient'


class Response(Model):
    question = ForeignKey(Question, on_delete=CASCADE)
    patient = ForeignKey(Patient, on_delete=CASCADE)
    value = BooleanField(null=False)

    class Meta:
        db_table = 'response'
        unique_together = (('question', 'patient'),)


class Score(Model):
    patient = ForeignKey(to=Patient, on_delete=CASCADE, null=False)
    domain = ForeignKey(to=Domain, on_delete=CASCADE, null=False)
    value = IntegerField(null=False, default=0)

    class Meta:
        db_table = 'score'
        unique_together = (('domain', 'patient'),)


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'label', 'ageRange', 'domain']


class DomainSerializer(ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Domain
        fields = ['id', 'name', 'question_set']


class AgeRangeSerializer(ModelSerializer):
    question_set = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = AgeRange
        fields = ['id', 'label', 'minimumAge', 'maximumAge', 'question_set']


class ResponseSerializer(ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'patient_id', 'question_id', 'value']


class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'value', 'domain', 'patient']


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'age']
