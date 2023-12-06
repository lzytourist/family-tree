from django_filters.rest_framework.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Person, ParentChildren
from .serializers import PersonSerializer, ParentChildrenSerializer


class PersonView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'name', 'dob', 'dod', 'nationality']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ParentChildrenView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ParentChildren.objects.all()
    serializer_class = ParentChildrenSerializer


class ChildrenView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ParentChildren.objects.all()
    serializer_class = ParentChildrenSerializer

    def retrieve(self, request, *args, **kwargs):
        children = Person.objects.filter(
            parent__parent_id=kwargs.get('pk')
        )
        serializer = PersonSerializer(children, many=True)
        return Response(data=serializer.data)
