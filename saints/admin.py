from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Saint,
    HagiographyOrWrittenSource,
    AspectsOfCult,
    ArchaeologicalAndArchitecturalEvidence,
    Image,
    Bibliography
)
import openpyxl
from django.http import HttpResponse


# ===== Export Function =====
def export_to_excel(modeladmin, request, queryset):
    # Create Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{modeladmin.model._meta.verbose_name_plural}"
    
    # Get field names from model (exclude auto-created fields)
    field_names = [field.name for field in modeladmin.model._meta.fields if not field.auto_created]
    
    # Write headers
    for col_num, field_name in enumerate(field_names, 1):
        ws.cell(row=1, column=col_num, value=field_name.replace('_', ' ').title())
    
    # Write data
    for row_num, obj in enumerate(queryset, 2):
        for col_num, field_name in enumerate(field_names, 1):
            value = getattr(obj, field_name)
            # Handle ForeignKey fields
            if hasattr(value, '__str__'):
                value = str(value)
            ws.cell(row=row_num, column=col_num, value=value)
    
    # Create HTTP response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"{modeladmin.model._meta.verbose_name_plural}_export.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb.save(response)
    return response

export_to_excel.short_description = "Export selected to Excel"


# ===== Inlines =====
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'material_technique', 'site_monument', 
              'site_monument_latitude', 'site_monument_longitude',
              'date', 'century', 'location_of_portrait', 
              'location_of_portrait_text', 'iconographic_type', 
              'has_inscription', 'inscription_text', 'description')


class HagiographyInline(admin.TabularInline):
    model = HagiographyOrWrittenSource
    extra = 1

class CultInline(admin.TabularInline):
    model = AspectsOfCult
    extra = 1

class ArchaeologyInline(admin.TabularInline):
    model = ArchaeologicalAndArchitecturalEvidence
    extra = 1

class BibliographyInline(admin.TabularInline):
    model = Bibliography
    extra = 1

# ===== Main admin =====
@admin.register(Saint)
class SaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'type_of_saint', 'act_period_1', 'act_period_2', 'image_preview')
    list_filter = ('gender', 'type_of_saint', 'act_period_1', 'act_period_2')
    search_fields = ('id', 'name', 'region_of_birth', 'region_of_burial')
    ordering = ('name',)
    list_display_links = ('id', 'name') 
    readonly_fields = ('id',)
    actions = [export_to_excel]  # Add export action directly
    
    inlines = [
        ImageInline,
        HagiographyInline,
        CultInline,
        ArchaeologyInline,
        BibliographyInline,
    ]
    
    def image_preview(self, obj):
        images_qs = getattr(obj, "images", None) or getattr(obj, "image_set", None)
        if images_qs:
            first_image = images_qs.first()
            if first_image and first_image.image:
                return format_html(
                    '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />',
                    first_image.image.url
                )
        return "No image"
    image_preview.short_description = 'Image Preview'

# ===== Other admins =====
@admin.register(HagiographyOrWrittenSource)
class HagiographyOrWrittenSourceAdmin(admin.ModelAdmin):
    list_display = ('title_literary_text', 'saint', 'literary_source_type', 'date_or_century_of_source')
    list_filter = ('literary_source_type',)
    search_fields = ('title_literary_text', 'saint__name')
    actions = [export_to_excel]  # Add export action directly

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "saint":
            kwargs["queryset"] = Saint.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(AspectsOfCult)
class AspectsOfCultAdmin(admin.ModelAdmin):
    list_display = ('saint', 'cult_place', 'pilgrimage_site', 'status')
    list_filter = ('pilgrimage_site', 'status')
    search_fields = ('saint__name', 'cult_place')
    actions = [export_to_excel]  # Add export action directly

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "saint":
            kwargs["queryset"] = Saint.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(ArchaeologicalAndArchitecturalEvidence)
class ArchaeologicalAndArchitecturalEvidenceAdmin(admin.ModelAdmin):
    list_display = ('saint', 'cult_buildings', 'date_1', 'date_2', 'date_text', 'location')
    list_filter = ('cult_buildings',)
    search_fields = ('saint__name', 'location')
    actions = [export_to_excel]  # Add export action directly

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "saint":
            kwargs["queryset"] = Saint.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'saint', 'image', 'material_technique', 'site_monument', 'date', 'century',
        'location_of_portrait', 'location_description', 'iconographic_type',
        'has_inscription', 'inscription_text', 'description'
    )
    list_filter = ('material_technique', 'century', 'iconographic_type')
    search_fields = ('saint__name', 'site_monument')
    actions = [export_to_excel]  # Add export action directly

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "saint":
            kwargs["queryset"] = Saint.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Bibliography)
class BibliographyAdmin(admin.ModelAdmin):
    list_display = ('saint', 'reference')
    search_fields = ('saint__name', 'reference')
    actions = [export_to_excel]  # Add export action directly

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "saint":
            kwargs["queryset"] = Saint.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)