from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

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
