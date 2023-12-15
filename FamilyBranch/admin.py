from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'father', 'mother')
    fieldsets = (
        (None, {
            'fields': ['user', 'name', 'gender']
        }),
        ('Additional info', {
            'fields': ('father', 'mother', 'dob', 'date_of_death', 'nationality')
        }),
    )
    search_fields = ('name', 'age', 'gender', 'father', 'mother')
    autocomplete_fields = ('user', 'father', 'mother')
    list_filter = ('user', 'gender')
    empty_value_display = 'N/A'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('father', 'mother')

    def get_search_results(self, request, queryset, search_term):
        if request.GET.get('field_name') == 'father':
            return queryset.filter(gender=Person.Gender.MALE).filter(name__icontains=search_term).order_by(
                'name'), False
        elif request.GET.get('field_name') == 'mother':
            return queryset.filter(gender=Person.Gender.FEMALE).filter(name__icontains=search_term).order_by(
                'name'), False
        return super().get_search_results(request, queryset, search_term)


admin.site.register(Person, PersonAdmin)
