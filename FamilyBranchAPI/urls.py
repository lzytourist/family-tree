from django.urls import path
from .views import PersonListView, PersonSingleView, PersonRelationView

urlpatterns = [
    path('people', PersonListView.as_view()),
    path('people/<int:pk>', PersonSingleView.as_view()),
    path('people/<int:pk>/relation', PersonRelationView.as_view())
]
