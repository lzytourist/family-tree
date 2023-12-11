from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.views.generic import ListView, DetailView

from .models import Person, ParentChildren
from .serializers import PersonSerializer, ParentChildrenSerializer


class PersonPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PersonView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'name', 'dob', 'dod', 'nationality']
    pagination_class = PersonPagination

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
        person = Person.objects.filter(pk=kwargs.get('pk')).get()
        children = Person.objects.filter(
            parent__parent_id=kwargs.get('pk')
        )
        serializer = PersonSerializer(children, many=True)
        data = {
            **PersonSerializer(person).data,
            'children': serializer.data
        }
        return Response(data=data)


class FamilyView(ListView):
    queryset = Person.objects.all()
    template_name = 'family.html'
