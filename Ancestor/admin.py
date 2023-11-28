from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import Person, ParentChildren


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ["name", "dob", "dod", "gender", "nationality"]
    fields = ["user", "name", "gender", "nationality", ("dob", "dod")]
    empty_value_display = "N/A"
    search_fields = list_display
    list_filter = ["gender", "nationality"]

admin.site.register(Person, PersonAdmin)

class ParentChildrenAdmin(admin.ModelAdmin):
    model = ParentChildren
    list_display = ["get_parent", "get_children"]
    list_display_links = ["get_parent", "get_children"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('parent').select_related('children')

    def get_parent(self, obj):
        return obj.parent.name
    get_parent.short_description = "Parent"
    
    def get_children(self, obj):
        return obj.children.name
    get_children.short_description = "Children"

admin.site.register(ParentChildren, ParentChildrenAdmin)