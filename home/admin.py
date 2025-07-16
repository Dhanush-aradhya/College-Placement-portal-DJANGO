# home/admin.py
from django.contrib import admin
from .models import StudentProfile, Domain, Language # Add Language

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('usn', 'full_name', 'user', 'college_email', 'department', 'batch', 'tenth_percentage', 'pre_university_qualification_type', 'pre_university_percentage') # Added new fields
    search_fields = ('usn', 'full_name', 'user__username', 'college_email')
    list_filter = ('department', 'batch', 'current_year', 'pre_university_qualification_type') # Added new filter
    filter_horizontal = ('domains', 'languages_known',) # Make M2M fields easier to manage

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Domain) # Assuming Domain is already registered like this
admin.site.register(Language, LanguageAdmin)