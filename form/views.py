from django.urls import path
from rest_framework.response import Response

from common.views import ViewSet
from .models import AgeRangeSerializer, DomainSerializer, PatientSerializer, QuestionSerializer, ResponseSerializer, \
    ScoreSerializer
from .services import AgeRangeService, DomainService, PatientService, QuestionService, ResponseService, ScoreService


class AgeRangeViewSet(ViewSet):
    def __init__(self, service=AgeRangeService(), serializer_class=AgeRangeSerializer, error_message='',
                 not_found_message='', required_fields=('label', 'minimumAge', 'maximumAge'),
                 fields=('label', 'minimumAge', 'maximumAge'), **kwargs):
        super().__init__(service=service, serializer_class=serializer_class, error_message=error_message,
                         not_found_message=not_found_message, required_fields=required_fields, fields=fields, **kwargs)


class PatientViewSet(ViewSet):

    def __init__(self, service=PatientService(), serializer_class=PatientSerializer, error_message='',
                 not_found_message='', required_fields=('age',), fields=('age', 'person_id'), **kwargs):
        super().__init__(service=service, serializer_class=serializer_class, error_message=error_message,
                         not_found_message=not_found_message, required_fields=required_fields, fields=fields,
                         **kwargs)


class QuestionViewSet(ViewSet):
    def __init__(self, service=QuestionService(), serializer_class=QuestionSerializer, error_message='',
                 not_found_message='', required_fields=('domain', 'ageRange', 'label'),
                 fields=('domain', 'ageRange', 'label'), **kwargs):
        super().__init__(service, serializer_class, error_message=error_message, not_found_message=not_found_message,
                         required_fields=required_fields, fields=fields, **kwargs)


class DomainViewSet(ViewSet):
    def __init__(self, service=DomainService(), serializer_class=DomainSerializer, error_message='',
                 not_found_message='', required_fields=('name', ), fields=('name', ), **kwargs):
        super().__init__(service=service, serializer_class=serializer_class, error_message=error_message,
                         not_found_message=not_found_message, required_fields=required_fields, fields=fields, **kwargs)
        self.age_range_service = AgeRangeService()

    def retrieve(self, request, pk=None, *args, **kwargs):
        domain_object = self.service.retrieve(pk)
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


class ResponseViewSet(ViewSet):
    def __init__(self, service=ResponseService(), serializer_class=ResponseSerializer, error_message='',
                 not_found_message='', required_fields=('question_id', 'patient_id', 'value'),
                 fields=('question_id', 'patient_id', 'value'), **kwargs):
        super().__init__(service=service, serializer_class=serializer_class, error_message=error_message,
                         not_found_message=not_found_message, required_fields=required_fields, fields=fields, **kwargs)


class ScoreViewSet(ViewSet):
    def __init__(self, service=ScoreService(), serializer_class=ScoreSerializer, error_message='', not_found_message='',
                 **kwargs):
        super().__init__(service=service, serializer_class=serializer_class, error_message=error_message,
                         not_found_message=not_found_message, **kwargs)

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
