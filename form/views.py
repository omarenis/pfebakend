from django.urls import path
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import AgeRangeSerializer, DomainSerializer, PatientSerializer, QuestionSerializer, ResponseSerializer, \
    ScoreSerializer
from .services import AgeRangeService, DomainService, PatientService, QuestionService, ResponseService, ScoreService


class AgeRangeViewSet(ModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AgeRangeService()

    def list(self, request, *args, **kwargs):
        age_range_list = self.service.list()
        if len(age_range_list) == 0:
            return Response(data={'response': 'pas de patients dans ce moment'}, status=200)
        return Response(data=[PatientSerializer(i).data for i in age_range_list], status=200)

    def create(self, request, *args, **kwargs):

        if request.data.get("label") is None:
            return Response(data={'error': 'label must be provided'}, status=400)
        if request.data.get('minimumAge') is None:
            return Response(data={'error': 'minimumAge must be provided'}, status=400)
        if request.data.get('maximumAge') is None:
            return Response(data={'error': 'maximumAge must be provided'}, status=400)
        age_range = self.service.create(request.data)
        if isinstance(age_range, Exception):
            return Response(data={'error': str(age_range)}, status=500)
        return Response(data=AgeRangeSerializer(age_range).data, status=201)

    def delete(self, request, pk=None, *args, **kwargs):

        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=400)
        deleted = self.service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=400)
        return Response(data={'response': True}, status=200)


class PatientViewSet(ModelViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PatientService()

    def list(self, request, *args, **kwargs):
        patient_list = self.service.list()
        if len(patient_list) == 0:
            return Response(data={'response': 'pas de patients dans ce moment'}, status=200)
        return Response(data=[PatientSerializer(i).data for i in patient_list], status=200)

    def create(self, request, *args, **kwargs):
        if request.data.get('age') is None:
            return Response(data={'error': 'patient has age'}, status=400)
        else:
            patient_object = self.service.create(
                {
                    'age': request.data.get('age'),
                    'person_id': request.data.get('person_id')
                }
            )
            if isinstance(patient_object, Exception):
                return Response(data={'error': str(patient_object)}, status=500)
            return Response(data=PatientSerializer(patient_object).data, status=201)


class QuestionViewSet(ModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.question_service = QuestionService()

    def list(self, request, *args, **kwargs):
        question_list = self.question_service.list()
        if len(question_list) == 0:
            return Response(data=[], status=200)
        return Response(data=[QuestionSerializer(i).data for i in question_list], status=200)

    def create(self, request, *args, **kwargs):
        if request.data.get('ageRange') is None:
            return Response(data={'error': 'age range not provided'}, status=400)
        elif request.data.get('domain') is None:
            return Response(data={'error': 'domain not provided'}, status=400)
        elif request.data.get('label') is None:
            return Response(data={'error': 'label not provided'}, status=400)
        else:
            question_data = dict()
            question_data['domain_id'] = request.data.get('domain')
            question_data['ageRange_id'] = request.data.get('ageRange')
            question_data['label'] = request.data.get('label')
            question_object = self.question_service.create(question_data)
            if isinstance(question_object, Exception):
                return Response(data={'error': str(question_object)}, status=500)
            return Response(data=QuestionSerializer(question_object).data, status=201)

    def update(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=400)
        question_object = self.question_service.retrieve(_id=pk)
        if question_object is None:
            return Response(data={'error': 'question not found'}, status=404)
        return Response(data=QuestionSerializer(question_object).data, status=201)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=400)
        deleted = self.question_service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=400)
        return Response(data={'response': True}, status=200)


class DomainViewSet(ModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain_service = DomainService()
        self.age_range_service = AgeRangeService()

    def list(self, request, *args, **kwargs):
        domain_list = self.domain_service.list()
        if len(domain_list) == 0:
            return Response(data={'response': 'pas de domaines dans ce moment'}, status=200)
        return Response(data=[DomainSerializer(i).data for i in domain_list], status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        domain_object = self.domain_service.retrieve(pk)
        if domain_object is None:
            return Response(data={'error': 'domain not found'}, status=404)
        age = request.GET.get('age')
        if age is not None:
            age = int(request.GET.get('age'))
            age_range = self.age_range_service.retrieve(age=age)
            if age_range is None:
                return Response(data={'response': 'age range not found for that age'}, status=404)
            question_set = domain_object.question_set.filter(ageRange_id=age_range.id)
            response = {
                'id': domain_object.id,
                'name': domain_object.name,
                'question_set': [QuestionSerializer(i).data for i in question_set],
            }
            return Response(data=response, status=200)
        return Response(data=DomainSerializer(domain_object).data, status=200)

    def delete(self, request, pk=None, *args, **kwargs):
        deleted = self.domain_service.delete(_id=pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=400)
        return Response(data={'response': True}, status=200)


class ResponseViewSet(ModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ResponseService()

    def list(self, request, *args, **kwargs):
        response_list = self.service.list()
        if len(response_list) == 0:
            return Response(data={'response': 'pas de questions dans ce moment'}, status=200)
        return Response(data=[DomainSerializer(i).data for i in response_list], status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        response_object = self.service.retrieve(pk)
        print(response_object)
        if response_object is None:
            return Response(data={'error': 'domain not found'}, status=404)
        return Response(data=DomainSerializer(response_object).data, status=200)

    def create(self, request, *args, **kwargs):
        if request.data.get("question") is None:
            return Response(data={'error': 'question must be provided'}, status=400)
        if request.data.get('patient') is None:
            return Response(data={'error': 'patient must be provided'}, status=400)
        if request.data.get('value') is None:
            return Response(data={'error': 'value must be provided'}, status=400)
        response_data = dict(question_id=request.data.get('question'), patient_id=request.data.get('patient'),
                             value=request.data.get('value'))
        response_object = self.service.create(response_data)
        if isinstance(response_object, Exception):
            return Response(data={'error': str(response_object)}, status=500)
        return Response(data=ResponseSerializer(response_object).data, status=201)

    def delete(self, request, pk=None, *args, **kwargs):
        deleted = self.service.delete(_id=pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=400)
        return Response(data={'response': True}, status=200)


class ScoreViewSet(ModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ScoreService()

    def list(self, request, *args, **kwargs):
        score_list = self.service.list(request.GET.get('patientId'))
        if len(score_list) == 0:
            return Response(data={'response': 'pas de scores dans ce moment'}, status=200)
        return Response(data=[ScoreSerializer(i).data for i in score_list], status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        score_object = self.service.retrieve(pk)
        print(score_object)
        if score_object is None:
            return Response(data={'error': 'score not found'}, status=404)
        return Response(data=ScoreSerializer(score_object).data, status=200)

    def create(self, request, *args, **kwargs):
        print(request.data)
        if request.data.get("domain") is None:
            return Response(data={'error': 'domain must be provided'}, status=400)
        if request.data.get('patient') is None:
            return Response(data={'error': 'patient must be provided'}, status=400)
        if request.data.get('value') is None:
            return Response(data={'error': 'value must be provided'}, status=400)
        score_data = dict(domain_id=request.data.get('domain'), patient_id=request.data.get('patient'),
                          value=request.data.get('value'))
        score_object = self.service.create(score_data)
        if isinstance(score_object, Exception):
            return Response(data={'error': str(score_object)}, status=500)
        return Response(data=ScoreSerializer(score_object).data, status=201)

    def delete(self, request, pk=None, *args, **kwargs):
        deleted = self.service.delete(_id=pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=400)
        return Response(data={'response': True}, status=200)


age_ranges = AgeRangeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

age_range = AgeRangeViewSet.as_view({
    'delete': 'delete'
})

questions = QuestionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
question = QuestionViewSet.as_view({
    'get': 'retrieve',
})
patients = PatientViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

domains = DomainViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
domain = DomainViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'delete'
})
responses = ResponseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
scores = ScoreViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('questions', questions),
    path('questions/<int:pk>', question),
    path('patients', patients),
    path('domains', domains),
    path('domains/<int:pk>', domain),
    path('responses', responses),
    path('scores', scores),
    path('ageRanges', age_ranges),
    path('ageRanges/<int:pk>', age_range)
]
