from .models import Patient, Question, Domain, Response, AgeRange, Score


class Repository(object):

    def __init__(self, model):
        self.model = model

    def list(self):
        return self.model.objects.all()

    def retrieve(self, _id: int):
        return self.model.objects.get(_id=id)

    def create(self, data: dict):
        return self.model.objects.create(**data)

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
