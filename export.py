import os
import django
import pandas as pd

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saint_project.settings')
django.setup()

from saints.models import Saint

rows = []

for s in Saint.objects.all():
    max_related = max(
        s.hagiographies.count(),
        s.cult_aspects.count(),
        s.archaeological_evidence.count(),
        s.images.count(),
        s.bibliographies.count(),
        1  # at least one row even if no related objects
    )

    for i in range(max_related):
        # Hagiography
        h = s.hagiographies.all()[i] if i < s.hagiographies.count() else None
        # Cult Aspect
        c = s.cult_aspects.all()[i] if i < s.cult_aspects.count() else None
        # Archaeological Evidence
        a = s.archaeological_evidence.all()[i] if i < s.archaeological_evidence.count() else None
        # Image
        img = s.images.all()[i] if i < s.images.count() else None
        # Bibliography
        b = s.bibliographies.all()[i] if i < s.bibliographies.count() else None

        rows.append({
            'Name': s.name,
            'Gender': s.gender,
            'Type': s.type_of_saint,
            'Active Period 1': s.act_period_1,
            'Active Period 2': s.act_period_2,
            'Active Period Text': s.act_period_text,
            'Region of Birth': s.region_of_birth,
            'Region of Burial': s.region_of_burial,
            'Feast Day': s.feast_day,

            # Hagiography fields
            'Hagiography Literary Title': h.title_literary_text if h else None,
            'Hagiography Literary Century': h.date_or_century_of_source if h else None,
            'Hagiography Literary Type': h.literary_source_type if h else None,
            'Hagiography Liturgical Title': h.title_liturgical_text if h else None,
            'Hagiography Liturgical Century': h.date_or_century_of_liturgical_source if h else None,
            'Hagiography Liturgical Type': h.liturgical_texts_source_type if h else None,

            # Cult Aspect fields
            'Cult Place': c.cult_place if c else None,
            'Pilgrimage Site': c.pilgrimage_site if c else None,
            'Cult Status': c.status if c else None,
            'Cult Activities': c.activities_accompanying_cult if c else None,
            'Relics/Objects': c.relics_cult_related_objects if c else None,
            'Miracles': c.miracles if c else None,

            # Archaeological Evidence fields
            'Evidence Type': a.get_cult_buildings_display() if a else None,
            'Evidence Location': a.location if a else None,
            'Evidence Date 1': a.date_1 if a else None,
            'Evidence Date 2': a.date_2 if a else None,
            'Evidence Date Text': a.date_text if a else None,
            'Evidence Condition': a.current_condition if a else None,

            # Image fields
            'Image File': img.image.url if img and img.image else None,
            'Image Material/Technique': img.get_material_technique_display() if img else None,
            'Image Site/Monument': img.site_monument if img else None,
            'Image Century': img.century if img else None,
            'Image Portrait Location': img.location_of_portrait if img else None,
            'Image Portrait Location Text': img.location_of_portrait_text if img else None,
            'Image Has Inscription': img.has_inscription if img else None,
            'Image Inscription Text': img.inscription_text if img else None,
            'Image Description': img.description if img else None,

            # Bibliography
            'Bibliography': b.reference if b else None
        })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Save to Excel
output_file = os.path.join(os.getcwd(), 'saints_export_flat.xlsx')
df.to_excel(output_file, index=False)

print(f"Exported {len(rows)} rows to {output_file}")
