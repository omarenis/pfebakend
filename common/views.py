from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class ViewSet(ModelViewSet):

    def __init__(self, service, serializer_class, required_fields: tuple,
                 fields: tuple,  error_message='', not_found_message='', **kwargs):
        super().__init__(**kwargs)
        self.service = service
        self.serializer_class = serializer_class
        self.error_message = error_message
        self.not_found_message = not_found_message
        self.required_fields = required_fields
        self.fields = fields

    def list(self, request, *args, **kwargs):
        _objects = self.service.list()
        if not _objects:
            return Response(data=[], status=status.HTTP_200_OK)
        return Response(data=[self.serializer_class(i).data for i in _objects], status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        attrs = list(request.data.keys())
        for i in attrs:
            if i not in self.fields:
                return Response(data={'error': f'{i} is not an attribute for the model'},
                                status=status.HTTP_400_BAD_REQUEST)
        for i in self.required_fields:
            if request.data.get(i) is None:
                return Response(data={'error': f'{i} is required'}, status=status.HTTP_400_BAD_REQUEST)
        _object = self.service.create(request.data)
        if isinstance(_object, Exception):
            return Response(data={"error": str(_object)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=self.serializer_class(_object).data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=status.HTTP_400_BAD_REQUEST)
        deleted = self.service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'response': True}, status=200)

    def update(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=status.HTTP_400_BAD_REQUEST)
        _object = self.service.retrieve(_id=pk)
        if _object is None:
            return Response(data={'error': 'question not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=self.serializer_class(_object).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        _object = self.service.retrieve(pk)
        if _object is None:
            return Response(data={'error': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=self.serializer_class(_object).data, status=status.HTTP_200_OK)
