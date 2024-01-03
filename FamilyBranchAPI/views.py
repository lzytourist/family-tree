from django.db.models.query import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from FamilyBranch.models import Person
from .serializers import PersonRelationSerializer, PersonSerializer


class PersonListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    search_fields = ['name', 'gender']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'gender', 'dob', 'date_of_death', 'father', 'mother', 'nationality']

    def get_queryset(self):
        if self.request.method == 'GET':
            self.queryset = self.queryset.select_related('father', 'mother')
        return self.queryset.filter(user=self.request.user)


class PersonSingleView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class PersonRelationView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            person = Person.objects.select_related('father', 'mother').filter(pk=kwargs.get('pk')).get()
            data = {
                **PersonRelationSerializer(person).data,
                'parents': [],
                'siblings': [],
            }

            if person.gender == Person.Gender.MALE:
                children = person.children_as_father.order_by('dob').all()
                data['children'] = PersonRelationSerializer(children, many=True).data
            else:
                children = person.children_as_mother.order_by('dob').all()
                data['children'] = PersonRelationSerializer(children, many=True).data

            if person.father_id:
                data['parents'].append(PersonRelationSerializer(person.father).data)
            if person.mother_id:
                data['parents'].append(PersonRelationSerializer(person.mother).data)

            siblings = Person.objects.filter(~Q(id=person.id)).filter(
                (Q(father_id__isnull=False) & Q(father_id=person.father_id)) |
                (Q(mother_id__isnull=False) & (Q(mother_id=person.mother_id)))
            ).order_by('dob').all()
            if siblings:
                data['siblings'] = PersonRelationSerializer(siblings, many=True).data
        except Person.DoesNotExist:
            return Response(data={
                'message': 'Not found'
            }, status=HTTP_404_NOT_FOUND)

        return Response(data=data)
