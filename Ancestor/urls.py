from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)

router.register("people", views.PersonView)

urlpatterns = router.urls
