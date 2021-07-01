from typing import Type

from django.contrib.auth.models import AbstractUser
from django.db.models import Model


class Repository(object):

    def __init__(self, model: Type[Model or AbstractUser]):
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

    def put(self, _id: int, data: dict):
        _object = self.retrieve(_id)
        if _object is None:
            return Exception('object not found')
        else:
            for i in data:
                if getattr(_object, i) != data[i]:
                    setattr(_object, i, data[i])
        _object.save()
        return _object


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

    def retreive(self, _id: int, data: dict):
        return self.repository.put(_id=_id, data=data)
