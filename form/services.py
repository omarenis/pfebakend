from .models import Patient, Question, Domain, Response, AgeRange, Score


class Repository(object):

    def __init__(self, model):
        self.model = model

    def list(self):
        return self.model.objects.all()

    def retrieve(self, _id: int):
        return self.model.objects.get(id=_id)

    def create(self, data: dict):
        try:
            return self.model.objects.create(**data)
        except Exception as exception:
            return exception

    def delete(self, _id: int):
        try:
            self.model.objects.get(id=_id).delete()
            return None
        except Exception as exception:
            return exception


class DomainRepository(Repository):
    def __init__(self):
        super().__init__(model=Domain)


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


class Service(object):

    def __init__(self, repository):
        self.repository = repository

    def list(self):
        return self.repository.list()

    def retrieve(self, _id: int):
        return self.repository.retrieve(_id)

    def create(self, data: dict):
        return self.repository.create(data=data)

    def delete(self, _id: int):
        return self.repository.delete(_id)


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
