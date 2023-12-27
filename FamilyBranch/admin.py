from django.contrib import admin

from .models import Person

admin.site.site_header = 'Family Tree'


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
    list_filter = ('user', 'gender', 'nationality')
    empty_value_display = 'N/A'

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return super().get_list_filter(request)
        return 'gender', 'nationality',

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = super(PersonAdmin, self).get_fieldsets(request, obj)
        else:
            fieldsets = (
                (None, {
                    'fields': ['name', 'gender']
                }),
                ('Additional info', {
                    'fields': ('father', 'mother', 'dob', 'date_of_death', 'nationality')
                }),
            )
        return fieldsets

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request).select_related('father', 'mother')
        return super().get_queryset(request).filter(user__id=request.user.pk).select_related('father', 'mother')

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user_id = request.user.pk
        return super(PersonAdmin, self).save_model(request, obj, form, change)

    def get_search_results(self, request, queryset, search_term):
        if request.GET.get('field_name') == 'father':
            return queryset.filter(gender=Person.Gender.MALE).filter(name__icontains=search_term).order_by(
                'name'), False
        elif request.GET.get('field_name') == 'mother':
            return queryset.filter(gender=Person.Gender.FEMALE).filter(name__icontains=search_term).order_by(
                'name'), False
        return super().get_search_results(request, queryset, search_term)


admin.site.register(Person, PersonAdmin)
