from django.contrib import admin
from CompanyData.models import CompanyName
# Register your models here.
from django.utils.html import format_html

# admin.site.register(CompanyName)

@admin.register(CompanyName)
class CompanyNameAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'career_page_link', 'employee_strength')
    search_fields = ('company_name',)

    def career_page_link(self, obj):
        # Return a formatted HTML link for the career_page
        return format_html('<a href="{}" target="_blank">{}</a>', obj.career_page, obj.career_page)
    career_page_link.short_description = 'Career Page'