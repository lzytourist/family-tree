from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)

router.register("people", views.PersonView)

urlpatterns = [
    path('people/relation', views.ParentChildrenView.as_view({
      'post': 'create',
    })),
    path('people/relation/<int:pk>', views.ParentChildrenView.as_view({
      'get': 'retrieve',
      'delete': 'destroy'
    })),
    path('people/<int:pk>/children', views.ChildrenView.as_view({
        'get': 'retrieve'
    })),
] + router.urls
