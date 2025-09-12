from django.db import models
from multiselectfield import MultiSelectField


class Saint(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    SAINT_TYPE_CHOICES = [
        ('Bishop', 'Bishop'),
        ('Monk-Ascetic', 'Monk-Ascetic'),
        ('Hermit-Recluse', 'Hermit-Recluse'),
        ('Martyr', 'Martyr'),
        ('Deacon', 'Deacon'),
        ('Other', 'Other'),
    ]
    ACT_PERIOD_CHOICES = [
        ('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'),
        ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th'),
        ('9th', '9th'), ('10th', '10th'), ('Unknown', 'Unknown')
    ]

    name = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    type_of_saint = models.CharField(max_length=20, choices=SAINT_TYPE_CHOICES, blank=True, null=True)
    act_period_1 = models.CharField(max_length=10, choices=ACT_PERIOD_CHOICES, blank=True, null=True)
    act_period_2 = models.CharField(max_length=10, choices=ACT_PERIOD_CHOICES, blank=True, null=True)
    act_period_text = models.CharField(max_length=100, blank=True, null=True)
    # Region of Birth + Coordinates
    region_of_birth = models.TextField(blank=True, null=True)
    region_of_birth_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    region_of_birth_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Region of Burial + Coordinates
    region_of_burial = models.TextField(blank=True, null=True)
    region_of_burial_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    region_of_burial_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    feast_day = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Saint"

    class Meta:
        ordering = ['name']
        verbose_name = 'Saint'
        verbose_name_plural = 'Saints'


class HagiographyOrWrittenSource(models.Model):
    LITERARY_SOURCE_CHOICES = [
        ('Lives', 'Lives'),
        ('Miracles', 'Miracles'),
        ('Accounts of martyrdom', 'Accounts of martyrdom'),
        ('New testament', 'New testament'),
        ('Other', 'Other'),
    ]
    LITURGICAL_SOURCE_CHOICES = [
        ('Liturgical compilation', 'Liturgical compilation'),
        ('Hymns', 'Hymns'),
        ('Other', 'Other'),
    ]

    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, related_name='hagiographies', blank=True, null=True)
    literary_source_type = models.CharField(max_length=25, choices=LITERARY_SOURCE_CHOICES, blank=True, null=True)
    date_or_century_of_source = models.CharField(max_length=20, blank=True, null=True)
    title_literary_text = models.TextField(blank=True, null=True)
    liturgical_texts_source_type = models.CharField(max_length=25, choices=LITURGICAL_SOURCE_CHOICES, blank=True, null=True)
    date_or_century_of_liturgical_source = models.CharField(max_length=20, blank=True, null=True)
    title_liturgical_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title_literary_text} ({self.saint.name if self.saint else 'Unknown Saint'})"

    class Meta:
        verbose_name = 'Hagiography or Written Source'
        verbose_name_plural = 'Hagiographies and Written Sources'
        ordering = ['title_literary_text']


class AspectsOfCult(models.Model):
    PILGRIMAGE_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive'), ('Lost', 'Lost')]

    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, related_name='cult_aspects', blank=True, null=True)
    cult_place = models.TextField(blank=True, null=True)
    cult_place_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    cult_place_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    pilgrimage_site = models.CharField(max_length=3, choices=PILGRIMAGE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, blank=True, null=True)
    activities_accompanying_cult = models.TextField(blank=True, null=True)
    relics_cult_related_objects = models.TextField(blank=True, null=True)
    relics_cult_related_objects_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    relics_cult_related_objects_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    miracles = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cult of {self.saint.name if self.saint else 'Unknown'} at {self.cult_place or 'Unknown place'}"

    class Meta:
        verbose_name = 'Aspect of Cult'
        verbose_name_plural = 'Aspects of Cult'


class ArchaeologicalAndArchitecturalEvidence(models.Model):
    CULT_BUILDINGS_CHOICES = [
        ('Cult building - Church', 'Cult building - Church'),
        ('Cult building - Chapel', 'Cult building - Chapel'),
        ('Cult building - Monastic Building', 'Cult building - Monastic Building'),
        ('Burial site - Crypt', 'Burial site - Crypt'),
        ('Burial site - Tomb', 'Burial site - Tomb'),
        ('Burial site - Sarcophagus', 'Burial site - Sarcophagus'),
        ("Saint's Life Site", "Place associated with saint's life"),
        ('Holy Spring', 'Holy spring'),
        ('Other', 'Other'),
    ]
    ACT_PERIOD_CHOICES = [
        ('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'),
        ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th'),
        ('9th', '9th'), ('10th', '10th'), ('11th', '11th'),
        ('12th', '12th'), ('13th', '13th'), ('14th', '14th'),
        ('15th', '15th'), ('16th', '16th'), ('Unknown', 'Unknown')
    ]
    CURRENT_CONDITION = [
        ('In use', 'In use'),
        ('Ruin', 'Ruin'),
        ('Restored', 'Restored'),
        ('Excavated', 'Excavated'),
        ('Other', 'Other')
    ]
  
    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, related_name='archaeological_evidence', blank=True, null=True)
    cult_buildings = models.CharField(max_length=50, choices=CULT_BUILDINGS_CHOICES, blank=True, null=True)
    cult_buildings_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    cult_buildings_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    date_1 = models.CharField(max_length=10, choices=ACT_PERIOD_CHOICES, blank=True, null=True)
    date_2 = models.CharField(max_length=10, choices=ACT_PERIOD_CHOICES, blank=True, null=True)
    date_text = models.CharField(max_length=100, blank=True, null=True)
    current_condition = models.CharField(max_length=50, choices=CURRENT_CONDITION, blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_cult_buildings_display() if self.cult_buildings else 'Unknown building'} at {self.location or 'Unknown location'}"

    class Meta:
        verbose_name = 'Archaeological and Architectural Evidence'
        verbose_name_plural = 'Archaeological and Architectural Evidences'


class Image(models.Model):
    MATERIAL_TECHNIQUE_CHOICES = [
        ('Wall Painting', 'Wall Painting'),
        ('Icon', 'Icon'),
        ('Other', 'Other'),
    ]
    CENTURY_CHOICES = [
        ('10th', '10th'), ('11th', '11th'), ('12th', '12th'),
        ('13th', '13th'), ('14th', '14th'), ('15th', '15th'), ('16th', '16th'),
    ]
    LOCATION_CHOICES = [
        ('Sanctuary', 'Sanctuary'),
        ('Naos', 'Naos'),
        ('Narthex', 'Narthex'),
    ]
    ICONOGRAPHIC_TYPE_CHOICES = [
        ('Portrait', 'Portrait'),
        ('Scene', 'Scene of life')
    ]

    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = models.ImageField(upload_to='saint_images/', blank=True, null=True)
    material_technique = models.CharField(max_length=20, choices=MATERIAL_TECHNIQUE_CHOICES, blank=True, null=True)
    site_monument = models.TextField(blank=True, null=True)
    site_monument_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    site_monument_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    date = models.CharField(max_length=20, blank=True, null=True)
    century = models.CharField(max_length=4, choices=CENTURY_CHOICES, blank=True, null=True)
    location_of_portrait = models.CharField(max_length=20, choices=LOCATION_CHOICES, blank=True, null=True)
    location_of_portrait_text = models.TextField(blank=True, null=True)
    location_description = models.TextField(blank=True, null=True)
    iconographic_type = models.CharField(max_length=20, choices=ICONOGRAPHIC_TYPE_CHOICES, blank=True, null=True)
    has_inscription = models.BooleanField(null=True, blank=True)
    inscription_text = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_material_technique_display() if self.material_technique else 'Unknown'} of {self.saint.name if self.saint else 'Unknown'}"

    @property
    def image_url(self):
        """Return safe URL for the image or a placeholder if missing."""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/img/placeholder.png'  

    class Meta:
        verbose_name = 'Saint Image'
        verbose_name_plural = 'Saint Images'


class Bibliography(models.Model):
    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, related_name='bibliographies', blank=True, null=True)
    reference = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.reference[:50]}..." if self.reference else "No reference"

    class Meta:
        verbose_name_plural = 'Bibliographies'


class SaintBuilding(models.Model):
    BUILDING_TYPE_CHOICES = [
        ('Church', 'Church'),
        ('Chapel', 'Chapel'),
        ('Monastery', 'Monastery'),
        ('Shrine', 'Shrine'),
        ('Other', 'Other'),
    ]

    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, related_name='buildings', blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    building_type = models.CharField(max_length=20, choices=BUILDING_TYPE_CHOICES, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    construction_date = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.name or 'Unnamed'} ({self.get_building_type_display() if self.building_type else 'Unknown'})"

    class Meta:
        verbose_name = 'Saint Building'
        verbose_name_plural = 'Saint Buildings'
