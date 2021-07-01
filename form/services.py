from common.services import Repository, Service
from .models import Patient, Question, Domain, Response, AgeRange, Score


class DomainRepository(Repository):
    def __init__(self, model=Domain):
        super().__init__(model=model)


class PatientRepository(Repository):

    def __init__(self):
        super().__init__(model=Patient)


class QuestionRepository(Repository):
    def __init__(self):
        super().__init__(model=Question)


class ResponseRepository(Repository):
    def __init__(self):
        super().__init__(model=Response)


class ScoreRepository(Repository):
    def __init__(self):
        super().__init__(model=Score)


class AgeRangeRepository(Repository):
    def __init__(self):
        super().__init__(model=AgeRange)

    @staticmethod
    def get_age_range_by_age(age: int):
        return AgeRange.objects.filter(minimumAge__lte=age, maximumAge__gt=age).first()


class DomainService(Service):
    def __init__(self, repository=DomainRepository()):
        super().__init__(repository=repository)


class AgeRangeService(Service):
    def __init__(self, repository=AgeRangeRepository()):
        super().__init__(repository=repository)

    def retrieve(self, _id: int = None, age: int = None):
        if age is None and _id is not None:
            return self.repository.retrieve(_id)
        else:
            return self.repository.get_age_range_by_age(age)


class ScoreService(Service):
    def __init__(self, repository=ScoreRepository()):
        super().__init__(repository)

    def list(self, patient_id=None):
        if patient_id is None:
            return super().list()
        else:
            return self.repository.model.objects.filter(patient_id=patient_id)


class PatientService(Service):
    def __init__(self, repository=PatientRepository()):
        super().__init__(repository=repository)
        self.score_service = ScoreService()


class ResponseService(Service):
    def __init__(self, repository=ResponseRepository()):
        super().__init__(repository)


class QuestionService(Service):
    def __init__(self, repository=QuestionRepository()):
        super().__init__(repository)
